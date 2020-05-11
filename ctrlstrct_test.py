# ctrlstrct_test.py

"""
Тестирование получения ошибок из онтологии на имеющихся алгоритмах и трассах

"""

import json
import os

from ctrlstrct_run import process_algtr
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

def run_tests_in_directory(directory) -> bool:
	
	tests_fpath = os.path.join(directory, TESTS_FNM)
	assert os.path.exists(tests_fpath), tests_fpath
	with open(tests_fpath, encoding="utf8") as f:
		tests_data = json.load(f)
		
	output_data = {}
	run_report = {"succeded": 0, "failed": 0, "skipped": 0, "messages":[]}
		
	# iterate over the tests
	for test_name in tests_data:
		if test_name.startswith("-"):
			output_data[test_name] = " == SKIPPED == "
			run_report["skipped"] += 1
		else:
			print("Running test:", "[%s]"%test_name)
			test_data = tests_data[test_name]
			
			fpath = resolve_path(test_data[ALG_FILE_FIELD], directory)
			assert fpath, test_data[ALG_FILE_FIELD] + " not found ..."
			with open(fpath, encoding="utf8") as f:
				alg = f.read()

			fpath = resolve_path(test_data[TRACE_FILE_FIELD], directory)
			assert fpath, test_data[TRACE_FILE_FIELD] + " not found ..."
			with open(fpath, encoding="utf8") as f:
				tr = f.read()
	
			
			try:
				if SAVE_RDF:
					ontology_file = test_name + "_output.rdf"
					ontology_fpath = os.path.join(directory, ontology_file)
					# onto.save(file=fpath, format='rdfxml')
					# print("Saved RDF file: {} !".format(ontology_file))
				else:
					ontology_fpath = None

				# Запуск !	
				onto, mistakes = process_algtr(alg, tr, verbose=0, debug_rdf_fpath=ontology_fpath)
				
			except Exception as e:
				msg = "Exception occured: %s: %s"%(str(type(e)), str(e))
				ok = False
				msg = ("[  ok]" if ok else "[FAIL]") + (" '%s'" % test_name) + ":\t" + msg
				print(msg)
				output_data[test_name] = msg
				run_report["messages"].append(msg)
				run_report["failed"] += 1
				continue
			
			# записывать больше?
			output_data[test_name] = mistakes
				
			# сравнить результат и эталон
			# ...
			ok, msg = compare_mistakes(test_data[REFERENCE_DATA_FIELD], mistakes)
			msg = ("[  ok]" if ok else "[FAIL]") + (" '%s'" % test_name) + "\t:" + msg
			print(msg)
			# 	run_report = {"succeded": 0, "failed": 0, "messages":[]}
			run_report["succeded" if ok else "failed"] += 1
			run_report["messages"].append(msg)
			
		
		fpath = os.path.join(directory, OUTPUT_FNM)
		with open(fpath, "w", encoding="utf8") as f:
			json.dump(output_data, f, indent=2)
	
		fpath = os.path.join(directory, REPORT_FNM)
		with open(fpath, "w", encoding="utf8") as f:
			f.write("\n".join(run_report["messages"]))
			f.write("\n=============\n")
			f.write("succeded: %d, failed: %d, total: %d.\n(skipped: %d)\n" % (run_report["succeded"], run_report["failed"], run_report["succeded"]+run_report["failed"], run_report["skipped"]))
			
	return run_report["failed"] == 0
	

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

