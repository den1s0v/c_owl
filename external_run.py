# external_run.py

import subprocess


def run_swiprolog_reasoning(rdf_path_in:str, rdf_path_out:str, verbose=False):
	# C:\D\Work\YDev\CompPr\c_owl>swipl -s run_ontology "test_data/test_make_trace_output.rdf" "test_data/prolog_output.rdf"
	cmd = f'swipl -s run_ontology "{rdf_path_in}" "{rdf_path_out}"'
	if verbose: print(">_ running cmd:", cmd)
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
	process.wait()
	if verbose: print(">_ cmd finished.")


def run_jena_reasoning(rdf_path_in:str, rdf_path_out:str, verbose=False):
	# java -jar Jena.jar "test_data/test_make_trace_output.rdf" "jena/all.rules" "test_data/jena_output.rdf"
	# How to specify working directory:
	# subprocess.Popen(r'c:\mytool\tool.exe', cwd=r'd:\test\local')
	cmd = f'java -jar jena/Jena.jar "{rdf_path_in}" "jena/all.rules" "{rdf_path_out}"'
	if verbose: print(">_ running cmd:", cmd)
	process = subprocess.Popen(cmd, creationflags=0x08000000)
	process.wait()
	if verbose: print(">_ cmd finished.")
	
	
	
