# external_run.py

import re
import subprocess
import time
import timeit
from timeit import default_timer as timer

# $ pip install psutil
import psutil


# MEASURE_TIME = True
MEASURE_TIME = False

# 0 is normal mode, ex. 5 means repeat 5 times and report
REPEAT_COUNT = 1  # this is required for stats measurements
# REPEAT_COUNT = 0

MIN_WALL_TIME = None
MIN_EXCLUSIVE_TIME = None
OUTPUT_TYPE = None
OUTPUT_TIME_LIST = []  # exclusive reasoning time measured by the reasoner process itself
PROC_STAT_LIST = []  # measurements of CPU and memory usage
REASONING_STAT_DICT = {}  # triples_before triples_after iterations (for prolog,sparql modes)

SHOW_PRINTOUT = False

_WATCHING_THREAD = None

def set_repeat_count(count: int):
	'Set REPEAT_COUNT globally for the module'
	global REPEAT_COUNT
	REPEAT_COUNT = count

def get_run_stats():
	stats_dict = PROC_STAT_LIST[0] if PROC_STAT_LIST else {}
	stats_dict.update({
		"wall_time": MIN_WALL_TIME,
		"exclusive_time": MIN_EXCLUSIVE_TIME,
		})
	stats_dict.update(REASONING_STAT_DICT)
	### print(stats_dict)
	return stats_dict


def ext_stdout_handler(stdout, stderr):
	if isinstance(stdout, bytes):
		stdout = stdout.decode('utf8')
		# print(stdout)
	if isinstance(stderr, bytes):
		stderr = stderr.decode('utf8')
		# print(stderr)
		
	REASONING_STAT_DICT.clear()
		
	if OUTPUT_TYPE == 'prolog':
		# m_0 = re.search(r"Loading the ontology took (\d+) ms\.", stdout)  # reasoning started
		m = re.search(r"Time it took: (\d+) ms\.", stdout)  # reasoning time
		if m:
			dur_s = int(m[1]) / 1000
			OUTPUT_TIME_LIST.append(dur_s)
		else:
			print("An error occured examiming the output of Prolog...")
		ms = re.findall(r"\d+(?=\striples)", stdout)  # triples count
		if ms:
			REASONING_STAT_DICT["triples_before"] = int(ms[0])
			REASONING_STAT_DICT["triples_after"] = int(ms[-1])
		m = re.search(r"\d+(?=\siterations)", stdout)  # iterations count
		if m:
			REASONING_STAT_DICT["iterations"] = int(m[0])
			
	elif OUTPUT_TYPE in ('jena', 'sparql'):
		m = re.search(r"Time spent on reasoning: ([\d.]+) seconds\.", stdout)  # reasoning started
		if m:
			dur_s = float(m[1])
			OUTPUT_TIME_LIST.append(dur_s)
		else:
			print("An error occured examiming the output of Jena/Sparql...")
		# Starting reasoning from NTriples: 99
		ms = re.findall(r"(?<=NTriples:\s)\d+", stdout)  # triples count
		if ms:
			REASONING_STAT_DICT["triples_before"] = int(ms[0])
			REASONING_STAT_DICT["triples_after"] = int(ms[-1])
		ms = re.findall(r"(?<=Iteration:\s)\d+", stdout)  # iterations count
		if ms:
			REASONING_STAT_DICT["iterations"] = int(ms[-1])
			
	elif SHOW_PRINTOUT:
		print('The printout of the process (%s):' % OUTPUT_TYPE)
		print(stdout)
		print(stderr)


def run_cmd(cmd, measure_time=MEASURE_TIME, repeat_count=REPEAT_COUNT, verbose=False) -> int:
	global PROC_STAT_LIST
	global MIN_WALL_TIME
	global MIN_EXCLUSIVE_TIME
	global SHOW_PRINTOUT
	
	if verbose:
		print(">_ running cmd:", cmd)
		
	SHOW_PRINTOUT = verbose
		
	if repeat_count is not None and repeat_count > 0:
		
		OUTPUT_TIME_LIST.clear()
		PROC_STAT_LIST.clear()
		
		time_list = timeit.repeat(stmt=f"invoke_shell('{cmd}', True, 'run once ...')",
			repeat=repeat_count, number=1, globals=globals())
		print(">_ cmd finished.")
		
		MIN_WALL_TIME =  min(time_list) if time_list else 999999
		time_report = "     Wall time measured for %d runs: %s (min: %.3f s.)." % (repeat_count, repr(time_list), MIN_WALL_TIME)
		print(time_report)
		
		MIN_EXCLUSIVE_TIME =  min(OUTPUT_TIME_LIST) if OUTPUT_TIME_LIST else 999999
		time_report = "Exclusive time measured for %d runs: %s (min: %.3f s.)." % (len(OUTPUT_TIME_LIST), repr(OUTPUT_TIME_LIST), MIN_EXCLUSIVE_TIME)
		print(time_report)
		
		# summarize the results of several runs
		PROC_STAT_LIST = [summarize_process_stat(PROC_STAT_LIST)]

		
		exitcode = 0
		
	else:  # Normal run once
		global OUTPUT_TYPE; OUTPUT_TYPE = None
		if measure_time:
			start = timer()
		# process = subprocess.Popen(cmd, stdout=stdout, creationflags=0x08000000)
		exitcode = invoke_shell(cmd)
		if measure_time:
			end = timer()
			time_report = "   Time elapsed: %.3f s." % (end - start)
	
		if verbose:
			print(">_ cmd finished with code", exitcode)
		if measure_time:
			print(time_report)
		
	return exitcode

	
