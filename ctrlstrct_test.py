# encoding: utf-8
# ctrlstrct_test.py

"""
Тестирование получения ошибок из онтологии на имеющихся алгоритмах и трассах

"""

# import json
import os
import re

###
import ctrlstrct_run

from ctrlstrct_run import process_algtraces, TraceTester
from trace_gen.json2alg2tr import act_line_for_alg_element
from trace_gen.txt2algntr import parse_text_files, parse_algorithms_and_traces_from_text, search_text_trace_files, get_ith_expr_value, find_by_key_in, find_by_keyval_in
from onto_helpers import get_relation_object, delete_ontology
import trace_gen.styling as styling

from common_helpers import Checkpointer


TEST_DIR = "./test_data"
OUTPUT_FNM = "output.json"
REPORT_FNM = "run_report.txt"
TESTS_FNM = "tests.json"

ALG_FILE_FIELD = "alg_input"
TRACE_FILE_FIELD = "trace_input"
REFERENCE_DATA_FIELD = "reference_output"

# SAVE_RDF = True
SAVE_RDF = False
# EVALUATE = True
EVALUATE = False

# global log storage
LOG = []


def log_print(*args, sep=" ", end="\n"):
	s = sep.join(map(str, args)) + end
	print(s, end="")
	LOG.append(s)

# def replace_print()	:
# 	pass

def object_to_hashable(obj, discard_dict_keys=()):
	if isinstance(obj, (tuple, str, int, float)):
		return obj
	if isinstance(obj, (list, set)):
		return tuple(object_to_hashable(x, discard_dict_keys) for x in obj)
	if isinstance(obj, dict):
		data = []
		for key in sorted(set(obj.keys()) - set(discard_dict_keys)):
			# print(key, discard_dict_keys)
			data.append(key)
			data.append( object_to_hashable(obj[key], discard_dict_keys) )
		return tuple(data)

def compare_mistakes(expected, actual, ignored_fields=("name",)):
	"""Precise but configurable list of dicts comparison"""
	assert isinstance(expected, list), "mistakes list expected"
	assert isinstance(actual, list), "mistakes list expected"

	# проверка совпадения количества
	if len(expected) != len(actual):
		return False, "%d mistakes (expected %d)" % (len(actual), len(expected))

	# проверка совпадения полей
	def unified_fields(dicts_list):
		return {
			tuple(sorted(
				set(d.keys()) - set(ignored_fields)
			))
			for d in dicts_list
		}

	keys_set_e = unified_fields(expected)
	keys_set_a = unified_fields(actual)

	if keys_set_e != keys_set_a:
		extra = keys_set_a - keys_set_e
		missing = keys_set_e - keys_set_a
		if 1:  # extra or missing:
			return False, "Mistakes' fields do not match: %d missing: (%s), %d extra (%s)" % (len(missing), str(missing), len(extra), str(extra), )

	# проверка совпадения значений полей
	data_e = (object_to_hashable(expected, ignored_fields))
	data_a = (object_to_hashable(actual  , ignored_fields))
	if data_e != data_a:
		# ...
		print(data_e)
		print(data_a)
		return False, "Mistakes' data mismatch <...TODO...>"

	return True, "ok"

def resolve_path(fname, directory='.'):
	for case_path in [
		os.path.join(directory, fname),
		fname,
		"/" + fname, ]:
		if os.path.exists(case_path):
			return case_path
	return None


