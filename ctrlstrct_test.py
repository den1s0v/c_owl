# ctrlstrct_test.py

"""
Тестирование получения ошибок из онтологии на имеющихся алгоритмах и трассах

"""

import json
import os

from ctrlstrct_run import process_algtr


TEST_DIR = "./test_data"
OUTPUT_FNM = "output.json"
RUN_REPORT_FNM = "run_report.txt"
TESTS_FNM = "tests.json"

ALG_FILE_FIELD = "alg_input"
TRACE_FILE_FIELD = "trace_input"
REFERENCE_DATA_FIELD = "reference_output"


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
				# Запуск !	
				_, mistakes = process_algtr(alg, tr, verbose=0)
			except Exception as e:
				msg = "Exception occured: %s: %s"%(str(type(e)), str(e))
				msg = ("  ok" if False else "FAIL") + (" [%s]" % test_name) + "\t:" + msg
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
			msg = ("  ok" if ok else "FAIL") + (" [%s]" % test_name) + "\t:" + msg
			print(msg)
			# 	run_report = {"succeded": 0, "failed": 0, "messages":[]}
			run_report["succeded" if ok else "failed"] += 1
			run_report["messages"].append(msg)
			
		
		fpath = os.path.join(directory, OUTPUT_FNM)
		with open(fpath, "w", encoding="utf8") as f:
			json.dump(output_data, f, indent=2)
	
		fpath = os.path.join(directory, RUN_REPORT_FNM)
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


if __name__ == '__main__':
	
	success_all = True
	
	for directory,subdirs,files in os.walk(TEST_DIR):
		if TESTS_FNM in files:
			print("Running tests in: ", directory)
			success = run_tests_in_directory(directory)
			success_all = success_all and success
			print("Tests passed:", success, " in directory: ", directory)
			
		# break
		
	# indicate tests success with exit code
	exit(0 if success_all else 1)