def invoke_shell(cmd, gather_stats=False, *args, output_handler=ext_stdout_handler):
	if args:
		print(*args)
	# process = subprocess.Popen(cmd, stdout=stdout, stderr=stdout, creationflags=0x08000000)
	# process = psutil.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000)
	process = psutil.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	
	stdout_accumulator = ''
	# printout = process.communicate()
	# print("printout-1:", printout)
	if gather_stats:
		stat_list = []
		interval = 0.1
		time = 0
		stat = True
		while stat:
			stat = cpu_mem(process, interval)  # blocks over 'interval' seconds
			if stat:
				stat_list.append(stat)
			stdout_accumulator += process.stdout.read()  # prevent buffer owerflow
				
		PROC_STAT_LIST.append(summarize_process_stat(stat_list))
	
	stdout, stderr = process.communicate()
	output_handler(stdout_accumulator + stdout, stderr)
	# process.wait()
	return process.returncode


def cpu_mem(p: psutil.Process, interval=0.1):
    metrics = {}
    try:
        with p.oneshot():
    #         if p.status() == psutil.STATUS_RUNNING:
            metrics["cpu"] = p.cpu_percent(interval=interval)
            mem = p.memory_full_info()
            metrics["rss"] = mem.rss  # alias for wset
            metrics["vms"] = mem.vms  # alias for pagefile
            metrics["uss"] = mem.uss
            metrics["rss_peak"] = mem.peak_wset
            metrics["vms_peak"] = mem.peak_pagefile
    except psutil.NoSuchProcess: pass
    except psutil.AccessDenied: pass
    return metrics

    
def summarize_process_stat(stat_list: list) -> dict:
	'find average CPU and max memory from list of samples'
	cpu = [metrics["cpu"] for metrics in stat_list if "cpu" in metrics]
	cpu = sum(cpu) / len(cpu) if cpu else 0.0
	
	rss = [metrics["rss"] for metrics in stat_list if "rss" in metrics]
	if stat_list and "rss_peak" in stat_list[-1]:
		rss.append(stat_list[-1]["rss_peak"])
	rss = max(rss) if rss else 0.0
	
	vms = [metrics["vms"] for metrics in stat_list if "vms" in metrics]
	if stat_list and "vms_peak" in stat_list[-1]:
		vms.append(stat_list[-1]["vms_peak"])
	vms = max(vms) if vms else 0.0
	
	uss = [metrics["uss"] for metrics in stat_list if "uss" in metrics]
	uss = max(uss) if uss else 0.0
	
	return {
		"cpu": cpu,
		"rss": rss,
		"vms": vms,
		"uss": uss,
	}
		
		
# from threading import Thread
import threading

def gather_clingo_stats(max_wait=3):
	chooser = lambda process: process.name() == 'clingo.exe' and 'win' in process.exe()
	return gather_process_stats(process_attributes=('name', 'exe'), chooser_func=chooser, label="Clingo process", max_wait=max_wait)

def gather_dlv_stats(max_wait=3):
	chooser = lambda process: process.name() == 'dlv.mingw.exe'
	return gather_process_stats(chooser_func=chooser, label="DLV process", max_wait=max_wait)

def gather_pellet_stats(max_wait=3):
	chooser = lambda process: process.name() == 'java.exe' and 'pellet.Pellet' in process.cmdline()
	return gather_process_stats(['name', 'cmdline'], chooser, "Pellet process", max_wait)

