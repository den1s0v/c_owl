import re

# from owlready2 import *

from trace_gen.json2alg2tr import get_target_lang
from upd_onto import get_relation_object, get_relation_subject



def tr(word_en, case='nomn'):
	""" Перевод на русский язык, если get_target_lang()=="ru" """
	if get_target_lang() == "en":
		return word_en
	grammemes = ('nomn','gent')
	assert case in grammemes, "Unknown case: "+case
	res = {
		"begin of " 		: ("начало ", ),
		"end of " 			: ("конец ", ),
		" (at line %d)" 	: (" (в строке %d)", ),
		" (the line is missing)" : (" (строка отсутствует)", ),
		"%s-branch" 		: ("ветка %s", ),
		"unknown structure" : ("неизвестная структура", ),
		"[unknown]"			: ("[неизвестно]", ),
		"expr"				: ("выражение", "выражения", ),
		"stmt"				: ("команда", "команды", ),
		"sequence"			: ("следование", "следования", ),
		"alternative"		: ("альтернатива", "альтернативы", ),
		"loop"				: ("цикл", "цикла", ),
		"while_loop"		: ("цикл", "цикла", ),
	}.get(word_en, ())
	try:
		return res[grammemes.index(case)]
	except IndexError:
		print("tr(%s, %s) error!"%(word_en, case))
		return "==>%s.%s not found!<=="%(word_en, case)


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


def get_base_classes(classes) -> set:
		return {sup for cl in classes for sup in cl.is_a}
	
	
def get_leaf_classes(classes) -> set:
		# print(classes, "-" ,base_classes)
		return set(classes) - get_base_classes(classes)
	
	
def format_full_name(a: 'act or stmt', include_phase=True, include_type=True, include_line_index=True, quote="'"):
	""" -> begin of loop waiting (at line 45) """
	try:
		onto = a.namespace
		
		is_act = bool({onto.act_begin, onto.act_end, onto.trace} & set(a.is_a))
		
		### print(" * ! is_act:", is_act, "for a:", a)
		
		phase = ''
		if is_act and include_phase:
			if onto.act_begin in a.is_a:
				phase = tr("begin of ")
			elif onto.act_end in a.is_a:
				phase = tr("end of ")
		
		line_index = ''
		if is_act and include_line_index:
			i = get_relation_object(a, onto.text_line)
			if i:
				line_index = tr(" (at line %d)") % i
			else:
				line_index = tr(" (the line is missing)")
		
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
					# onto_class += "-branch"
					onto_class = tr("%s-branch") % onto_class
				else:
					onto_class = tr(onto_class, 'gent' if include_phase else 'nomn')
				type_ = f"{onto_class} "
			else:
				type_ = tr("unknown structure")
			type_ = type_.strip() + " "
			
		### print(phase, type_, quote, stmt_name, quote, line_index)
		
		return phase + type_ + quote + stmt_name + quote + line_index
	except Exception as e:
		print(e)
		# raise e
		return tr("[unknown]")


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
	# return ['Cannot format explanation for XYZY']


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
	

def class_formatstr(*args):
	""" Перевод в русский язык, если get_target_lang()=="ru" """
	class_name, format_str_ru, format_str_en = args if len(args) == 3 else list(args[0])
	if get_target_lang() == "en":
		return class_name, format_str_en
	else:
		return class_name, format_str_ru


