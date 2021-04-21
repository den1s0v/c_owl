# export2json.py
# write algorithm examoples to JSON for compPrehension Question format

from owlready2 import *
import ctrlstrct_run
import trace_gen.styling as styling
import trace_gen.syntax as syntax

from pprint import pprint

def export_algtr2dict(alg_tr, onto):
	ctrlstrct_run.clear_ontology(onto, keep_tbox=True)
	ctrlstrct_run.algorithm_only_to_onto(alg_tr, onto)

	statementFacts = []
	answerObjects = []
	tags = []
	concepts = set()

	# "owl:NamedIndividual"
	# "xsd:int"
	# "xsd:string"
	# "xsd:boolean"
	# objectType
	# object
	# verb
	# subjectType
	# subject

	### q_text = alg_tr['algorithm']['text']

	alg_data = alg_tr['algorithm']
	# pprint(alg_data)

	user_language = 'en'
	user_syntax = 'C'
	algorithm_tags = syntax.algorithm_to_tags(alg_data, user_language, user_syntax)
	# pprint(algorithm_tags)
	question_html = styling.to_html(algorithm_tags)


	# pprint(question_html)

	# algorithm structure
	for ind in onto.individuals():
		for prop in ind.get_properties():
			for subj, value in prop.get_relations():
				if ind == subj:
					# print(ind, "\t >>>> .%s >>>>\t %s" % (prop.python_name, value))
					statementFacts.append({
						'objectType': "owl:NamedIndividual",
						'object': ind.name,
						'verb': prop.name,
						**({
							'subjectType': "owl:NamedIndividual",
							'subject': value.name,
						  }
						  if isinstance(value, Thing) else
						  {
							'subjectType': type_of(value),
							'subject': value,
						  })
					})

	# expr_values
	for ind in onto.expr.instances():
		expr_name = ind.stmt_name
		values_list = alg_data["expr_values"].get(expr_name, None)
		if values_list:
			statementFacts.append({
				'objectType': "owl:NamedIndividual",
				'object': ind.name,
				'verb': "not-for-reasoner:expr_values",
				'subjectType': "List<boolean>",
				'subject': ",".join([{True:1,False:0}.get(v, v) for v in values_list]),
			})


	def make_answerObject(hyperText, phase, id_, concept):
		return {
			"hyperText": hyperText,
			"domainInfo": phase + ":" + str(id_),
			"isRightCol": True,
			"concept": concept,
			"responsesLeft": [],
			"responsesRight": []
		}

	# actions to answerObjects
	action_classes = [*onto.action.subclasses()]
	for ind in onto.action.instances():
		if isinstance(ind, onto.algorithm):  # or use `ind.is_a`
			continue  # no buttons for whole algorithm
		action_class = [cl for cl in ind.is_a if cl in action_classes][0]  # must exist
		concepts.add(action_class.name)
		for obj_dict in ctrlstrct_run.find_by_keyval_in("id", ind.id, alg_data):
			break
		### print(obj_dict)
		action_title = obj_dict["act_name"]["en"]
		if onto.expr in ind.is_a or onto.stmt in ind.is_a:
			answerObjects.append(make_answerObject(
				("execute" if onto.stmt in ind.is_a else "evaluate") + " " + action_title,
				"performed", ind.id, action_class.name,
			))
		else:
			answerObjects.append(make_answerObject(
				("begin") + " " + action_title,
				"started", ind.id, action_class.name,
			))
			answerObjects.append(make_answerObject(
				("end") + " " + action_title,
				"finished", ind.id, action_class.name,
			))


	return {
		"questionType": "ORDERING",
		"questionData": {
		  "questionType": "ORDER",
		  "questionDomainType": "OrderActs",
		  "questionText": question_html,
		  "areAnswersRequireContext": False,
		  "options": {
		  },
		  "answerObjects": answerObjects,
		  "statementFacts": statementFacts,
		},
		"concepts": [  # ???
		  "trace",
		  "mistake",
		  *sorted(concepts),
		],
		"tags": [  # ????
		  "C++",
		  # "basics",
		  # "operators",
		  # "order",
		  # "evaluation"
		]
	  }


def type_of(literal):
	if isinstance(literal, bool):
		return "xsd:boolean"
	if isinstance(literal, str):
		return "xsd:string"
	# "xsd:int"
	return "xsd:" + str(type(literal).__name__)
