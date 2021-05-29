# export2json.py
# write algorithm examples to JSON as CompPrehension questions

from itertools import count

from owlready2 import *
import ctrlstrct_run
import trace_gen.styling as styling
import trace_gen.syntax as syntax

from pprint import pprint


syntax.set_allow_hidden_buttons(False)


def export_algtr2dict(alg_tr, onto):
	ctrlstrct_run.clear_ontology(onto, keep_tbox=True)
	ctrlstrct_run.algorithm_only_to_onto(alg_tr, onto)

	statementFacts = []
	answerObjects = []
	tags = []
	concepts = set()

	answer_ids = count()

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
		# write type(s)
		for class_ in ind.is_a:
			statementFacts.append({
				'subjectType': "owl:NamedIndividual",
				'subject': ind.name,
				'verb': "rdf:type",
				'objectType': "owl:Class",
				'object': class_.name,
			})
		# write relations
		for prop in ind.get_properties():
			for subj, value in prop.get_relations():
				if ind == subj:
					# print(ind, "\t >>>> .%s >>>>\t %s" % (prop.python_name, value))
					statementFacts.append({
						'subjectType': "owl:NamedIndividual",
						'subject': ind.name,
						'verb': prop.name,
						**({
							'objectType': "owl:NamedIndividual",
							'object': value.name,
						  }
						  if isinstance(value, Thing) else
						  {
							'objectType': type_of(value),
							'object': value,
						  })
					})

	# expr_values
	for ind in onto.expr.instances():
		expr_name = ind.stmt_name
		values_list = alg_data["expr_values"].get(expr_name, None)
		if values_list:
			#
			# print("values_list:", values_list)
			#
			statementFacts.append({
				'subjectType': "owl:NamedIndividual",
				'subject': expr_name,
				'verb': "not-for-reasoner:expr_values",
				'objectType': "List<boolean>",
				'object': ",".join([{True:'1',False:'0'}.get(v, str(v)) for v in values_list]),
			})


	def make_answerObject(hyperText, phase, id_, concept, answer_id=None):
		if answer_id is None:
			answer_id = next(answer_ids)
		# make simple trace line without "nth time" in English only ...
		# strip first word (begin/end/execute) and add phase (started/finished/performed)
		view_phase = {
			'started': 'began',
			'finished': 'ended',
			'performed': 'evaluated' if concept == 'expr' else 'executed',
		}[phase]
		trace_act = hyperText.split(maxsplit=1)[1] + " " + view_phase
		# trace_act_hypertext = trace_act
		trace_act_hypertext = styling.to_html(styling.prepare_tags_for_line(trace_act))

		# patch ids in HTML
		old_info = phase + ":" + str(id_)
		new_info = old_info + ":" + trace_act_hypertext
		nonlocal question_html
		question_html = question_html.replace(old_info, str(answer_id))

		### print("domainInfo length:", len(new_info))

		return {
			"answerId": answer_id,
			"hyperText": hyperText,
			"domainInfo": new_info,
			"isRightCol": False,
			"concept": concept,
			"responsesLeft": [],
			"responsesRight": []
		}

	# actions to answerObjects
	action_classes = [*onto.action.descendants()]

	### print(action_classes)

	for ind in sorted(onto.action.instances(), key=lambda a: a.name):
		if isinstance(ind, onto.algorithm):  # or use `ind.is_a`
			continue  # no buttons for whole algorithm
		action_class = [cl for cl in ind.is_a if cl in action_classes]
		assert action_class, (ind, ind.is_a, alg_tr)
		action_class = action_class[0]  # must exist
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

	# show concepts
	print("concepts:", concepts)


	# patch generated html ...
	question_html = question_html.replace("<i class=\"play small icon\"></i>", '<img src="https://icons.bootstrap-4.ru/assets/icons/play-fill.svg" alt="Play" width="22">')
	question_html = question_html.replace("<i class=\"stop small icon\"></i>", '<img src="https://icons.bootstrap-4.ru/assets/icons/stop-fill.svg" alt="Stop" width="20">')
	# data-toggle="tooltip" data-placement="top" title="Tooltip on top"
	question_html = question_html.replace("data-tooltip=", 'data-toggle="tooltip" title=')
	question_html = question_html.replace("data-position=\"top left\"", 'data-placement="top"')

	# # replace answer IDs with their positions among answerObjects
	# for i, answerObject in enumerate(answerObjects):
	# 	pattern = "answer_" + answerObject["domainInfo"]
	# 	new_str = "answer_" + str(i)
	# 	question_html = question_html.replace(pattern, new_str)

	question_html += STYLE_HEAD


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


STYLE_HEAD = '''<style type="text/css" media="screen">
	div.code-line {
	  font-family: courier;
	  font-size: 10pt;
	}

	span.string, span.atom { color: #f08; font-style: italic; font-weight: bold; }
	span.comment { color: #262; font-style: italic; line-height: 1em; }
	span.meta { color: #555; font-style: italic; line-height: 1em; }
	span.variable { color: #700; text-decoration: underline; }
	span.variable-2 { color: #b11; }
	span.struct { color: #07c; font-weight: bold; }
	span.number { color: #f00; font-weight: bold; }
	span.program { color: #f70; font-weight: bold; }
	span.function { color: #707; font-weight: bold; }
	span.action { color: #077; font-weight: bold; }
	span.qualifier { color: #555; }
	span.keyword { color: #00a; font-weight: bold; }
	span.builtin { color: #30a; }
	span.link { color: #762; }

	span.warning { background-color: #ff9; }
	span.error { background-color: #fdd; }
	span.button { background-color: #add; }

</style>
'''