def run_test_for_alg_trace(test_data: dict, directory=TEST_DIR):
	
	alg = test_data["algorithm"]
	tr  = test_data["trace"]
	test_name  = test_data["trace_name"]
	
	try:
		if SAVE_RDF:
			ontology_file = test_name + "_output.rdf"
			ontology_fpath = os.path.join(directory, ontology_file)
			# onto.save(file=fpath, format='rdfxml')
			# print("Saved RDF file: {} !".format(ontology_file))
		else:
			ontology_fpath = None

		# Запуск !	
		onto, mistakes = process_algtr(alg, tr, verbose=0, debug_rdf_fpath=ontology_fpath, mistakes_as_objects=True)
		
	except Exception as e:
		msg = "Exception occured: %s: %s"%(str(type(e)), str(e))
		ok = False
		msg = ("[  ok]" if ok else "[FAIL]") + (" '%s'" % test_name) + ":\t" + msg
		log_print(msg)
		
		# debug only:
		# raise e
		
		return False

	# сравнить результат и эталон
	# ...
	ok, msg = validate_mistakes(tr, mistakes, onto)
	msg = ("[  ok]" if ok else "[FAIL]") + (" '%s'" % test_name) + ":\t" + msg
	log_print(msg)
	
	return ok


def validate_mistakes(trace:list, mistakes:list, onto) -> (bool, str):
	"Находит расхождения в определении ошибочных строк трассы"
	
	def is_error_act(d:dict):
		comment = d["comment"]
		return ("error" in comment or "ошибка" in comment)
	
	error_flags = {d["text_line"]:is_error_act(d) for d in trace}
	
	arg_objs = []
	
	for prop_name in ("arg", ):  # добавить поля, если они появятся в спецификации ошибки
		arg_dicts = (find_by_key_in(prop_name, mistakes))  # список словарей с ключами 'arg', по которым хранятся списки объектов онтологии
		for dct in arg_dicts:
			arg_objs += dct[prop_name]
			
	if arg_objs:
		onto = arg_objs[0].namespace
		prop_text_line = onto["text_line"]
	
	inferred_error_lines = []
	for arg_obj in arg_objs:
		text_line = get_relation_object(arg_obj, prop_text_line)
		inferred_error_lines.append(text_line)
		
	# проверка
	differences = []
	first_err_line = None  # из размеченных комментариями в трассе
	for i,is_err in error_flags.items():
		if is_err:
			if first_err_line is None:
				first_err_line = i
			if i not in inferred_error_lines:
				m = f"Erroneous line {i} hasn't been recognized by the ontology."
				differences.append(m)
			# break ?
		elif i in inferred_error_lines and first_err_line is None:  # вслед за первой ошибочной может быть всё что угодно
			m = f"Correct line {i} has been recognized by the ontology as erroneous."
			differences.append(m)
			# break
				
	if differences:
		return False, "\n\t> ".join(["",*differences])
	return True, "Validation ok."


def run_tests():
	
	files = search_text_trace_files(directory="handcrafted_traces/")
	
	### Отладочная заглушка !
	files = [f for f in files if "example" in f]
	# files = [f for f in files if "correct_branching" in f]
	
	alg_trs = parse_text_files(files)
	
	### Отладочная заглушка !
	alg_trs = alg_trs[1:2]
	
	test_count = len(alg_trs)
	
	success_all = True
	failed = 0
	
	for i, test_data in enumerate(alg_trs):
		try:
			assert "trace_name"     in test_data, "trace_name"
			assert "algorithm_name" in test_data, "algorithm_name"
			assert "trace"          in test_data, "trace"         
			assert "algorithm"      in test_data, "algorithm"     
		except Exception as e:
			log_print("Fix me: field is missing:", e)
			continue
		
		# log_print("Running test %2d/%d for trace: " % (i+1, test_count), test_data["trace_name"])
		log_print("%2d/%d  " % (i+1, test_count), end="")
		success = run_test_for_alg_trace(test_data)
		if not success:
			failed += 1
			success_all = False
		# success_all = success_all and success
			
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
	success_all = run_tests()
	
	# save LOG
	fpath = os.path.join(TEST_DIR, REPORT_FNM)
	with open(fpath, "w", encoding="utf8") as f:
		f.write("\n".join(LOG))
		
	# indicate tests success with exit code
	exit(0 if success_all else 1)