def validate_mistakes(trace:list, mistakes:list, onto) -> (bool, str):
	"Находит расхождения в определении ошибочных строк трассы"

	# print(f"mistakes: {mistakes}")

	# extract erroneous acts provided by trace
	def error_description(comment_str) -> list:
		if "error" in comment_str or "ошибк" in comment_str:
			# For input str "error: LastConditionIsFalseButNoElse, TooEarly (Нет ветки ИНАЧЕ)"
			# the result will be ['LastConditionIsFalseButNoElse', 'TooEarly']
			m = re.search(r"(?:ошибк[аи]|errors?)\s*:?\s*([^()]*)\s*(?:\(.+\).*)?$", comment_str, re.I)
			if m:
				err_names = m.group(1).strip()
				return re.split(r"\s*,?\s+", err_names)
		return None

	text_lines = [d["text_line"] for d in trace]
	error_descrs = {d["text_line"]: error_description(d["comment"]) for d in trace}


	# extract erroneous acts and messages from error instances (inferred)
	err_objs = []
	err_obj_id2msgs = {}

	# get text lines of the inferred erroneous acts
	inferred_error_lines = [dct["text_line"] for dct in mistakes]
	inferred_error_lines = [arr[0] if arr else None for arr in inferred_error_lines]

	for dct, line in zip(mistakes, inferred_error_lines):
		if line in text_lines:  # ignore unrelated errors (possibly related to another trace)
			err_objs.append(dct)
			err_obj_id2msgs[id(dct)] = dct["classes"]

	inferred_error_lines = [dct["text_line"][0] for dct in err_objs]  # reassign from filtered array

	# do check
	differences = []

	def _compare_mistakes(expected: list, inferred: list, line_i) -> str or None:
		if not expected and not inferred:
			return None

		if expected and not inferred:
			return f"Erroneous line {line_i} hasn't been recognized by the ontology. Expected mistakes: {', '.join(expected)}"

		if not expected and inferred:
			return f"Correct line {line_i} has been recognized by the ontology as erroneous. Inferred mistakes: {', '.join(inferred)}"

		(recognized, not_recognized, extra) = ([], [], inferred[:])
		for err_word in expected:
			for inferred_descr in extra[:]:
				if err_word and err_word.lower() in inferred_descr.lower():
					recognized.append(inferred_descr)
					extra.remove(inferred_descr)
					break
			else:
				not_recognized.append(err_word)

		if not not_recognized and not extra:
			return None

		m = f"Erroneous line {line_i} has been recognized by the ontology partially only ({', '.join(recognized) or 'None in common'}). Expected but not recognized - {len(not_recognized)} ({', '.join(not_recognized) or None}). Inferred but not expected - {len(extra)} ({', '.join(extra) or None})."
		return m


	# first_err_line = None  # из размеченных комментариями в трассе
	for line_i in text_lines:
		descr_messages = []
		for descr_line_i, err_descr in error_descrs.items():
			if err_descr and descr_line_i == line_i:
				descr_messages = err_descr
				break

		# gather all inferred mistakes
		inferred_messages = set()
		if line_i in inferred_error_lines:
			for inferred_line_i, err_obj in zip(inferred_error_lines, err_objs):
				if line_i == inferred_line_i:
					inferred_messages |= set(err_obj_id2msgs[id(err_obj)])

		m = _compare_mistakes(descr_messages, list(inferred_messages), line_i)
		if m:
			differences.append(m)

	if differences:
		return False, "\n\t> ".join(["",*differences])
	return True, "Validation ok."

def process_algorithm_and_trace_from_text(text: str, process_kwargs=dict(reasoning="jena")):
	feedback = {"messages": []}

	try:
		alg_trs = parse_algorithms_and_traces_from_text(text)
	except Exception as ex:
		alg_trs = None
		feedback["messages"] += [str(ex)]

	if not alg_trs:
		feedback["messages"] += ["Nothing to process: no valid algorithm / trace found."]
		return feedback

	mistakes, err_msg = process_algorithms_and_traces(alg_trs, process_kwargs)

	if err_msg:
		feedback["messages"] += [err_msg]
	else:
		feedback["messages"] += ["Processing of algorithm & trace finished OK."]
		feedback["mistakes"] = mistakes

	return feedback

def process_algorithm_and_trace_from_json(alg_tr: dict, process_kwargs=dict(reasoning="jena")):
	feedback = {"messages": []}

	# validate input alg_tr
	# {
	#     "trace_name"    : str,
	#     "algorithm_name": str,
	#     "trace"         : list,
	#     "algorithm"     : dict,
	#     "header_boolean_chain" : list of bool,
	# }
	try:
		assert alg_tr, f"Empty data"
		assert type(alg_tr) == dict, f"'JSON data is not a dict!";
		key = "trace_name"; t = str;
		assert key in alg_tr, f"Key '{key}' is missing"; assert type(alg_tr[key]) == t, f"'{key}' -> is not a {str(t)}";
		key = "algorithm_name";  t = str;
		assert key in alg_tr, f"Key '{key}' is missing"; assert type(alg_tr[key]) == t, f"'{key}' -> is not a {str(t)}";
		key = "trace";  t = list;
		assert key in alg_tr, f"Key '{key}' is missing"; assert type(alg_tr[key]) == t, f"'{key}' -> is not a {str(t)}";
		key = "algorithm";  t = dict;
		assert key in alg_tr, f"Key '{key}' is missing"; assert type(alg_tr[key]) == t, f"'{key}' -> is not a {str(t)}";
	except Exception as e:
		feedback["messages"] += [f"JSON error: {str(e)}\n{alg_tr}"]
		return feedback

	alg_trs = [alg_tr]

	if not alg_trs:
		feedback["messages"] += ["Nothing to process: no valid algorithm / trace found."]
		return feedback

	mistakes, err_msg = process_algorithms_and_traces(alg_trs, process_kwargs)

	if err_msg:
		feedback["messages"] += [err_msg]
	else:
		feedback["messages"] += ["Processing of algorithm & trace finished OK."]
		feedback["mistakes"] = mistakes

	return feedback


