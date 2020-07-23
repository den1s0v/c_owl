# encoding: utf-8
# ctrlstrct_test.py

"""
Тестирование получения ошибок из онтологии на имеющихся алгоритмах и трассах

"""

# import json
import os
import re

from ctrlstrct_run import process_algtr, process_algtraces
from trace_gen.txt2algntr import parse_text_files, search_text_trace_files, find_by_key_in
from upd_onto import get_relation_object


TEST_DIR = "./test_data"
OUTPUT_FNM = "output.json"
REPORT_FNM = "run_report.txt"
TESTS_FNM = "tests.json"

ALG_FILE_FIELD = "alg_input"
TRACE_FILE_FIELD = "trace_input"
REFERENCE_DATA_FIELD = "reference_output"

SAVE_RDF = True

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
		if "error" in comment_str or "ошибка" in comment_str:
			# ex. "error: AllFalseNoElse (Нет ветки ИНАЧЕ)"
			m = re.search(r"(?:ошибка|error)\s*:?\s*([^()]*)\s*(?:\(.+\).*)?$", comment_str, re.I)
			if m:
				err_names = m.group(1).strip()
				return re.split(r"\s,?\s+", err_names)
		return None
	
	text_lines = [d["text_line"] for d in trace]
	error_descrs = {d["text_line"]: error_description(d["comment"]) for d in trace}
	
	# extract erroneous acts and messages from error instances (inferred)
	err_objs = []
	err_obj_id2msgs = {}
	
	# retrieve property object(s)
	prop_text_line = onto["text_line"]
	# prop_message = onto["message"]

	for prop_name in ("cause", ):  # добавить поля, если они появятся в спецификации ошибки
		tr_obj_dicts = list(find_by_key_in(prop_name, mistakes))  # список ошибок с ключами 'cause', по которым хранятся списки объектов онтологии
		
		for dct in tr_obj_dicts:
			for err_obj in dct[prop_name]:
				if (err_obj.text_line) in text_lines:  # ignore unrelated errors (possibly related to another trace)
					err_objs.append(err_obj)
					err_obj_id2msgs[id(err_obj)] = dct["message"]
			
	
	# get text lines of the inferred erroneous acts
	inferred_error_lines = [
		get_relation_object(err_obj, prop_text_line)
		for err_obj in err_objs
	]
		
	# do check
	differences = []
	
	def _compare_mistakes(expected: list, inferred: list, line_i) -> str or None:
		if not expected and not inferred:
			return None
		
		if expected and not inferred:
			return f"Erroneous line {line_i} hasn't been recognized by the ontology. Expected mistakes: {', '.join(expected)}"
			
		if not expected and inferred:
			return f"Correct line {line_i} has been recognized by the ontology as erroneous. Inferred mistakes: {', '.join(inferred)}"
			
		(not_recognised, extra) = ([], inferred[:])
		for err_word in expected:
			for inferred_descr in extra[:]:
				if err_word and err_word.lower() in inferred_descr.lower():
					extra.remove(inferred_descr)
					break
			else:
				not_recognised.append(err_word)
		
		if not not_recognised and not extra:
			return None
		
		m = f"Erroneous line {line_i} has been recognized by the ontology partially only. Expected but not recognised - ({len(not_recognised)}) {', '.join(not_recognised)}. Inferred but not expected - ({len(extra)}) {', '.join(extra)}."
		return m
			
				
	# first_err_line = None  # из размеченных комментариями в трассе
	for line_i, err_descr in error_descrs.items():
		
		# gather all inferred mistakes
		inferred_messages = []
		if line_i in inferred_error_lines:
			for inferred_line_i, err_obj in zip(inferred_error_lines, err_objs):
				if line_i == inferred_line_i:
					inferred_messages.extend(err_obj_id2msgs[id(err_obj)])
		
		m = _compare_mistakes(err_descr, inferred_messages, line_i)
		if m:
			differences.append(m)
				
	if differences:
		return False, "\n\t> ".join(["",*differences])
	return True, "Validation ok."


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
			onto, mistakes = process_algtraces(alg_trs, verbose=0, debug_rdf_fpath=ontology_fpath, mistakes_as_objects=True, **process_kwargs)
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


if __name__ == '__main__':
	
	success_all = True
	
	# for directory,subdirs,files in os.walk(TEST_DIR):
	# 	if TESTS_FNM in files:
	# 		print("Running tests in: ", directory)
	# 		success = run_tests_in_directory(directory)
	# 		success_all = success_all and success
	# 		print("Tests passed:", success, " in directory: ", directory)
			
	# 	# break
	success_all = run_tests(process_kwargs=dict(
		reasoning=None, 
		# reasoning="stardog", 
		# reasoning="pellet", 
		extra_act_entries=1
		)
	)
	
	# save LOG
	fpath = os.path.join(TEST_DIR, REPORT_FNM)
	with open(fpath, "w", encoding="utf8") as f:
		f.write("\n".join(LOG))
		
	# indicate tests success with exit code
	exit(0 if success_all else 1)
