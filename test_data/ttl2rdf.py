import os.path
from glob import glob

import rdflib  # pip install rdflib
from rdflib import RDF

SEARCH_PATTERN = '*.ttl'

START_DIR = "c:/Temp2/cntrflowoutput_v4/"


FORMAT_IN = "turtle"
FORMAT_OUT = "xml"
EXT_OUT = ".rdf"
# EXT_OUT = ".full.rdf"

OVERWRITE_ANYWAY = True
# OVERWRITE_ANYWAY = False

INJECT_RDF = [
	# r'c:/D/Work/YDev/CompPr/c_owl/jena/control-flow-statements-domain-schema.rdf',
]


NS_CODE = 'http://vstu.ru/poas/code#'

# !! keep list of actions up to date!
action_classes = { rdflib.term.URIRef(NS_CODE + name)
					for name in 'action sequence expr stmt alternative if else-if else func func_call loop while_loop do_while_loop do_until_loop for_loop foreach_loop'.split() }

def patch(g):
	# insert boundaries for actions
	boundary_class = rdflib.term.URIRef(NS_CODE + "boundary")
	for s, o in g.subject_objects(RDF.type):
		if o in action_classes:
			for prop_name in ("begin_of", "end_of"):
				bound = rdflib.term.URIRef(s.replace(NS_CODE, NS_CODE + prop_name + "_"))
				g.add((bound, RDF.type, boundary_class))
				prop = rdflib.term.URIRef(NS_CODE + prop_name)
				g.add((bound, prop, s))
	return g



def convert(file_in, file_out):
	g = rdflib.Graph()

	# g.bind("my", "http://vstu.ru/poas/ctrl_structs_2020-05_v1#")
	# g.bind("owl", "http://www.w3.org/2002/07/owl#")

	# print("reading ... ", end='')
	g.parse(location=file_in, format=FORMAT_IN)
	# print("done")
	# print("saving ... ", end='')
	g.serialize(file_out, format=FORMAT_OUT)


def read_rdf(*files, rdf_format=None):
	g = rdflib.Graph()
	for file_in in files:
		g.parse(location=file_in, format=rdf_format)
	return g


def change_ext(filepath):
	return os.path.splitext(filepath)[0] + EXT_OUT


if __name__ == '__main__':
	inject_g = read_rdf(*INJECT_RDF)


	for fp in glob(START_DIR + SEARCH_PATTERN):
		target_filepath = change_ext(fp)
		if not OVERWRITE_ANYWAY and os.path.exists(target_filepath):
			continue

		print(fp, '...')
		try:
			# convert(fp, target_filepath)
			g = read_rdf(fp, rdf_format=FORMAT_IN)
			g += inject_g
			patch(g)
			g.serialize(target_filepath, format=FORMAT_OUT)
		except Exception as e:
			print("#################")
			print("Error:", e)
			print("^^^^^^^^^^^^^^^^^")
			# raise e

	print("done.")