def make_act_json(algorithm_json, algorithm_element_id: int, act_type: str, existing_trace_json, user_language=None) -> list:
	'''
	act_type: начало ('started') или конец ('finished') - для составных, 'performed' - для простых (атомарных)
	Returns full supplemented trace: list of dicts, each dict represents act object.
	(Returns string with error description if an exception occured)
	'''
	# Отфильтровать неправильные акты (если есть)
	# existing_trace_json
	existing_trace_json = existing_trace_json or ()
	existing_trace_list = [act for act in existing_trace_json if act["is_valid"] == True]

	### print(algorithm_element_id, act_type, *existing_trace_list, sep='\n')

	try:
		elem = algorithm_json["id2obj"].get(algorithm_element_id, algorithm_json["id2obj"].get(str(algorithm_element_id)))

		assert elem, f"No element with id={algorithm_element_id} in given algorithm."

		max_id = max(a['id'] for a in existing_trace_list) if existing_trace_list else 100 - 1

		result_acts = []
		if len(existing_trace_list) == 0 and elem['id'] != algorithm_json["entry_point"]['id']:
			# создать строку "program began"
			act_text = act_line_for_alg_element(algorithm_json, phase='started', lang=user_language, )  # передаём сам корень алгоритма, так как его type=='algorithm',
			max_id += 1
			html_tags = styling.prepare_tags_for_line(act_text)
			result_acts.append({
				'executes': algorithm_json["entry_point"]['id'],  # ! а привязываем к глобальному коду (или функции main)
				'name': algorithm_json["entry_point"]['name'],
				'phase': 'started',
				'as_string': act_text,
				# 'as_tags': html_tags,
				'as_html': styling.to_html(html_tags),
				'id': max_id,
				'n': 1,
				'is_valid': True  # в начале трассы акт всегда такой
				})

		exec_time = 1 + len([a for a in existing_trace_list if a['executes'] == algorithm_element_id and a['phase'] == act_type])

		### print("exec_time:", exec_time)

		expr_value = None
		if elem['type'] == "expr" and act_type in ('finished', 'performed'):
			name = elem['name']
			expr_list = algorithm_json['expr_values'].get(name, None)

			assert expr_list is not None, f"No expression values provided for expression '{name}' in given algorithm."

			expr_value = get_ith_expr_value(expr_list, exec_time - 1)

			# assert expr_value is not None, f"Not enough expression values provided for expression '{name}': '{expr_list}' provided, # {exec_time} requested."
			if expr_value is None:
				expr_value = False
				print(f"Info: use default value: {expr_value} for expression '{name}'.")

		act_text = act_line_for_alg_element(
			elem,
			phase=act_type,
			lang=user_language,
			expr_value=expr_value,
			use_exec_time=exec_time,
			)
		max_id += 1
		html_tags = styling.prepare_tags_for_line(act_text)
		act_json = {
				'executes': elem['id'],
				'name': elem['name'],
				'phase': act_type,
				'as_string': act_text,
				# 'as_tags': html_tags,
				'as_html': styling.to_html(html_tags),
				'id': max_id,
				'n': exec_time,
				'is_valid': None,  # пока нет информации о корректности такого акта
				# 'is_valid': True,  # debug !!
		}
		if expr_value is not None:
			act_json['value'] = expr_value

		result_acts.append(act_json)

		# print(result_acts)
		return existing_trace_list + result_acts
	except Exception as e:
		# raise e
		return f"Server error in make_act_json() - {type(e).__name__}:\n\t{str(e)}"


def add_styling_to_trace(algorithm_json, trace_json, user_language=None, comment_style=None, add_tags=False) -> list:
	'''Adds text line, tags and html form for each act in given trace and returns the same reference to the trace list
	
	comment_style: {None | 'use' | 'highlight'}'''
	try:
		assert isinstance(trace_json, (list, tuple)), "The trace was not correctly constructed: " + str(trace_json)

		for act_dict in trace_json:

			algorithm_element_id = act_dict['executes']
			elem = algorithm_json["id2obj"].get(algorithm_element_id, algorithm_json["id2obj"].get(str(algorithm_element_id), None))

			assert elem, f"No element with id={algorithm_element_id} in given algorithm."

			if elem['id'] == algorithm_json["entry_point"]['id']:
				# создать строку типа "program began"
				# act_text = act_line_for_alg_element(algorithm_json, phase='started', lang=user_language, )  # передаём сам корень
				elem = algorithm_json

			act_text = act_line_for_alg_element(
				elem,
				phase=act_dict['phase'],
				lang=user_language,
				expr_value=act_dict.get('value', None),
				use_exec_time=int(act_dict['n']),
				)
			if 'comment' in act_dict and act_dict['comment'] and comment_style is not None:
				act_text += "    // " + act_dict['comment']
				
			html_tags = styling.prepare_tags_for_line(act_text)

			if 'comment' in act_dict and act_dict['comment'] and comment_style == 'highlight':
				html_tags = {
					"tag": "span",
					"attributes": {"class": ["warning"]},
					"content": html_tags
				}
				
			add_json = {
				'as_string': act_text,
				'as_html': styling.to_html(html_tags),
			}
			act_dict.update(add_json)
			if add_tags:
				add_json = {
					'as_tags': html_tags,
				}
				act_dict.update(add_json)

		return trace_json
	except Exception as e:
		# raise e
		return f"Server error in add_styling_to_trace() - {type(e).__name__}:\n\t{str(e)}"


