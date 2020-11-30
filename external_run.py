# external_run.py

import sys
import subprocess
import timeit
from timeit import default_timer as timer


MEASURE_TIME = 1
REPEAT_COUNT = 1  # 1 is normal mode, ex. 5 mean repeat 5 times and report

def run_cmd(cmd, measure_time=MEASURE_TIME, repeat_count=REPEAT_COUNT, verbose=False) -> int:
	if verbose:
		print(">_ running cmd:", cmd)
		
	if verbose:
		# stdout=subprocess.PIPE
		stdout=sys.stdout
	else:
		stdout=None
		
	if repeat_count is not None and repeat_count > 1:
		time_list = timeit.repeat(stmt=f"invoke_shell('{cmd}', {None}, 'run once ...')",
			repeat=repeat_count, number=1, globals=globals())
		print(">_ cmd finished.")
		time_report = "   Time measured for %d runs: %s (min: %.3f s.)." % (repeat_count, repr(time_list), min(time_list))
		print(time_report)
		exitcode = 0
		
	else:  # Normal run once
		if measure_time:
			start = timer()
		# process = subprocess.Popen(cmd, stdout=stdout, creationflags=0x08000000)
		exitcode = invoke_shell(cmd, stdout)
		if measure_time:
			end = timer()
			time_report = "   Time elapsed: %.3f s." % (end - start)
	
		if verbose:
			print(">_ cmd finished with code", exitcode)
		if measure_time:
			print(time_report)
		
	return exitcode

	
def invoke_shell(cmd, stdout, *args):
	if args:
		print(*args)
	process = subprocess.Popen(cmd, stdout=stdout, stderr=stdout, creationflags=0x08000000)
	process.wait()
	return process.returncode
	

def run_swiprolog_reasoning(rdf_path_in:str, rdf_path_out:str, verbose=True):
	# C:\D\Work\YDev\CompPr\c_owl>swipl -s run_ontology "test_data/test_make_trace_output.rdf" "test_data/prolog_output.rdf"
	cmd = f'swipl -s run_ontology "{rdf_path_in}" "{rdf_path_out}"'
	# if verbose: print(">_ running cmd:", cmd)
	run_cmd(cmd, verbose=verbose)
	# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
	# process.wait()
	# exitcode = process.returncode
	# if verbose: print(">_ cmd finished with code", exitcode)


def run_jena_reasoning(rdf_path_in:str, rdf_path_out:str, reasoning_mode='jena', verbose=True):
	# java -jar Jena.jar "test_data/test_make_trace_output.rdf" "jena/all.rules" "test_data/jena_output.rdf"
	# How to specify working directory:
	# subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')
	
	if reasoning_mode not in ('sparql', 'jena'):
		print(' Warning: Unknown reasoning mode:', reasoning_mode)
		reasoning_mode = 'jena'
		print(' Defaulting to mode:', reasoning_mode)
	
	rules_path = {
		'jena': "jena/all.rules",
		'sparql': "sparql_from_swrl.ru", 
	}[reasoning_mode]
	
	cmd = f'java -jar jena/Jena.jar {reasoning_mode} "{rdf_path_in}" "{rules_path}" "{rdf_path_out}"'
	run_cmd(cmd, verbose=verbose)
	# if verbose: print(">_ running cmd:", cmd)
	# process = subprocess.Popen(cmd, creationflags=0x08000000)
	# process.wait()
	# exitcode = process.returncode
	# if verbose: print(">_ cmd finished with exit code", exitcode)
	

	
