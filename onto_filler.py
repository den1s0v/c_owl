# onto-filler.py

from owlready2 import *

# import function make_ontology() that defines all classes & SWRL rules
from onto_creator import make_ontology


def extend_from_triples(onto, triples_list, names_map=None):
	""" -> changed onto
	Parse string values from
	"""
	assert isinstance(onto, Ontology), "expected an instance of owlready2.namespace.Ontology"
	assert not names_map or isinstance(names_map, dict), "expected None or an instance of dict"

	if names_map:
		names_map = {v: k for k, v in names_map.items()}
	else:
		names_map = {}

	type_predicate = 'type'

	# names_map.update({})

	# find out all the types of individuals declared with `type` as predicate
	name2obj = {}
	for s,p,o in triples_list:
		p = names_map.get(p, p)
		if p == type_predicate:
			s = names_map.get(s, s)
			o = names_map.get(o, o)

			# resolve the class name
			class_ = onto[o]
			if not class_:
				raise ValueError("extend_from_triples() error: `%s` is not recognized as a class of given ontology (`%s`)" % (o, onto.base_iri))

			# make an instance within the ontology
			instance = class_(s)
			name2obj[s] = instance
	###	print(name2obj)

	# parse all other individuals' relations
	for s,p,o in triples_list:
		p = names_map.get(p, p)
		if p != type_predicate:
			# resolve the predicate name
			predicate = onto[p]
			if not predicate:
				raise ValueError("extend_from_triples() error: `%s` is not recognized as a predicate of given ontology (`%s`)" % (p, onto.base_iri))
			s = names_map.get(s, s)
			o = names_map.get(o, o)
			subject = name2obj.get(s, None)

			if not subject:
				raise ValueError("extend_from_triples() error: subject `%s` is not recognized as a declared (with `rdf:type`) entity of given ontology (`%s`)" % (s, onto.base_iri))


			object_class = predicate.range  # primitive value classes (like bool, int, str) are also OK!
			if not object_class:
				print("* extend_from_triples() warning: attempting to find object `%s` in ontology or add as string value, as property `%s` is not declared with Range within given ontology (`%s`)" % (o, p, onto.base_iri))
				object_ = (
					onto[o]  # try find in ontology by name
					or  globals().get(o, None)  # try find in current scope (i.e. imported with `from owlready2 import *`)
					or  o  # leave plain string (OK if a string literal is expected)
					)
				print("* _ type", type(object_), "is chosen for", object_, end='\n'*2)

			else:
				object_class = object_class.first()  # extract from list
				object_ = object_class(o)
				if issubclass(object_class, Thing) and not object_:
					raise ValueError("* extend_from_triples() error: object `%s` is not recognized as a declared (with `rdf:type`) entity of given ontology (`%s`)" % (s, onto.base_iri))

			print("Go: ",subject,predicate,object_)
			# add relation (the most stable method to do it, tested on Owlready2 v0.23)
			predicate[subject].append(object_)
		# end of for
	return onto

# print("Resolving Nothing:", vars().get("Nothing", 'None!'))  # OK!

def _main():

	c_schema = make_ontology()


	############################
	######## Export RDF ########
	############################

	onto_name = c_schema.name
	rdf_filename = onto_name + '_filled' + '.rdf'

	c_schema.save(file=rdf_filename, format='rdfxml')
	print("Saved RDF file: {} !".format(rdf_filename))

	# upload_rdf_to_SPARQL_endpoint('http://localhost:3030/c_owl/data', rdf_filename)



if __name__ == '__main__':
	_main()