def process_algorithms_and_traces(alg_trs_list: list, write_mistakes_to_acts=False, process_kwargs=dict(reasoning="jena", debug_rdf_fpath=None and 'test_data/ajax.rdf')) -> ('mistakes', 'error_message: str or None'):

	try:
		onto, mistakes = process_algtraces(alg_trs_list, verbose=0, mistakes_as_objects=False, **process_kwargs)

		if not mistakes and len(alg_trs_list) == 1:
			### print("[] try to find automatically polyfilled acts ...")
			# try to find automatically polyfilled acts & insert them into the trace
			# apply simplest behaviour: skipped acts will be inserted to the previous-to-the-last position.
			if implicit_acts := list(onto.implicit_act.instances()):
				implicit_acts.sort(key=lambda a: a.id)
				acts_count = len(implicit_acts)
				print(acts_count, 'implicit_acts found, inserting them into trace.')

				algorithm = alg_trs_list[0]["algorithm"]
				# to be modified in-place (new acts will be inserted to prev. to the last)
				mutable_trace = alg_trs_list[0]["trace"]

				for imp_act in implicit_acts:
					bound = imp_act.executes
					assert bound
					st = bound.boundary_of
					assert st
					algorithm_element_id = st.id
					if onto.act_end in imp_act.is_a:
						act_type = "finished"
					elif onto.act_begin in imp_act.is_a:
						act_type = "started"
					else:
						raise ValueError("implict act has no begin/end type!: %s" % imp_act)
					apended_trace = make_act_json(algorithm_json=algorithm, algorithm_element_id=algorithm_element_id, act_type=act_type, existing_trace_json=mutable_trace[:-1], user_language=None)
					assert len(apended_trace) >= 2, apended_trace
					mutable_trace.insert(-1, apended_trace[-1])
					### print("+++ inserted act:", apended_trace[-1])
				# end for

			if fihish_trace_acts := list(onto.fihish_trace_act.instances()):
				# fihish_trace_act exists => finish the trace.

				print('fihish_trace_act found, closing the trace.')
				act = fihish_trace_acts[0]

				algorithm = alg_trs_list[0]["algorithm"]
				# to be modified in-place (new acts will be inserted to prev. to the last)
				mutable_trace = alg_trs_list[0]["trace"]

				bound = act.executes
				assert bound
				end_of_trace_bound = bound.consequent[0]
				assert end_of_trace_bound
				st = end_of_trace_bound.boundary_of
				assert st

				algorithm_element_id = st.id
				act_type = "finished"

				apended_trace = make_act_json(algorithm_json=algorithm, algorithm_element_id=algorithm_element_id, act_type=act_type, existing_trace_json=mutable_trace[:], user_language=None)
				assert len(apended_trace) >= 2, apended_trace
				mutable_trace.append(apended_trace[-1])
				###
				print("+=+ inserted closing act:", apended_trace[-1]["as_string"])


		delete_ontology(onto)

		# from pprint import pprint
		# pprint(mistakes)

		if write_mistakes_to_acts and len(alg_trs_list) != 1:
			print("** Warning!: write_mistakes_to_acts is inapplicable when traces count =", len(alg_trs_list), "(!=1)")
		if write_mistakes_to_acts and len(alg_trs_list) == 1:
			# ошибки нужны, и сейчас не режим тестирования
			trace = alg_trs_list[0]['trace']
			for mistake in mistakes:
				act_id = mistake["id"][0]
				for act_obj in list(find_by_keyval_in("id", act_id, trace)):
					new_explanations = act_obj.get("explanations", []) + mistake["explanations"]
					act_obj["explanations"] = sorted(set(new_explanations))
					if not act_obj["explanations"]:  # был пустой список - запишем хоть что-то
						act_obj["explanations"] = ["Ошибка обнаружена, но вид ошибки не определён."]
					act_obj["mistakes"] = mistake
					act_obj["is_valid"] = False
					if 'value' in act_obj:
						print(" ***** Reset expr evaluation value.")
						act_obj["value"] = "not evaluated"
						# del act_obj["value"]
						alg_data = alg_trs_list[0]['algorithm']
						# rewrite this act
						add_styling_to_trace(alg_data, [act_obj])
					# break

			# Apply correctness mark to other acts:  act_obj["is_valid"] = True
			for act_obj in trace:
				if act_obj["is_valid"] is None:
					act_obj["is_valid"] = True

			# Признак окончания трассы
			# set act_obj["is_final"] = True for end of the topmost statement
			top_stmts = set()
			for alg_obj in find_by_keyval_in("type", "algorithm", alg_trs_list):
				top_stmts.add(alg_obj["entry_point"]["body"][-1]["id"])
			assert top_stmts, top_stmts

			for act_obj in trace:
				if (act_obj["is_valid"] == True
						and act_obj["phase"] in ('finished', "performed")
						and act_obj["executes"] in top_stmts):
					act_obj["is_final"] = True

		return mistakes, None
	except Exception as e:
		msg = "Exception occured in process_algorithms_and_traces(): %s: %s"%(str(type(e)), str(e))
		raise e
		print(msg)
		return [], msg


