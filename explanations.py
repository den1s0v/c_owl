import re

# from owlready2 import *

from trace_gen.json2alg2tr import get_target_lang
from upd_onto import get_relation_object, get_relation_subject


onto = None


def tr(word_en, case='nomn'):
	""" Перевод на русский язык, если get_target_lang()=="ru" """
	if get_target_lang() == "en":
		return word_en
	grammemes = ('nomn','gent')
	assert case in grammemes, "Unknown case: "+case
	res = {
		"__"				: ("__", ),
		"[unknown]"			: ("[неизвестно]", ),
		"begin of " 		: ("начало ", ),
		"end of " 			: ("конец ", ),
		" (at line %d)" 	: (" (в строке %d)", ),
		" (the line is missing)" : (" (строка отсутствует)", ),
		"%s-branch" 		: ("ветка %s", ),
		"unknown structure" : ("неизвестная структура", ),
		"expr"				: ("выражение", "выражения", ),
		"stmt"				: ("команда", "команды", ),
		"sequence"			: ("следование", "следования", ),
		"alternative"		: ("альтернатива", "альтернативы", ),
		"loop"				: ("цикл", "цикла", ),
		"while_loop"		: ("цикл", "цикла", ),
		"body of loop"		: ("тело цикла", "тела цикла", ),
		"ex."				: ("например,", ),
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
CLASS_NAMES = {}  # "lang" -> str


def get_base_classes(classes) -> set:
		return {sup for cl in classes for sup in cl.is_a}
	
	
def get_leaf_classes(classes) -> set:
		# print(classes, "-" ,base_classes)
		return set(classes) - get_base_classes(classes)
	
	
def format_full_name(a: 'act or stmt', include_phase=True, include_type=True, include_line_index=True, case='nomn', quote="'"):
	""" -> begin of loop waiting (at line 45) """
	try:
		
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
		
		if stmt_name.endswith("_loop_body"):
			# тело цикла XYZ
			# body of loop XYZ
			stmt_name = tr("body of loop", case) + " " + quote + stmt_name.replace("_loop_body", '') + quote
		else:
			stmt_name = quote + stmt_name + quote
		
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
		full_msg = phase + type_ + stmt_name  # + line_index
		if full_msg != stmt_name:
			# wrap in additional quotes
			full_msg = "«%s»" % full_msg
		if line_index:
			full_msg += line_index
		return full_msg
	except Exception as e:
		print(e)
		# raise e
		# return tr("[unknown]")
		return tr("__")


def format_explanation(current_onto, act_instance, _auto_register=True) -> list:
	
	global onto
	onto = current_onto
	
	if not FORMAT_STRINGS:
		register_explanation_handlers()
	# # Не оптимально, зато не кешируются устаревшие онтологии
	# if FORMAT_STRINGS:
	# 	FORMAT_STRINGS.clear()
	# 	PARAM_PROVIDERS.clear()
	# register_explanation_handlers()
	
	### print(*FORMAT_STRINGS.keys())
		
	error_classes = set(act_instance.is_a) & set(onto.Erroneous.descendants())
	error_classes = get_leaf_classes(error_classes)
	result = []
	
	for error_class in error_classes:
		class_name = error_class.name
		if class_name in PARAM_PROVIDERS:
			format_str = FORMAT_STRINGS[class_name].get(get_target_lang(), None) or FORMAT_STRINGS[class_name].get("en", '__')
			expl = format_by_spec(
				format_str,
				**PARAM_PROVIDERS[class_name](act_instance)
			)
			localized_class_name = CLASS_NAMES[class_name].get(get_target_lang(), None) or class_name
			result.append(f"{localized_class_name}: {expl}")
		else:
			print("Skipping explanation for:", class_name)
	
	# if not result and _auto_register:
	# 	register_explanation_handlers()
	# 	return format_explanation(onto, act_instance, _auto_register=False)
			
	return result
	# return ['Cannot format explanation for XYZY']


def format_by_spec(format_str: str, **params: dict):
	"Simple replace"
	for key, value in params.items():
		format_str = format_str.replace(key, value)
		
	if not format_str.endswith('.'):
		format_str += '.'
	###
	print('*', format_str)
		
	return format_str
	# return 'cannot format it...'

def register_handler(class_name, format_dict, method):
	"Map class name to function procesing act with that error "
	if isinstance(class_name, dict):
		class_names_dict = class_name
		class_name = class_names_dict["en"]
	else:
		class_names_dict = {}
	
	PARAM_PROVIDERS[class_name] = method
	FORMAT_STRINGS[class_name] = format_dict
	if class_names_dict:
		CLASS_NAMES[class_name] = class_names_dict
	# onto_class = onto[class_name]
	# # assert onto_class, onto_class
	# if onto_class:
	# 	onto_class._format_explanation = method
	# 	onto_class._format_str = format_str
	# else:
	# 	print(f" Warning: cannot register_explanation_handler for '{class_name}': no such class in the ontology.")
	

def class_formatstr(*args):
	""" Сохраняем все переводы в словарь """
	class_name, format_str_ru, format_str_en = args if len(args) == 3 else list(args[0])
	
	class_names_dict = dict(zip(("en", "ru"), class_name.split()))
	
	return class_names_dict, {
		"ru": format_str_ru,
		"en": format_str_en,
	}


def register_explanation_handlers():
	
	
	######### General act mistakes #########
	########========================########
	
	spec = """ActEndsWithoutStart Конец-без-начала
<начало акта А> не может выполняться позже <конец акта А>.
Act <A> can't finish in this line because it didn't start yet."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """ActStartsAfterItsEnd Акт-начался-позже-чем-закончился
Акт <A> не может начаться, потому что он уже закончился.
Act <A> can't start in this line because it is already finished."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 1,1,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """MisplacedBefore Раньше-объемлющего-акта
Акт <B> не может выполняться раньше начала акта <A>, потому что <B> входит в <A>.
Act <B> is a part of <A> so it can't be executed outside of (earlier than) <A>"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(correct_parent_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """MisplacedAfter Позже-объемлющего-акта
Акт <B> не может выполняться позже окончания акта <A>, потому что <B> входит в <A>
Act <B> is a part of <A> so it can't be executed outside of (later than) <A>"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(correct_parent_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	# EndedDeeper: Every act ends exactly when all its nested acts have ended, so act of the body of the loop 'work' cannot end until the end of act of the alternative 'choose' (the alternative 'choose' is included in the body of the loop 'work').
	spec = """EndedDeeper Конец-внутри-вложенного-акта
Всякий акт заканчивается ровно тогда, когда завершились все его вложенные акты, поэтому aкт <A> не может закончиться до окончания акта <B> (<B> входит в <A>)
Every act ends exactly when all its nested acts have ended, so act <A> cannot end until the end of act <B> (<B> is included in <A>)"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		nested = get_relation_object(a, onto.cause)
		return {
			'<A>': format_full_name(a, 0,0,0),
			'<B>': format_full_name(nested, 0,1,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	# WrongContext is left not replaced in case if absence of correct act (-> MisplacedWithout)
	spec = """WrongContext Вне-контекста
Акт <B> не может выполняться в рамках акта <EX>, потому что <B> непосредственно входит в "<A>".
Act <B> is an immediate part of "<A>" so it can't be executed inside of <EX>"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be) or get_relation_subject(onto.parent_of, a)
		wrong_parent_act = get_relation_object(a, onto.precursor)
		
		return {
			'<A>': format_full_name(correct_parent_act, 0,1,0, case='gent'),
			'<B>': format_full_name(a, 0,0,0),
			'<EX>': format_full_name(wrong_parent_act, 0,1,0) if wrong_parent_act else "__",
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	# spec = """ExtraAct Лишний-акт
	# Не должно быть здесь
	# <A> must not happen here due to previous error(s)"""
	# class_name, format_str = class_formatstr(spec.split('\n'))
	
	# def _param_provider(a: 'act_instance'):
	# 	return {
	# 		'<A>': format_full_name(a, 1,1,0).capitalize(),
	# 		}
	# register_handler(class_name, format_str, _param_provider)
	
	
	# spec = """TooEarly
	# <A> следует выполнить позже, после некоторых пропущенных актов
	# <A> must happen later, after some missing acts"""
	# class_name, format_str = class_formatstr(spec.split('\n'))
	
	# def _param_provider(a: 'act_instance'):
	# 	return {
	# 		'<A>': format_full_name(a, 1,1,0).capitalize(),
	# 		}
	# register_handler(class_name, format_str, _param_provider)
	
	
	# spec = """DisplacedAct Перемещённый-акт
	# <A> должно произойти перед <B>, но не здесь
	# <A> must happen before <B> but not here"""
	# class_name, format_str = class_formatstr(spec.split('\n'))
	
	# def _param_provider(a: 'act_instance'):
	# 	before_this_act = get_relation_object(a, onto.should_be_before)
	# 	return {
	# 		'<A>': format_full_name(a, 1,0,0).capitalize(),
	# 		'<B>': format_full_name(before_this_act, 1,1,0),
	# 		}
	# register_handler(class_name, format_str, _param_provider)
	
	
	
	######### Sequence mistakes #########
	########=====================########
	
	# spec = """TooEarlyInSequence
	# <конец акта А> не может находится позже <начало акта Б>, потому что в <следование В><оператор А> находится перед <оператор Б>
	# Act <A> is placed in sequnce <C> before act <B> so act <A> must finish before act <B> starts"""
	# class_name, format_str = class_formatstr(spec.split('\n'))
	
	# def _param_provider(a: 'act_instance'):
	# 	item = get_relation_object(a, onto.executes)
	# 	sequence = get_relation_subject(onto.body_item, item)
	# 	missing_acts = list(onto.should_be_after[a])
	# 	stmts = {format_full_name(act, 0,0,0) for act in missing_acts}
	# 	plur1_s = 's' if len(stmts) > 1 else ''
	# 	is1_are = 'are' if len(stmts) > 1 else 'is'
	# 	stmts = ", ".join(stmts)
	# 	acts = ", ".join("'%s'"%format_full_name(act, 1,0,0, quote='') for act in missing_acts)
	# 	plur2_s = 's:' if len(stmts) > 1 else ''
		
	# 	return {
	# 		'Act <A> is': f"Act{plur1_s} {stmts} {is1_are}",
	# 		'act <A>': f"act{plur2_s} {acts}",
	# 		'<B>': format_full_name(a, 0,0,0),
	# 		'<C>': format_full_name(sequence, 0,0,0),
	# 		}
	# register_handler(class_name, format_str, _param_provider)
	
	
	spec = """TooEarlyInSequence Не-в-порядке-следования
Следование выполняет все свои действия по порядку, поэтому <A> не может выполняться раньше, чем <B>.
A sequence performs all actions in order, so <A> cannot run before <B>"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		missed_act = get_relation_object(a, onto.should_be_after)
		print(" **** missed_act", missed_act)
		return {
			'<A>': format_full_name(a, 0,1,0),
			'<B>': format_full_name(missed_act, 0,1,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	# переработано
	spec = """NoFirstOfSequence Следование-не-сначала
Следование выполняет все действия по порядку от первого до последнего, поэтому выполнение следования <S> должно начинаться с этого: <B> (но не с этого: <A>)
A sequence performs all actions in order from the first through the last, so the execution of the sequence <S> must start with <B> (but not with <A>)"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		st = get_relation_object(a, onto.should_be)
		seq = get_relation_object(a, onto.precursor)
		print(" **** NoFirstOfSequence",)
		return {
			'<A>': format_full_name(a, 0,1,0),
			'<B>': format_full_name(st, 0,1,0),
			'<S>': format_full_name(seq, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	# SequenceFinishedTooEarly: A sequence performs all its actions from the first through the last, so it's too early to finish the sequence of the body of the loop 'work' because not all actions of the sequence have completed (ex. alternative 'choose').
	spec = """SequenceFinishedTooEarly Следование-прервано
Следование выполняет все свои действия от первого до последнего, потому рано заканчивать следование <A>, т.к. не все действия следования выполнены<EX>
A sequence performs all its actions from the first through the last, so it's too early to finish the sequence <A> because not all actions of the sequence have completed<EX>"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		missed_act = get_relation_subject(onto.should_be_before, a)
		print(" **** SequenceFinishedTooEarly", missed_act)
		return {
			'<A>': format_full_name(a, 0,0,0),
			'<EX>': f" ({tr('ex.')} {format_full_name(missed_act, 0,1,0)})" if missed_act else "",
			}
	register_handler(class_name, format_str, _param_provider)
	
	
	spec = """DuplicateOfAct Дубликат (sequence only)
Оператор <B> входит в следование <A>, поэтому между началом и концом акта <A> должен содержаться ровно один акт <B>.
Act <B> is a part of sequence <A> so each execution of <A> must contain strictly one execution of <B>"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
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
	
	spec = """NoFirstCondition Нет-первого-условия
Развилка в первую очередь проверяет все условия по порядку до первого истинного. Развилка <A> должна начинаться с проверки первого условия <B>.
An alternative first evaluates its conditions in order until one is true. The alternative <A> should start with the first condition <B>."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		alt_act = get_relation_object(a, onto.precursor)
		# cond = get_relation_object(cond_act, onto.executes)
		cond_act = get_relation_object(a, onto.should_be)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	# spec = """WrongBranch -> BranchOfLaterCondition
# Во время выполнения альтернативы <A> не должна выполниться ветка <D>, потому что условие <C> уже истинно.
# Alternative <A> must not execute branch <D> because the condition <C> is true"""
	# class_name, format_str = class_formatstr(spec.split('\n'))
	
	# def _param_provider(a: 'act_instance'):
	# 	wrong_branch_act = a
	# 	wrong_branch = get_relation_object(wrong_branch_act, onto.executes)
	# 	# wrong_cond = get_relation_object(wrong_branch, onto.cond)  # - fails in case of ELSE branch
	# 	correct_branch_act = get_relation_object(a, onto.should_be)
	# 	correct_branch = get_relation_object(correct_branch_act, onto.executes)
	# 	true_cond = get_relation_object(correct_branch, onto.cond)
	# 	alt_act = get_relation_subject(onto.student_parent_of, a)
	# 	return {
	# 		'<A>': format_full_name(alt_act, 0,0,0),
	# 		# '<B>': format_full_name(wrong_cond, 0,1,0),
	# 		'<C>': format_full_name(true_cond, 0,0,0),
	# 		'<D>': format_full_name(a, 0,0,0),
	# 		}
	# register_handler(class_name, format_str, _param_provider)

	
	spec = """BranchNotNextToCondition Ветка-без-условия
Альтернатива выполняет ветку только тогда, когда соответствующее условие истинно. Альтернативная ветка <C> не может начаться, пока условие <B> не проверено.
An alternative performs a branch only if the corresponding condition is true. The alternative <A> cannot execute the branch <C> until the condition <B> is evaluated."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)

	
	spec = """ElseBranchNotNextToLastCondition Ветка-иначе-без-условия
Альтернатива выполняет ветку "ИНАЧЕ" только тогда, когда ни одно условие не оказалось истинным. Альтернативная ветка <C> не может начаться, пока условие <B> не проверено.
An alternative performs the "ELSE" branch only if no condition is true. The alternative <A> cannot execute the branch <C> until the condition <B> is evaluated"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)

	
	spec = """CondtionNotNextToPrevCondition Условие-не-по-порядку
Развилка проверяет все условия по порядку до первого истинного. Во время выполнения альтернативы <A> условие <C> нельзя проверить, пока условие не проверено <B> (и не примет значение "ложь")
An alternative evaluates its conditions in order until one is true. The alternative <A> cannot evaluate condition <C> until the condition <B> is evaluated (and yielded false)"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)

	
	spec = """BranchOfFalseCondition Ветка-при-ложном-условии
Альтернатива выполняет ветку только тогда, когда соответствующее условие истинно. Во время выполнения альтернативы <A> не должна выполниться ветка <C>, потому что условие <B> ложно.
An alternative performs a branch only if the corresponding condition is true. The alternative <A> must not execute the branch <C> because the condition <B> is false."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.cause)
		# cond = get_relation_object(cond_act, onto.executes)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """AnotherExtraBranch Лишняя-вторая-ветка
Выполнив не более одного из альтернативных действий, развилка завершается. Во время выполнения альтернативы <A> не должна выполниться ветка <B>, потому что ветка <D> уже выполнилась.
Each alternative performs no more than one alternative action and terminates. The alternative <A> must not execute the branch <B> because the branch <D> has already been executed."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		prev_branch_act = get_relation_object(a, onto.cause)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(a, 0,1,0),
			'<D>': format_full_name(prev_branch_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """NoBranchWhenConditionIsTrue Нет-ветки-при-истинном-условии
Альтернатива выполняет ветку тогда, когда соответствующее условие истинно. Во время выполнения альтернативы <A> должна выполниться ветка <C>, потому что условие <B> истинно.
An alternative performs a branch if the corresponding condition is true. The alternative <A> must execute the branch <C> because the condition <B> is true."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		correct_branch_act = get_relation_object(a, onto.should_be)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			'<C>': format_full_name(correct_branch_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """LastFalseNoEnd Развилка-не-закончилась
Когда ни одно условие альтернативы не оказалось истинным, выполняется ветка "ИНАЧЕ" (при наличии), и завершается вся развилка. Альтернатива <A> не имеет ветки "иначе", поэтому она должна завершиться, так как условие <B> является ложным.
When no condition of an alternative is true, the alternative performs the "ELSE" branch (if exists) and finishes. The alternative <A> does not have an 'else' branch so it must finish because the condition <B> is false"""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(cond_act, onto.executes)
		br = get_relation_subject(onto.cond, cond)
		alt = get_relation_subject(onto.branches_item, br)
		# alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,1,0),
			}
	register_handler(class_name, format_str, _param_provider)

	# NoAlternativeEndAfterBranch: Each alternative performs no more than one alternative action and terminates. The alternative 'choose' has executed the 'if-ready' branch and should finish.
	spec = """NoAlternativeEndAfterBranch Развилка-не-закончена-после-ветки
Всякая альтернатива выполняет не более одного альтернативного действия и завершается. Альтернатива <A> выполнила ветку <B> и должна завершиться.
Each alternative performs no more than one alternative action and terminates. The alternative <A> has executed the <B> branch and should finish."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		# cond_act = get_relation_object(a, onto.precursor)
		# cond = get_relation_object(cond_act, onto.executes)
		# br = get_relation_subject(onto.cond, cond)
		alt = get_relation_object(a, onto.should_be)
		branch = get_relation_object(a, onto.precursor)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(branch, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """LastConditionIsFalseButNoElse Нет-ветки-иначе
Альтернатива выполняет ветку "ИНАЧЕ" только тогда, когда ни одно условие не оказалось истинным. Во время выполнения альтернативы <A> должна выполниться ветка <D>, потому что условие <B> ложно.
An alternative performs the "ELSE" branch only if no condition is true. The alternative <A> must execute the branch <D> because the condition <B> is false."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,0),
			'<D>': "'else'",
			}
	register_handler(class_name, format_str, _param_provider)
	
	

	######### Lops mistakes #########
	########=================########
	
                # cond_then_body (-> true)
	spec = """NoIterationAfterSuccessfulCondition Нет-итерации
Если условие продолжения цикла истинно, то цикл должен продолжиться, т.е. начаться итерация цикла. Поэтому, раз условие <B> истинно, должно начаться тело цикла <A>.
Every time the condition of continuation of a loop is true, the loop should continue, i.e. an iteration should begin. The Iteration of loop <A> must start because the condition <B> is true."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		
		cond_act = get_relation_object(a, onto.cause)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		
		print(cond_act, cond, loop)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
                # a general Loop
	spec = """NoLoopEndAfterFailedCondition Нет-конца-цикла
Цикл заканчивается, как только условие продолжения стало ложным. Поэтому, раз условие <B> ложно, цикл <A> должен завершиться.
A loop ends as soon as the continuation condition becomes false. Therefore, if the condition <B> is false, the loop <A> must end."""
                # a general Loop
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		
		cond_act = get_relation_object(a, onto.cause)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
                # a general Loop
	spec = """LoopEndsWithoutCondition Конец-цикла-без-проверки-условия
Цикл заканчивается только тогда, когда условие продолжения стало ложным. Поэтому, чтобы цикл <A> должен завершиться, раз условие <B> ложно.
A loop ends as soon as the continuation condition becomes false. Therefore, if the condition <B> is false, the loop <A> must end."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		
		cond_act = get_relation_object(a, onto.cause)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
                # start_with_cond
	spec = """LoopStartIsNotCondition Цикл-начался-не-с-проверки-условия
Цикл WHILE/FOREACH является циклом с предусловием. Поэтому начать цикл <A> следует с проверки условия <B>.
The WHILE/FOREACH loop is a preconditioned. Therefore, the <A> loop should start with a check of the condition <B>."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		
		loop_act = get_relation_object(a, onto.precursor)
		loop = get_relation_object(loop_act, onto.executes)
		cond = get_relation_object(loop, onto.cond)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
                # start_with_body
	spec = """LoopStartIsNotIteration Цикл-начался-не-с-итерации
Цикл DO[/БезусловныйЦикл?] является циклом с постусловием. Поэтому начать цикл <A> следует с итерации.
The Do[/unconditional-Loop?] loop is post-conditioned. Therefore, the loop <A> should start with an iteration."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		
		loop_act = get_relation_object(a, onto.precursor)
		loop = get_relation_object(loop_act, onto.executes)
		# cond = get_relation_object(loop, onto.cond)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			# '<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
                # a general Loop
	spec = """IterationAfterFailedCondition Итерация-при-ложном-условии
Как только условие продолжения стало ложным, цикл заканчивается. Поэтому, раз условие <B> ложно, итерация цикла <A> не может начаться.
As soon as the continuation condition becomes false, the loop ends. Therefore, if the condition <B> is false, the iteration of the loop <A> cannot start."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(cond_act, onto.executes)
		loop = get_relation_subject(onto.cond, cond)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,1),
			}
	register_handler(class_name, format_str, _param_provider)
	
	
                # body_then_cond
	spec = """NoConditionAfterIteration Нет-проверки-условия
После очередной итерации цикла WHILE/DO/FOREACH нужно проверить условие, чтобы продолжить цикл или закончить его. После итерации цикла <A> надо проверить условие <B>.
After an iteration of the WHILE/DO/FOREACH loop, the condition must be checked to continue the loop or finish it. After the iteration of loop <A>, condition <B> must be checked."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		body_act = get_relation_object(a, onto.cause)
		body = get_relation_object(body_act, onto.executes)
		loop = get_relation_subject(onto.body, body)
		cond = get_relation_object(loop, onto.cond)
		
		return {
			'<A>': format_full_name(loop, 0,1,0) if loop else '',
			'<B>': format_full_name(cond, 0,0,0) if cond else '',
			}
	register_handler(class_name, format_str, _param_provider)


                # body_then_cond
	spec = """NoConditionBetweenIterations Нет-проверки-условия-между-итерациями
После очередной итерации цикла WHILE/DO/FOREACH нужно проверить условие, чтобы продолжить цикл или закончить его. Перед тем как перейти к следующей итерации цикла <A>, нужно проверить условие <B>.
After an iteration of the WHILE/DO/FOREACH loop, the condition must be checked to continue the loop or finish it. Before proceeding to the next iteration of the loop <A>, the condition <B> must be checked."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		body_act = get_relation_object(a, onto.precursor)
		body = get_relation_object(body_act, onto.executes)
		loop = get_relation_subject(onto.body, body)
		cond = get_relation_object(loop, onto.cond)
		
		return {
			'<A>': format_full_name(loop, 0,0,0) if loop else '',
			'<B>': format_full_name(cond, 0,0,1) if cond else '',
			}
	register_handler(class_name, format_str, _param_provider)
	


                # ForLoop
	spec = """LoopStartsNotWithInit Цикл-FOR-начался-не-с-инициализации
Прежде чем начать цикл FOR, следует сначала инициализировать его. После начала цикла <A> нужно выполнить инициализацию <B>.
Before a FOR loop can be started, it must first be initialised. Once the <A> loop has been started, the initialization <B> should be performed. """
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_object(a, onto.precursor)
		loop = get_relation_object(loop_act, onto.executes)
		init = get_relation_object(loop, onto.init)
		
		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(init, 0,0,0) if init else '',
			}
	register_handler(class_name, format_str, _param_provider)


                # ForLoop
	spec = """InitNotAtLoopStart Инициализация-FOR-не-в-начале-цикла
Инициализация цикла FOR выполняется один раз в самом начале цикла. После акта <A> инициализацию <B> выполнять не следует.
The initialization of the FOR loop is performed once at the beginning of the loop. After the <A> act, the initialization <B> should not be performed."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		some_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A>': format_full_name(some_act, 0,1,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)
	

# =========================

                # ForLoop
	spec = """NoConditionAfterForInit Нет-проверки-условия-после-инициализации-цикла-FOR
Цикл FOR является циклом с предусловием, поэтому сразу после инициализации он проверяет условие продолжения. После инициализации <A> следует проверить условие цикла <B>.
The FOR loop is a preconditioned, so immediately after initialization, it checks the continuation condition. After initialization <A> the loop condition <B> should be evaluated."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForLoop
	spec = """IterationAfterForInit Итерация-после-инициализации-цикла-FOR
Цикл FOR является циклом с предусловием, поэтому прежде чем начать возможную итерацию, необходимо проверить условие цикла. После инициализации <A> следует проверить условие цикла <B>.
The FOR loop is a pre-conditioned loop, so it is necessary to check the loop condition before starting a possible iteration. After initialization <A> the condition of the loop <B> should be checked."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForLoop
	spec = """NoUpdateAfterIteration Нет-перехода-после-итерации-цикла-FOR
Цикл FOR является циклом с инкрементом, поэтому после всякой итерации необходимо выполнить переход к новому значению переменной цикла. После итерации цикла <A> следует выполнить переход <B>. (??? Терминология: переход/инкремент ???)
The FOR loop is a loop with increment, so after every iteration, it is necessary to update the loop variable. After the iteration of the loop <A>, the update <B> must be performed."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A!>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForLoop
	spec = """UpdateNotAfterIteration Нет-перехода-после-итерации-цикла-FOR
Цикл FOR является циклом с инкрементом, поэтому обновление переменной цикла до нового значения необходимо выполнять только после итерации. После итерации цикла <A> следует выполнить переход <B>.
The FOR loop is a loop with increment, so the update of the loop variable to a new value should only be done after iteration. After the iteration of the loop <A>, the update <B> should be performed."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A!>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForLoop
	spec = """ForConditionAfterIteration Условие-после-итерации-цикла-FOR
Цикл FOR является циклом с инкрементом, поэтому после итерации необходимо обновить значение переменной цикла, и только затем проверять условие цикла. После итерации цикла <A> следует выполнить переход <B>.
The FOR loop is a loop with increment, so it is necessary to update the loop variable after an iteration, and only then check the loop condition. After the iteration of the loop <A> the update <B> should be performed."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A!>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForLoop
	spec = """NoConditionAfterForUpdate Нет-условия-после-перехода-цикла-FOR
Цикл FOR является циклом с инкрементом, и после обновления переменной цикла до нового значения необходимо проверить условие продолжения цикла. После перехода <A> следует проверить условие <B>.
The FOR loop is a loop with an increment, and after updating the loop variable to a new value, it is necessary to check the continuation condition of the loop. After the update <A> the condition <B> should be checked."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)
		
		return {
			'<A!>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForeachLoop
	spec = """NoForeachUpdateAfterSuccessfulCondition Нет-перехода-после-условия-цикла-FOREACH
Цикл FOREACH обходит коллекцию/перебирает итератор, поэтому после проверки наличия очередного элемента должен перейти к этому элементу. Так как условие <A> истинно, следует получить очередной элемент и начать итерацию цикла <B>.
The FOREACH loop traverses the collection/iterator, so after checking for the next element, it should go to that element. Since condition <A> is true, the next element should be retrieved and the iteration of loop <B> should start."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		prev_act = get_relation_object(a, onto.precursor)
		# prev = get_relation_object(loop, onto.prev)
		
		return {
			'<A!>': format_full_name(prev_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForeachLoop
	spec = """ForeachUpdateNotAfterSuccessfulCondition Переход-не-после-истинного-условия-цикла-FOREACH
Цикл FOREACH обходит коллекцию/перебирает итератор, поэтому переходить к следующему элементу должен непосредственно после проверки наличия очередного элемента. Переход к очередному элементу должен следовать сразу за успешной проверкой условия <A> цикла <B>.
The FOREACH loop traverses the collection/iterator, so it should move to the next element immediately after checking for that element. Retrieving the next element in the loop <B> should immediately follow a successful check of the condition <A>."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		prev_act = get_relation_object(a, onto.precursor)
		# prev = get_relation_object(loop, onto.prev)
		
		return {
			'<A!>': format_full_name(prev_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


                # ForeachLoop
	spec = """NoIterationAfterForeachUpdate Нет-итерации-после-перехода-цикла-FOREACH
Цикл FOREACH обходит коллекцию/перебирает итератор, поэтому после перехода к очередному элементу должен начинать новую итерацию. Сразу за переходом к очередному элементу должно следовать начало итерации цикла <B>.
The FOREACH loop traverses the collection/iterator, so it should start a new iteration after traversing to the next element. As soon as the next element is retrieved the iteration of the <B> loop should start."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		prev_act = get_relation_object(a, onto.precursor)
		# prev = get_relation_object(loop, onto.prev)
		
		return {
			'<A!>': format_full_name(prev_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)



                # ForeachLoop
	spec = """IterationNotAfterForeachUpdate Итерация-не-после-перехода-цикла-FOREACH
Цикл FOREACH обходит коллекцию/перебирает итератор, поэтому начинать новую итерацию должен непосредственно после перехода к очередному элементу. Сразу за переходом к очередному элементу должно следовать начало итерации цикла <B>.
The FOREACH loop traverses the collection/iterator, so a new iteration should start immediately after traversing to the next element. The iteration of the <B> loop should start right after an element is retrieved."""
	class_name, format_str = class_formatstr(spec.split('\n'))
	
	def _param_provider(a: 'act_instance'):
		prev_act = get_relation_object(a, onto.precursor)
		# prev = get_relation_object(loop, onto.prev)
		
		return {
			'<A!>': format_full_name(prev_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)

