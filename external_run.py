# external_run.py

import subprocess


def run_swiprolog_reasoning(rdf_path_in:str, rdf_path_out:str, verbose=False):
	# C:\D\Work\YDev\CompPr\c_owl>swipl -s run_ontology "test_data/test_make_trace_output.rdf" "test_data/prolog_output.rdf"
	cmd = f'swipl -s run_ontology "{rdf_path_in}" "{rdf_path_out}"'
	if verbose: print(">_ running cmd:", cmd)
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
	process.wait()
	if verbose: print(">_ cmd finished.")
	
	
	