def grid_question(alg, skip_redundant_checks=False):
	""" Try all possible options "to click" for each step of building the trace.
		Alert if multiple or no correct answers are found at a time.
		Gather and return possible mistake types for each step.

		If True, `skip_redundant_checks` may result in incomplete mistakes set.
	 """

	# use repair_data
	tt = TraceTester({
					"trace_name"    : 'trace_name',
					"algorithm_name": "alg_name",
					"trace"         : [],
					"algorithm"     : alg,
					"header_boolean_chain": None
				})
	tt.prepare_id2obj()

	# print(alg)

	# find all available "buttons" to "click"
	actions = []  # list of tuples: (id, phase)
	for d in find_by_key_in("id", alg['entry_point']):
		if 'type' in d:
			if d['type'] in ('expr', 'stmt'):
				act_types = ['performed']
			else:
				act_types = ['finished', 'started', ]
			for phase in act_types:
				item = ((d['id']), phase)
				# actions.append(item)
				actions.insert(0, item)
				###
				# print(repr(d['id']), d["act_name"]["ru"])
				###

	# actions = list(reversed(actions))

	###
	print("grid_question():", len(actions), "actions found in algorithm.")
	for i, action in enumerate(actions):
		print("\t%d)" % (i + 1), action[0], action[1], ":", alg["id2obj"].get(action[0])["act_name"]["ru"])
	###

	partial_trace = []  # is always correct
	trace_completed = False
	steps = []

	ch = Checkpointer()

	# step-by-step building the trace
	while not trace_completed:
		step = {
			'mistakes': set(),
			'correct_answer': None,
		}
		steps.append(step)

		correct_acts = None

		for i, (action_id, phase) in enumerate(actions):
			###
			print(">>>")
			print(">>> Griding ... step", len(partial_trace) + 1, "take", i + 1)
			print(">>>")
			###

			# obtain a new partial trace with act-candidate
			acts = make_act_json(algorithm_json=alg, algorithm_element_id=action_id,
				act_type=phase,
				existing_trace_json=partial_trace,
				user_language='en',
			)

			###
			assert isinstance(acts[0], dict), acts
			print("Trying act:", acts[-1]["as_string"])

			alg_trs = [{
				"trace_name"    : 'trace_name',
				"algorithm_name": "alg_name",
				"trace"         : acts,  # [*partial_trace, *acts]
				"algorithm"     : alg,
				"header_boolean_chain": None
			}]

			# process_algorithms_and_traces(alg_trs, write_mistakes_to_acts=True)
			try:
				_onto, mistakes = process_algtraces(alg_trs, verbose=0, mistakes_as_objects=False, reasoning="jena", debug_rdf_fpath=None)

			except Exception as e:
				msg = "Exception occured running reasoner while griding a question: %s: %s"%(str(type(e)), str(e))
				raise e
				print(msg)
				# return [], msg

			if not mistakes:
				if step["correct_answer"]:
					# one more correct answer!
					print("** grid_question(): Alert!")
					print("** grid_question(): Alert! Multiple correct answers at the same point!")
				else:
					correct_acts = acts
					step["correct_answer"] = (action_id, phase)
					print("\t+++")
					print("\t++ Correct step(s) found:", *['%d: %s' % (d["executes"], d["as_string"]) for d in acts], sep="\n\t\t")
					print("\t+++")

				# a simple finish heuristic
				if phase == 'finished' and partial_trace and action_id == partial_trace[0]["executes"]:
					print(" >>>> Trace building completed successfully! <<<<")
					trace_completed = True
					# Last act is "program ended", so further griding makes no sense
					break

				if skip_redundant_checks:
					break

			else:
				curr_mistakes = {m for d in mistakes for m in d["classes"]}
				step["mistakes"].update(curr_mistakes)


		if not correct_acts:
			# no correct answer!
			print("** grid_question(): Alert! No correct answers at the point!")
			break

		# add correct act(s) to trace
		for act in correct_acts:
			act["is_valid"] = True
		partial_trace = correct_acts

		print("Mistakes possible at this step:", step["mistakes"])

		# inner loop end
		ch.hit("Griding step completed in")

	# outer loop end
	ch.since_start("Griding question completed in")

	return steps


