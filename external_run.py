# external_run.py

import re
import subprocess
import sys
import time
import timeit
from timeit import default_timer as timer

# $ pip install psutil
import psutil


MEASURE_TIME = True
REPEAT_COUNT = 1  # 0 is normal mode, ex. 5 mean repeat 5 times and report

# OUT_STREAM = io.StringIO()
# OUT_STREAM.getvalue()  # retrieve the data written to stream

MIN_WALL_TIME = None
MIN_EXCLUSIVE_TIME = None
OUTPUT_TYPE = None
OUTPUT_TIME_LIST = []  # exclusive reasoning time measured by the reasoner process itself
PROC_STAT_LIST = []  # measurements of CPU and memory usage

SHOW_PRINTOUT = False

_WATCHING_THREAD = None

def set_repeat_count(count: int):
	global REPEAT_COUNT
	REPEAT_COUNT = count

def get_run_stats():
	stats_dict = PROC_STAT_LIST[0] if PROC_STAT_LIST else {};
	stats_dict.update({
		"wall_time": MIN_WALL_TIME,
		"exclusive_time": MIN_EXCLUSIVE_TIME,
		})
	### print(stats_dict)
	return stats_dict


def ext_stdout_handler(stdout, stderr):
	if isinstance(stdout, bytes):
		stdout = stdout.decode('utf8')
		# print(stdout)
	if isinstance(stderr, bytes):
		stderr = stderr.decode('utf8')
		# print(stderr)
		
	if OUTPUT_TYPE == 'prolog':
		# m_0 = re.search(r"Loading the ontology took (\d+) ms\.", stdout)  # reasoning started
		m = re.search(r"Time it took: (\d+) ms\.", stdout)  # reasoning time
		if m:
			dur_s = int(m[1]) / 1000
			OUTPUT_TIME_LIST.append(dur_s)
		else:
			print("An error occured examiming the output of Prolog...")
			
	elif OUTPUT_TYPE in ('jena', 'sparql'):
		m = re.search(r"Time spent on reasoning: ([\d.]+) seconds\.", stdout)  # reasoning started
		if m:
			dur_s = float(m[1])
			OUTPUT_TIME_LIST.append(dur_s)
		else:
			print("An error occured examiming the output of Jena...")
			
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

	
def invoke_shell(cmd, gather_stats=False, *args):
	if args:
		print(*args)
	# process = subprocess.Popen(cmd, stdout=stdout, stderr=stdout, creationflags=0x08000000)
	# process = psutil.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=0x08000000)
	process = psutil.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
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
		PROC_STAT_LIST.append(summarize_process_stat(stat_list))
	
	printout = process.communicate()
	ext_stdout_handler(*printout)
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
    except psutil.NoSuchProcess:
        pass
    except psutil.AccessDenied:
        pass
    return metrics

    
def summarize_process_stat(stat_list: list) -> dict:
	'find average CPU and max memoty from list of samples'
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

# class PelletStatsGatherer(Thread):
#     def __init__(self, max_wait=3):
#         """Инициализация потока"""
#         super().__init__()
#         self.max_wait = max_wait
    
#     def run(self):
#         """Запуск потока"""
#         gather_pellet_stats(self.max_wait)


def gather_pellet_stats(max_wait=3):
	# print('Tread Start!')
	# search for java proces running Pellet that should start soon
	elapsed = 0
	while elapsed < max_wait:
		try:
			for process in psutil.process_iter(['name', 'cmdline']):
				if process.name() == 'java.exe' and 'pellet.Pellet' in process.cmdline():
					break
				# else:
				# 	print(process.name(), end=' ')
			else:
				# print('Pellet not found (%.1f), waiting...' % elapsed)
				time.sleep(0.1)
				elapsed += 0.1
				continue
		except psutil.Error:
			print('failed searching for the Pellet process...')
			return
		break  # found!
	else:
		# still not found
		print("Pellet process has not been detected during %.1f seconds!" % max_wait)
		return 'failed to detect process...'
		
	# print('Found java->pellet! pid:', process.pid)
	stat_list = []
	interval = 0.1
	# stat = True
	while True:
		stat = cpu_mem(process, interval)  # blocks over 'interval' seconds
		if stat:
			stat_list.append(stat)
		else:
			break
	PROC_STAT_LIST.append(summarize_process_stat(stat_list))


def measure_stats_for_pellet_running(max_wait=3):
	# '''java -Xmx2000M -cp C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\antlr-3.2.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\antlr-runtime-3.2.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\aterm-java-1.6.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\commons-codec-1.6.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\httpclient-4.2.3.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\httpcore-4.2.2.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jcl-over-slf4j-1.6.4.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-arq-2.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-core-2.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-iri-0.9.5.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jena-tdb-0.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\jgrapht-jdk1.5.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\log4j-1.2.16.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\owlapi-distribution-3.4.3-bin.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\pellet-2.3.1.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\slf4j-api-1.6.4.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\slf4j-log4j12-1.6.4.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\xercesImpl-2.10.0.jar;C:\D\Work\Python\Python37\lib\site-packages\owlready2\pellet\xml-apis-1.4.01.jar pellet.Pellet realize --loader Jena --input-format N-Triples --infer-prop-values --infer-data-prop-values --ignore-imports {path}'''
	
	PROC_STAT_LIST.clear()
	# global _MAX_WAIT; _MAX_WAIT = max_wait
	global _WATCHING_THREAD
	
	from multiprocessing import Process
	# PelletStatsGatherer(max_wait)
	_WATCHING_THREAD = threading.Thread(target=gather_pellet_stats)
	_WATCHING_THREAD.start()
	
	return 'wait and call get_pellet_run_stats()'

def get_pellet_run_stats():
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
	

def run_swiprolog_reasoning(rdf_path_in:str, rdf_path_out:str, verbose=True):
	# C:\D\Work\YDev\CompPr\c_owl>swipl -s run_ontology "test_data/test_make_trace_output.rdf" "test_data/prolog_output.rdf"
	global OUTPUT_TYPE; OUTPUT_TYPE = 'prolog'
	cmd = f'swipl -s run_ontology "{rdf_path_in}" "{rdf_path_out}"'
	# if verbose: print(">_ running cmd:", cmd)
	run_cmd(cmd, verbose=verbose)
	# process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
	# process.wait()
	# exitcode = process.returncode
	# if verbose: print(">_ cmd finished with code", exitcode)
	return get_run_stats()


def run_jena_reasoning(rdf_path_in:str, rdf_path_out:str, reasoning_mode='jena', verbose=True):
	# java -jar Jena.jar "test_data/test_make_trace_output.rdf" "jena/all.rules" "test_data/jena_output.rdf"
	# How to specify working directory:
	# subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')
	
	global OUTPUT_TYPE; OUTPUT_TYPE = reasoning_mode
	
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
	return get_run_stats()
	

	