def register_explanation_handlers(onto):
	
	
	######### General act mistakes #########
	########========================########
	
	spec = """ActEndsWithoutStart	<начало акта А> не может выполняться позже <конец акта А>.	Act <A> can't finish in this line because it didn't start yet."""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,1),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """ActStartsAfterItsEnd	<начало акта А> не может выполняться позже <конец акта А>.	Act <A> can't start in this line because it is already finished."""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,1),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """MisplacedBefore	<Акт Б> не может выполняться раньше <начало акта А> потому что <Б> входит в <А>.	Act <B> is a part of <A> so it can't be executed outside of (earlier than) <A>"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(correct_parent_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """MisplacedAfter	<Акт Б> не может выполняться позже <конец акта А> потому что <Б> входит в <А>	Act <B> is a part of <A> so it can't be executed outside of (later than) <A>"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(correct_parent_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """MisplacedDeeper	Акт <B> не может выполняться в рамках акта, вложенного в акт <A>, потому что <B> входит в <A>	Act <B> is a part of <A> so it can't be executed whitin act nested to <A>"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(correct_parent_act, 0,1,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	# WrongContext is left not replaced in case if absence of correct act (-> MisplacedWithout)
	spec = """WrongContext	<Акт Б> не может выполняться при отсутствии выполения <акта А>, потому что <Б> входит в <А>.	Act <B> is a part of <A> so it can't be executed while no act of <A> exists"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(correct_parent_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """ExtraAct		<A> must not happen here due to previous error(s)"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,0).capitalize(),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """TooEarly	<A> должно произойти позже, после некоторых пропущенных актов (подробности см. далее)	<A> must happen later, after some missing acts"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,0).capitalize(),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """DisplacedAct	<A> должно произойти перед <B>, но не здесь (подробности см. далее)	<A> must happen before <B> but not here (see there for details)"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		before_this_act = get_relation_object(a, onto.should_be_before)
		return {
			'<A>': format_full_name(a, 1,0,0).capitalize(),
			'<B>': format_full_name(before_this_act, 1,1,1),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	
	######### Sequence mistakes #########
	########=====================########
	
	spec = """TooEarlyInSequence	<конец акта А> не может находится позже <начало акта Б>, потому что в <следование В><оператор А> находится перед <оператор Б>	Act <A> is placed in sequnce <C> before act <B> so act <A> must finish before act <B> starts"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		item = get_relation_object(a, onto.executes)
		sequence = get_relation_subject(onto.body_item, item)
		missing_acts = list(onto.should_be_after[a])
		stmts = {format_full_name(act, 0,0,0) for act in missing_acts}
		plur1_s = 's' if len(stmts) > 1 else ''
		is1_are = 'are' if len(stmts) > 1 else 'is'
		stmts = ", ".join(stmts)
		acts = ", ".join("'%s'"%format_full_name(act, 1,0,0, quote='') for act in missing_acts)
		plur2_s = 's:' if len(stmts) > 1 else ''
		
		return {
			'Act <A> is': f"Act{plur1_s} {stmts} {is1_are}",
			'act <A>': f"act{plur2_s} {acts}",
			'<B>': format_full_name(a, 0,0,0),
			'<C>': format_full_name(sequence, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """DuplicateOfAct (sequence only)	Оператор Б входит в следование А, при этом между  началом акта А и концом акта А содержится больше одного акта Б	Act <B> is a part of sequence <A> so each execution of <A> can contain strictly one execution of <B>"""
	class_name, format_str = class_formatstr(spec.split('\t'))
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
	
	
	
	######### Alternative mistakes #########
	########========================########
	
	spec = """NoFirstCondition		The first condition <B> must be executed right after alternative <A> starts"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		onto = a.namespace  # debugging reassignment (useless until different 'onto' appear)
		alt_act = get_relation_object(a, onto.precursor)
		# cond = get_relation_object(cond_act, onto.executes)
		cond_act = get_relation_object(a, onto.should_be)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """WrongBranch -> BranchOfLaterCondition	Во время выполнения альтернативы <акт А> не должна выполниться ветка <В>, потому что условие <Б> не должно проверяться после истинного условия	Alternative <A> must not execute branch <D> because the condition <C> is true"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	class_name = list(class_name.split())[0]
	
	def _param_provider(a: 'act_instance'):
		wrong_branch_act = a
		wrong_branch = get_relation_object(wrong_branch_act, onto.executes)
		# wrong_cond = get_relation_object(wrong_branch, onto.cond)  # - fails in case of ELSE branch
		correct_branch_act = get_relation_object(a, onto.should_be)
		correct_branch = get_relation_object(correct_branch_act, onto.executes)
		true_cond = get_relation_object(correct_branch, onto.cond)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			# '<B>': format_full_name(wrong_cond, 0,1,1),
			'<C>': format_full_name(true_cond, 0,0,0),
			'<D>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)

	
	spec = """BranchOfFalseCondition	Во время выполнения альтернативы <акт А> не должна выполниться ветка <В>, потому что условие <Б> ложно	Alternative <A> must not execute branch <C> because the condition <B> is false"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
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


	spec = """AnotherExtraBranch	Во время выполнения альтернативы <акт А> не должна выполниться ветка <В>, потому что ветка <Г> уже выполнилась	Alternative <A> must not execute branch <B> because the branch <D> has already been executed"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		prev_branch_act = get_relation_object(a, onto.cause)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(a, 0,1,1),
			'<D>': format_full_name(prev_branch_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """NoBranchWhenConditionIsTrue	Во время выполнения альтернативы <акт А> должна выполниться ветка <В>, потому что условие <Б> истинно	Alternative <A> must execute branch <C> because the condition <B> is true"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		correct_branch_act = get_relation_object(a, onto.should_be)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,1),
			'<C>': format_full_name(correct_branch_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """AllFalseNoEnd	Альтернатива <A> не имеет ветви "иначе", поэтому она должна завершиться, потому что условие <B> является ложным	Alternative <A> does not have 'else' branch so it must finish because the condition <B> is false"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		# onto = a.namespace
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(cond_act, onto.executes)
		br = get_relation_subject(onto.cond, cond)
		alt = get_relation_subject(onto.branches_item, br)
		# alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,1,1),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """AllFalseNoElse	Во время выполнения альтернативы <акт А> должна выполниться ветка <Г>, потому что условие <Б> ложно	Alternative <A> must execute branch <D> because the condition <B> is false"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		onto = a.namespace
		cond_act = get_relation_object(a, onto.precursor)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,1),
			'<D>': "'else'",
			}
	register_handler(class_name, format_str, _param_provider)
	
	

	######### Lops mistakes #########
	########=================########
	
	spec = """MissingIterationAfterSuccessfulCondition	Во время выполнения цикла <A> на <i-ой> итерации должно выполниться тело <D>, потому что условие <B> истинно	Iteration <C> of loop <A> must happen because condition <B> is true"""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		onto = a.namespace
		
		# cond_act = get_relation_subject(onto.student_next, a)
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		body = get_relation_object(loop, onto.body)
		
		return {
			'<i-ой>': 'очередной',
			' <C>': '',
			'<D>': format_full_name(body, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<A>': format_full_name(loop, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """IterationAfterFailedCondition	Во время выполнения цикла <A> на очередной итерации не должно выполниться тело <D>, потому что условие <B> ложно	During execution of loop <A>, iteration <C> mustn't happen because condition <B> is false."""
	class_name, format_str = class_formatstr(spec.split('\t'))
	
	def _param_provider(a: 'act_instance'):
		# onto = a.namespace
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		body = get_relation_object(loop, onto.body)
		
		return {
			'<C> ': '',
			'<D>': format_full_name(body, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,1),
			'<A>': format_full_name(loop, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	

