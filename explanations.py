import re

# from owlready2 import *

from upd_onto import get_relation_object, get_relation_subject


ALGORITHM_ITEM_CLASS_NAMES = {
	'sequence',
	"alternative", 
	'loop', "while_loop", 'do_while_loop', 'do_until_loop', 'for_loop', 'foreach_loop', 'infinite_loop',
	"func", 
	"expr", "stmt",
	"if", "else-if", "else", 
}

# map error class name to format string & method of it's expansion
FORMAT_STRINGS = {}
PARAM_PROVIDERS = {}


def get_leaf_classes(classes) -> set:
		base_classes = {sup for cl in classes for sup in cl.is_a}
		# print(classes, "-" ,base_classes)
		return set(classes) - base_classes
	
	
def format_full_name(a: 'act or stmt', include_phase=True, include_type=True, include_line_index=True, quote="'"):
	""" -> begin of loop waiting (at line 45) """
	try:
		onto = a.namespace
		
		is_act = bool({onto.act_begin, onto.act_end} & set(a.is_a))
		
		### print(" * ! is_act:", is_act, "for a:", a)
		
		phase = ''
		if is_act and include_phase:
			if onto.act_begin in a.is_a:
				phase = "begin of "
			elif onto.act_end in a.is_a:
				phase = "end of "
		
		line_index = ''
		if is_act and include_line_index:
			i = get_relation_object(a, onto.text_line)
			if i:
				line_index = f" (at line {i})"
			else:
				line_index = " (the line is missing) "
		
		if is_act:
			stmt = get_relation_object(a, onto.executes)
		else:
			stmt = a
		assert stmt, f" ValueError: no stmt found for {str(a)}"
		stmt_name = get_relation_object(stmt, onto.stmt_name)
		assert stmt_name, f" ValueError: no stmt_name found for {str(stmt)}"
		
		type_ = ''
		if include_type:
			onto_classes = get_leaf_classes(stmt.is_a)
			onto_classes = {c.name for c in onto_classes}  # convert to strings
			onto_classes &= ALGORITHM_ITEM_CLASS_NAMES
			if onto_classes:
				onto_class = next(iter(onto_classes))
				# make the name more readable
				if onto_class in {"if", "else-if", "else"}:
					onto_class += "-branch"
				type_ = f"{onto_class} "
			else:
				type_ = "unknown structure"
			type_ = type_.strip() + " "
			
		### print(phase, type_, quote, stmt_name, quote, line_index)
		
		return phase + type_ + quote + stmt_name + quote + line_index
	except Exception as e:
		print(e)
		raise e
		return "[unknown]"


def format_explanation(onto, act_instance, _auto_register=True) -> list:
	
	if not FORMAT_STRINGS:
		register_explanation_handlers(onto)
		
	error_classes = set(act_instance.is_a) & set(onto.Erroneous.descendants())
	error_classes = get_leaf_classes(error_classes)
	result = []
	
	for error_class in error_classes:
		class_name = error_class.name
		if class_name in PARAM_PROVIDERS:
			expl = format_by_spec(
				FORMAT_STRINGS[class_name],
				**PARAM_PROVIDERS[class_name](act_instance)
			)
			result.append(f"{class_name}: {expl}")
		else:
			print("Skipping explanation for:", class_name)
	
	# if not result and _auto_register:
	# 	register_explanation_handlers(onto)
	# 	return format_explanation(onto, act_instance, _auto_register=False)
			
	return result
	# return 'Cannot format explanation for '


def format_by_spec(format_str: str, **params: dict):
	"Simple replace"
	for key, value in params.items():
		format_str = format_str.replace(key, value)
		
	###
	print('*', format_str)
		
	return format_str
	# return 'cannot format it...'

def register_handler(class_name, format_str, method):
	"Map class name to function procesing act with that error "
	PARAM_PROVIDERS[class_name] = method
	FORMAT_STRINGS[class_name] = format_str
	# onto_class = onto[class_name]
	# # assert onto_class, onto_class
	# if onto_class:
	# 	onto_class._format_explanation = method
	# 	onto_class._format_str = format_str
	# else:
	# 	print(f" Warning: cannot register_explanation_handler for '{class_name}': no such class in the ontology.")
	

def register_explanation_handlers(onto):
	
	spec = """DuplicateOfAct (sequence only)	Оператор Б входит в следование А, при этом между  началом акта А и концом акта А содержится больше одного акта Б	Act <B> is a part of sequence <A> so each execution of <A> can contain strictly one execution of <B>"""
	class_name, _, format_str = spec.split('\t')
	class_name = list(class_name.split())[0]
	
	def _param_provider(a: 'act_instance'):
		# sequence_act = get_relation_subject(onto.parent_of, a)
		item = get_relation_object(a, onto.executes)
		sequence = get_relation_subject(onto.body_item, item)
		return {
			'<B>': format_full_name(a, 0,0,0),
			'<A>': format_full_name(sequence, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """MissingIterationAfterSuccessfulCondition	Во время выполнения цикла <акт А> на <i-ой> итерации должно выполниться тело <В>, потому что условие <Бi> истинно	Iteration <C> of loop <A> must happen because condition <B> is true"""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		onto = a.namespace
		
		# cond_act = get_relation_subject(onto.student_next, a)
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		
		return {
			'<C> ': '',
			'<B>': format_full_name(cond, 0),
			'<A>': format_full_name(loop, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	

	spec = """ActEndsWithoutStart	<начало акта А> не может выполняться позже <конец акта А>.	Act <A> can't finish in this line because it didn't start yet."""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,1),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """ActStartsAfterItsEnd	<начало акта А> не может выполняться позже <конец акта А>.	Act <A> can't start in this line because it is already finished."""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,1),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """BranchOfFalseCondition	Во время выполнения альтернативы <акт А> не должна выполниться ветка <В>, потому что условие <Б> ложно	Alternative <A> must not execute branch <C> because the condition <B> is false"""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		onto = a.namespace  # debugging reassignment (useless until different 'onto' appear)
		cond_act = get_relation_object(a, onto.cause)
		# cond = get_relation_object(cond_act, onto.executes)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,1),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """AllFalseNoEnd		Alternative <A> does not have 'else' branch so it must finish because the condition <B> is false"""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		onto = a.namespace
		cond_act = get_relation_object(a, onto.precursor)
		# cond = get_relation_object(cond_act, onto.executes)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,1),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """TooEarly		<A> must happen later"""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,0).capitalize(),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """ExtraAct		<A> must not happen here due to previous error(s)"""
	class_name, _, format_str = spec.split('\t')
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,0).capitalize(),
			}
	register_handler(class_name, format_str, _param_provider)
	
