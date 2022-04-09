# onto_helpers.py

from owlready2 import *


def get_isolated_ontology(ontology_iri):
	new_world = World()
	return new_world.get_ontology(ontology_iri)


def delete_ontology(onto, close_world=True):
	onto.destroy()
	if close_world:
		onto.world.close()


def make_triple(subj, prop, obj):
	try:
		if FunctionalProperty in prop.is_a:
			# "not asserted" workaround
			setattr(subj, prop.python_name, obj)
		else:
			prop[subj].append(obj)
	except Exception as e:
		print("Exception in make_triple: ", subj, prop, obj)
		raise e


def remove_triple(subj, prop, obj):
	try:
		if FunctionalProperty in prop.is_a:
			# "not removed" workaround
			setattr(subj, prop.python_name, None)
		else:
			if obj in prop[subj]:
				prop[subj].remove(obj)
	except Exception as e:
		print("Exception in remove_triple: ", subj, prop, obj)
		raise e


def get_relation_object(subj, prop):
	"""
	Another way to retrieve 3rd element of stored triple.
	Usage:
		obj = get_relation_object(subj, prop)
	Works when the following fails (this appears generally with FunctionalProperty'es):
		obj = subj.prop
		objs = prop[subj]
	"""
	d = dict(prop.get_relations())
	return d.get(subj, None)

def get_relation_subject(prop, obj):
	"""
	Another way to retrieve 1st element of stored triple.
	Usage:
		subj = get_relation_subject(prop, obj)
	(This may be good for InverseFunctionalProperty'es)
	"""
	d = dict((b,a) for a,b in prop.get_relations())
	return d.get(obj, None)