def gather_process_stats(process_attributes=('name', ), chooser_func=None, label='Process', max_wait=3):
	# print('Tread Start!')
	# search for <java> process running <Pellet> that should start soon
	elapsed = 0
	while elapsed < max_wait:
		processes = []  # several processes can possibly be found
		try:
			for process in psutil.process_iter(process_attributes):
				if chooser_func(process):
					# break
					processes.append(process)
					# print(f'Found {label}! pid:', process.pid)
			if not processes:
				time.sleep(0.1)
				elapsed += 0.1
				continue
		except psutil.Error:
			print(f'failed searching for the {label}...')
			return 'failed to read process data...'
		break  # found!
	else:
		# still not found
		print(f"{label} has not been detected during %.1f seconds!" % max_wait)
		return 'failed to detect process...'
		
	# print(f'Found {label}! pid:', process.pid)
	stat_list = []
	interval = 0.1
	# stat = True
	while True:
		# stat = cpu_mem(process, interval)  # blocks over 'interval' seconds
		# if stat:
		# 	stat_list.append(stat)
		# else:
		# 	break
		stat = [cpu_mem(process, interval) for process in processes]
		if any(stat):
			stat_list.append(summarize_process_stat(list(filter(None, stat))))
		else:
			# print(f"{label} has finished.")
			break
	# print(stat_list)
	PROC_STAT_LIST.append(summarize_process_stat(stat_list))
	
	return 'success'


def measure_stats_for_process_running(max_wait=3, target=None, args=()):	
	PROC_STAT_LIST.clear()
	REASONING_STAT_DICT.clear()

	global _WATCHING_THREAD
	
	_WATCHING_THREAD = threading.Thread(target=target, args=args)  # pass max_wait ?
	_WATCHING_THREAD.start()
	
	return 'wait and call get_process_run_stats()'


def measure_stats_for_pellet_running(max_wait=3):
	# '''java -Xmx2000M -cp C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\antlr-3.2.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\antlr-runtime-3.2.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\aterm-java-1.6.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\commons-codec-1.6.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\httpclient-4.2.3.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\httpcore-4.2.2.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jcl-over-slf4j-1.6.4.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-arq-2.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-core-2.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-iri-0.9.5.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-tdb-0.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jgrapht-jdk1.5.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\log4j-1.2.16.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\owlapi-distribution-3.4.3-bin.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\pellet-2.3.1.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\slf4j-api-1.6.4.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\slf4j-log4j12-1.6.4.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\xercesImpl-2.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\xml-apis-1.4.01.jar pellet.Pellet realize --loader Jena --input-format N-Triples --infer-prop-values --infer-data-prop-values --ignore-imports {path}'''
	
	return measure_stats_for_process_running(max_wait, target=gather_pellet_stats)

	
def measure_stats_for_clingo_running(max_wait=3):
	'Complete copy of measure_stats_for_pellet_running() function but target function'
	return measure_stats_for_process_running(max_wait, target=gather_clingo_stats)

def measure_stats_for_dlv_running(max_wait=3):
	'Complete copy of measure_stats_for_pellet_running() function but target function'
	return measure_stats_for_process_running(max_wait, target=gather_dlv_stats)

	

def get_process_run_stats():
	global _WATCHING_THREAD
	if _WATCHING_THREAD:
		_WATCHING_THREAD.join()  # wait
		# _WATCHING_THREAD.terminate()
		_WATCHING_THREAD = None
	stats = get_run_stats()
	# print('After Pellet run:', stats)
	del stats['wall_time']
	del stats['exclusive_time']
	return stats
	

def run_swiprolog_reasoning(rdf_path_in:str, rdf_path_out:str, verbose=True, command_name="run_ontology"):
	# C:\D\Work\YDev\CompPr\c_owl>swipl -s run_ontology "test_data/test_make_trace_output.rdf" "test_data/prolog_output.rdf"
	global OUTPUT_TYPE; OUTPUT_TYPE = 'prolog'
	cmd = f'swipl -s {command_name} "{rdf_path_in}" "{rdf_path_out}"'
	# if verbose: print(">_ running cmd:", cmd)
	run_cmd(cmd, verbose=verbose)
	# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
	# process.wait()
	# exitcode = process.returncode
	# if verbose: print(">_ cmd finished with code", exitcode)
	return get_run_stats()


def run_jena_reasoning(rdf_path_in:str, rdf_path_out:str, reasoning_mode='jena', verbose=True, rules_path=None):
	# java -jar Jena.jar jena "test_data/test_make_trace_output.rdf" "jena/all.rules" "test_data/jena_output.rdf"
	# How to specify working directory:
	# subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')
	
	if reasoning_mode not in ('sparql', 'jena'):
		print(' Warning: Unknown reasoning mode:', reasoning_mode)
		reasoning_mode = 'jena'
		print(' Defaulting to mode:', reasoning_mode)
	
	global OUTPUT_TYPE; OUTPUT_TYPE = reasoning_mode
	
	if not rules_path:
		rules_path = {  # set defaults
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
	return get_run_stats()
	

	
