# encoding: utf-8
# ctrlstrct_test.py

"""
Тестирование получения ошибок из онтологии на имеющихся алгоритмах и трассах

"""

# import json
import os
import re

from ctrlstrct_run import process_algtraces
from trace_gen.txt2algntr import parse_text_files, parse_algorithms_and_traces_from_text, search_text_trace_files, find_by_key_in, find_by_keyval_in
from trace_gen.json2alg2tr import act_line_for_alg_element
from upd_onto import get_relation_object
import trace_gen.styling as styling


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
			# For input str "error: AllFalseNoElse, TooEarly (Нет ветки ИНАЧЕ)"
			# the result will be ['AllFalseNoElse', 'TooEarly']
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
	Returns list of dicts, each dict represents act object; usually list is 1 in length, but gets two elements if given trace is empty - put begin of trace and requested act.
	(Returns string with error description if an exception occured)
	'''
	existing_trace_list = existing_trace_json
	try:
		elem = algorithm_json["id2obj"].get(str(algorithm_element_id), None)
		
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
				'as_tags': html_tags,
				'as_html': styling.to_html(html_tags),
				'id': max_id,
				'n': 1,
				'is_valid': True  # в начале трассы акт всегда такой
				})
		
		exec_time = 1 + len([a for a in existing_trace_list if a['executes'] == algorithm_element_id and a['phase'] == act_type])
		
		expr_value = None
		if elem['type'] == "expr" and act_type in ('finished', 'performed'):
			name = elem['name']
			expr_list = algorithm_json['expr_values'].get(name, None)
			
			assert expr_list is not None, f"No expression values provided for expression '{name}' in given algorithm."
			assert len(expr_list) >= exec_time, f"Not enough expression values provided for expression '{name}': {len(expr_list)} provided, {exec_time} requested."
			
			expr_value = expr_list[exec_time - 1]
		
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
				'as_tags': html_tags,
				'as_html': styling.to_html(html_tags),
				'id': max_id,
				'n': exec_time,
				'is_valid': None,  # пока нет информации о корректности такого акта
				# 'is_valid': True,  # !!
		}
		if expr_value is not None:
			act_json['value'] = expr_value
			
		result_acts.append(act_json)
		
		# print(result_acts)
		return result_acts
	except Exception as e:
		# raise e
		return f"Server error in make_act_json() - {type(e).__name__}:\n\t{str(e)}"


def add_styling_to_trace(algorithm_json, trace_json, user_language=None) -> list:
	'''Adds text line, tags and html form for each act in given trace and returns the same reference to the trace list'''
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
				use_exec_time=act_dict['n'],
				)
			html_tags = styling.prepare_tags_for_line(act_text)
			add_json = {
					'as_string': act_text,
					'as_tags': html_tags,
					'as_html': styling.to_html(html_tags),
			}
			act_dict.update(add_json)
	
		return trace_json
	except Exception as e:
		# raise e
		return f"Server error in add_styling_to_trace() - {type(e).__name__}:\n\t{str(e)}"


def process_algorithms_and_traces(alg_trs_list: list, write_mistakes_to_acts=False, process_kwargs=dict(reasoning="jena", debug_rdf_fpath='test_data/ajax.rdf')) -> ('mistakes', 'error_message: str or None'):
		
	try:
		_onto, mistakes = process_algtraces(alg_trs_list, verbose=0, mistakes_as_objects=False, **process_kwargs)
		
		# from pprint import pprint
		# pprint(mistakes)
		
		if write_mistakes_to_acts and len(alg_trs_list) == 1:
			trace = alg_trs_list[0]['trace']
			for mistake in mistakes:
				act_id = mistake["id"][0]
				for act_obj in find_by_keyval_in("id", act_id, trace):
					act_obj["explanations"] = act_obj.get("explanations", []) + mistake["explanations"]
					if not act_obj["explanations"]:  # был пустой список - запишем хоть что-то
						act_obj["explanations"] = ["Ошибка обнаружена, но вид ошибки не определён."]
					act_obj["is_valid"] = False
					break
					
			# Apply correctness mark to other acts:  act_obj["is_valid"] = True
			for act_obj in trace:
				if act_obj["is_valid"] is None:
					act_obj["is_valid"] = True
			
		return mistakes, None
	except Exception as e:
		msg = "Exception occured in process_algorithms_and_traces(): %s: %s"%(str(type(e)), str(e))
		raise e
		print(msg)
		return [], msg


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
				onto, mistakes = process_algtraces(alg_trs, verbose=0, debug_rdf_fpath=ontology_fpath, mistakes_as_objects=True, **process_kwargs)
			else:
				dataset = os.path.splitext(os.path.split(files[0])[1])[0]
				eval_results = []
				# 46
				for n in sorted({
									*range(1, 10 + 1, 1),
									*range(5, 100 + 1, 5),
									*range(100, 201 + 1, 10),
									# *range(90, 131 + 1, 10),
									# *range(30, 60 + 1, 10),
									# *range(65, 95 + 1, 5),
								}):
					# reasoners = ("pellet", )
					# reasoners = ("prolog", ); alg_trs = alg_trs[:22]  # !!!
					# reasoners = ("sparql", )
					# reasoners = ("jena", )
					reasoners = ("clingo", )
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
	body {
	  font-family: courier; font-size: 10pt;
	}
	# div {
	#     border: 1px solid #000000;
	# }

	span.string, span.atom { color: #f08; font-style: italic; font-weight: bold; }
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
	
	

if __name__ == '__main__':

	if 0:
		# test_make_act_line()
		test_algorithm_to_tags()
		###
		print()
		print('Exit as in custom debug mode.')
		exit()
		###
	
	success_all = run_tests(process_kwargs=dict(
		# reasoning=None, 
		# reasoning="pellet", 
		# reasoning="clingo", 
		reasoning="dlv", 
		# reasoning="jena", 
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