def get_question_mistakes_via_grid(alg_data, skip_redundant_checks=False):
	try:
		steps = grid_question(alg_data, skip_redundant_checks)
		mistakes_set = {m for step in steps for m in step['mistakes']}
		return sorted(mistakes_set)
	except Exception as e:
		print("!* Exception in get_question_mistakes_via_grid():")
		print(e)
		return []


def run_tests(directory="test_data/", process_kwargs={}):

	files = search_text_trace_files(directory="handcrafted_traces/")

	### Отладочная заглушка !
	# files = [f for f in files if "example" in f]
	# files = [f for f in files if "correct_branching" in f]

	alg_trs = parse_text_files(files)

	### Отладочная заглушка !
	# alg_trs = alg_trs[:1]

	test_count = len(alg_trs)

	if test_count == 0:
		print("Nothing to test: no valid traces found.")
		return True

	success_all = True
	failed = 0
	mistakes = []

	try:
		if True:
			if SAVE_RDF:
				ontology_file = "test_make_trace" + "_output.rdf"
				ontology_fpath = os.path.join(directory, ontology_file)

			else:
				ontology_fpath = None

			if not EVALUATE:
				onto, mistakes = process_algtraces(alg_trs, verbose=1, debug_rdf_fpath=ontology_fpath, mistakes_as_objects=True, **process_kwargs)
			else:  # EVALUATE !
				dataset = os.path.splitext(os.path.split(files[0])[1])[0]
				eval_results = []
				# 46
				for n in sorted({
					# 11 , 12 , 14 , 17 , 18 , 21 , 23 , 24 , 26 , 27 , 29 , 32 , 33 , 36 , 38 , 39 , 41 , 42 , 44 , 47 , 48 , 51 , 53 , 54 , 56 , 57 , 59 , 62 , 63 , 66 , 68 , 69 , 71 , 72 , 74 , 77 , 78 , 81 , 83 , 84 , 86 , 87 , 89 , 91 , 92 , 93 , 94 , 105 , 115 , 125
									# *range(1, 9 + 1, 1),
									# *range(5, 100 + 1, 5),
									# *range(100, 201 + 1, 10),
									# *range(85, 140 + 1, 10),
									# *range(60, 130 + 1, 5),
									# *range(65, 95 + 1, 5),
									88
								}):
					# reasoners = ("pellet", )
					# reasoners = ("prolog", ); alg_trs = alg_trs[:22]  # !!!
					reasoners = ("sparql", )
					# reasoners = ("jena", )
					# reasoners = ("clingo", )
					# reasoners = ("dlv", )
					# reasoners = ("jena", "clingo")
					# reasoners = ("jena", "sparql")
					# reasoners = ("jena", "prolog", "sparql")
					# reasoners = ("clingo", "jena", "prolog", "sparql")
					for reasoning_type in reasoners:
						process_kwargs["reasoning"] = reasoning_type

						print(' >  >  >  >  >  >  >  >  >  >  >  >  > ')
						print(f"  Running {n} traces with {reasoning_type}")
						print(' <  <  <  <  <  <  <  <  <  <  <  <  < ')

						eval_result = process_algtraces(alg_trs, verbose=0, debug_rdf_fpath=None, mistakes_as_objects=True, _eval_max_traces=n, **process_kwargs)

						eval_item = {
							'dataset': dataset,
							'reasoner': reasoning_type,
							'count': n,
						}
						eval_item.update(eval_result)

						# dump current result
						with open('partial_eval.txt', "a") as file:
							file.write(str(eval_item))
							file.write('\n')

						eval_results.append(eval_item)

					# break

				# dump full result
				with open('full_eval.txt', "a") as file:
					for eval_item in eval_results:
						file.write(str(eval_item))
						file.write('\n')

				print(' ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^ ')
				print("Eval finished.")
				exit()
		# else:
		# 	for i, test_data in enumerate(alg_trs):
		# 		try:
		# 			assert "trace_name"     in test_data, "trace_name"
		# 			assert "algorithm_name" in test_data, "algorithm_name"
		# 			assert "trace"          in test_data, "trace"
		# 			assert "algorithm"      in test_data, "algorithm"
		# 		except Exception as e:
		# 			log_print("Fix me: field is missing:", e)
		# 			continue

		# 		# log_print("Running test %2d/%d for trace: " % (i+1, test_count), test_data["trace_name"])
		# 		log_print("%2d/%d  " % (i+1, test_count), end="")
		# 		success = run_test_for_alg_trace(test_data)
		# 		if not success:
		# 			failed += 1
		# 			success_all = False
		# 		# success_all = success_all and success
	except Exception as e:
		msg = "Exception occured: %s: %s"%(str(type(e)), str(e))
		ok = False
		success_all = False
		msg = ("[  ok]" if ok else "[FAIL]") + (" '%s'" % "test_all") + ":\t" + msg
		log_print(msg)
		raise e

	# test the results
	for tr_dict in alg_trs:
		ok, msg = validate_mistakes(tr_dict["trace"], mistakes, onto)
		if not ok:
			failed += 1
			success_all = False
		msg = ("[  ok]" if ok else "[FAIL]") + (" '%s'" % tr_dict["trace_name"]) + ":\t" + msg
		log_print(msg)

	log_print()
	log_print("="*40)
	log_print("Tests passed:", success_all)
	log_print(f"tests failed: {failed} of {test_count}.")

	return success_all


def test_make_act_line():
	import json
	with open('trace_gen/alg_test.json') as file:
		alg_data = json.load(file)

	result = make_act_json(algorithm_json=alg_data, algorithm_element_id=23,
		act_type='performed',
		# act_type='started',
		# act_type='finished',
		existing_trace_json=[],
		user_language='en',
		# user_language='ru',
		)
	result = make_act_json(algorithm_json=alg_data, algorithm_element_id=23,
		act_type='performed',
		# act_type='started',
		# act_type='finished',
		existing_trace_json=result,
		user_language='en',
		# user_language='ru',
		)
	print(result)


STYLE_HEAD = '''<style type="text/css" media="screen">
	span.algorithm {
	  font-family: courier; font-size: 10pt;
	}
	# div {
	#     border: 1px solid #000000;
	# }

	span.string { color: #555; font-style: italic }
	span.atom { color: #f08; font-style: italic; font-weight: bold; }
	span.comment { color: #262; font-style: italic; line-height: 1em; }
	span.meta { color: #555; font-style: italic; line-height: 1em; }
	span.variable { color: #700; text-decoration: underline; }
	span.variable-2 { color: #b11; }
	span.struct { color: #07c; font-weight: bold; }
	span.number { color: #f00; font-weight: bold; }
	span.program { color: #f70; font-weight: bold; }
	span.function { color: #707; font-weight: bold; }
	span.action { color: #077; font-weight: bold; }
	span.qualifier { color: #555; }
	span.keyword { color: #00a; font-weight: bold; }
	span.builtin { color: #30a; }
	span.link { color: #762; }

	span.warning { background-color: #ff9; }
	span.error { background-color: #fdd; }
	span.button { background-color: #add; }

</style>
'''

def test_algorithm_to_tags():
	import json
	with open('trace_gen/alg_test.json') as file:
		alg_data = json.load(file)

	from trace_gen.styling import algorithm_to_tags, to_html, get_button_tips

	tags = algorithm_to_tags(alg_data, 'ru')
	tips = get_button_tips()
	from pprint import pprint
	pprint(tips)

	with open('web_exp/alg_test.htm', 'w') as file:
		file.write(STYLE_HEAD)
		file.write(to_html(tags))


def test_algorithm_to_triples(inspect_questions_via_dot=False, mistakes_via_grid=False):

	print("SPECIAL MODE: algorithm_to_triples (saving questions to JSON)")

	import export2json
	import json

	files = search_text_trace_files(directory="handcrafted_traces/")

	alg_trs = parse_text_files(files)
	onto = ctrlstrct_run.create_ontology_tbox()
	questions = []
	alg_names = set()

	### [-1::]
	for alg_tr in alg_trs:
		# print(alg_tr)
		if alg_tr["algorithm_name"] in alg_names:
			# skip the same algorithms
			continue

		alg_names.add(alg_tr["algorithm_name"])
		print(" >>> ", alg_tr["algorithm_name"])

		# ctrlstrct_run.algorithm_only_to_onto(alg_tr, onto)
		q_dict = export2json.export_algtr2dict(alg_tr, onto)
		if mistakes_via_grid:
			# rewrite basic method with full tracing
			print(" >>> Griding ", alg_tr["algorithm_name"])
			q_dict["negativeLaws"] = get_question_mistakes_via_grid(alg_tr["algorithm"], skip_redundant_checks=True)  # =False is common case
		### print(q_dict)
		questions.append(q_dict)

	# skip reasoning: question data is to be solve()'d anyway
	## apply rules only for algorithm
	# onto = ctrlstrct_run.sync_jena(onto, rules_path="jena/alg_rules.ttl")


	if inspect_questions_via_dot:
		# analyze created questions
		import qs2dot
		qs2dot.lay_questions_on_graph({d["_alg_name"]:set(d["negativeLaws"]) for d in questions})

		print('SKIP saving to JSON ! 	Debugging the graph...')
		return


	with open("jena/control-flow-statements-domain-questions.json", "w") as f:
		json.dump(questions, f, indent=2)

	print('Done:', len(questions), 'questions written to JSON !')


def test_algtr_to_question_html(read_from="handcrafted_traces/one4html.txt", save_as="handcrafted_traces/one_q.html"):

	print("SPECIAL MODE: test_algtr_to_question_html (making question HTML from text)")

	from pprint import pprint
	import trace_gen.syntax as syntax

	files = [read_from]  # search_text_trace_files(directory="handcrafted_traces/")

	alg_trs = parse_text_files(files)
	alg_tr = alg_trs[0]

	syntax.set_hide_all_buttons(True)
	
	alg_data = alg_tr['algorithm']
	
	# use repair_data
	tt = TraceTester({
					"trace_name"    : 'trace_name',
					"algorithm_name": "alg_name",
					"trace"         : [],
					"algorithm"     : alg_data,
					"header_boolean_chain": None
				})
	tt.prepare_id2obj()
	del tt

	user_language = 'ru'
	user_syntax = 'C'
	algorithm_tags = syntax.algorithm_to_tags(alg_data, user_language, user_syntax)
	
	# wrap with root tag
	algorithm_tags = {
		"tag": "span",
		"attributes": {"class": ["algorithm"]},
		"content": algorithm_tags
	}
	# question_html = styling.to_html(algorithm_tags)
	
	styling.inline_class_as_style(algorithm_tags, STYLE_HEAD)
	alg_html = styling.to_html(algorithm_tags)
	
	tr_data = alg_tr['trace']
	
	question_type = None  # 'correct' or 'error'
	
	for tr_line in tr_data:
		if tr_line["comment"]:
			if not question_type:
				comment_str = tr_line["comment"]
				question_type = 'error' if comment_str.startswith(("error", "ошибк")) else 'correct'
				if question_type == "error":
					tr_line["comment"] = 'ошибка !'
					
			else:
				# erase all further comments (show first error only)
				tr_line["comment"] = ''
				
	print("guessed question_type:", question_type)
	
	tr_data = add_styling_to_trace(alg_data, tr_data, user_language, comment_style="highlight", add_tags=True)
	
	trace_html = "<br>\n".join(
		styling.to_html(styling.inline_class_as_style(a['as_tags'] , STYLE_HEAD))
		for a in tr_data
	)

	preamble = "Объясните, почему выделенное действие должно стоять в указанном месте (почему именно это действие и почему именно здесь)." if question_type == 'correct' else "Объясните, почему выделенное действие является ошибочным (почему именно это действие не должно быть в указанном месте)."
	
	trace_caption = "Трасса" if question_type == 'correct' else "Трасса с ошибками"

	question_html = "%s<br>Алгоритм:\n<br>%s\n<br><p>%s:\n<br>%s" % (preamble, alg_html, trace_caption, trace_html)
	# print(question_html)
	
	with open(save_as, "w") as f:
		f.write(question_html.strip() + "")

	print('Saved HTML to:', save_as)
	print('Done with one alg-trace pair.')


def test_grid():
	# import json
	# with open('trace_gen/alg_test.json') as file:
	# 	alg_data = json.load(file)

	files = search_text_trace_files(directory="handcrafted_traces/")
	alg_trs = parse_text_files(files)

	alg_data = alg_trs[0]['algorithm']

	steps = grid_question(alg_data, True)
	mistakes_set = {m for step in steps for m in step['mistakes']}
	print("mistakes_set:", mistakes_set)



if __name__ == '__main__':

	if 0:
		test_algtr_to_question_html()
		###
		exit()
		###

	if 0:
		test_grid()
		###
		print()
		print('Exit as in custom debug mode.')
		exit()
		###

	if 0:
		# test_make_act_line()
		# test_algorithm_to_tags()
		test_algorithm_to_triples(inspect_questions_via_dot=0, mistakes_via_grid=0)
		###
		print()
		print('Exit as in custom debug mode.')
		exit()
		###

	success_all = run_tests(process_kwargs=dict(
		# reasoning=None,
		# reasoning="pellet",
		# reasoning="clingo",
		# reasoning="dlv",
		reasoning="jena",
		# reasoning="prolog",
		# reasoning="sparql",
		# reasoning="stardog",
		extra_act_entries=0
		)
	)

	# save LOG
	fpath = os.path.join(TEST_DIR, REPORT_FNM)
	with open(fpath, "w", encoding="utf8") as f:
		f.write("\n".join(LOG))

	# indicate tests success with exit code
	exit(0 if success_all else 1)
