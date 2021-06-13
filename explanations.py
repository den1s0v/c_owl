import re


MESSAGES_FILE = "jena/control-flow-statements-domain-messages.txt"


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
		"do_while_loop"		: ("цикл", "цикла", ),
		"body of loop"		: ("тело цикла", "тела цикла", ),
		"ex."				: ("например,", ),
		"is true"			: ("истинно", ),
		"is false"			: ("ложно", ),
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


def get_executes(act, *_):
	boundary = get_relation_object(act, onto.executes)
	return get_relation_object(boundary, onto.boundary_of)

def get_base_classes(classes) -> set:
		return {sup for cl in classes for sup in cl.is_a}


def get_leaf_classes(classes) -> set:
		# print(classes, "-" ,base_classes)
		return set(classes) - get_base_classes(classes)


def format_full_name(a: 'act or stmt', include_phase=False, include_type=True, include_line_index=False, case='nomn', quote="'"):
	""" -> begin of loop waiting (at line 45) """
	try:

		is_act = bool({onto.act_begin, onto.act_end, onto.trace} & set(a.is_a))
		is_boundary = onto.boundary in a.is_a

		### print(" * ! is_boundary:", is_boundary, "for a:", a)

		phase = ''
		if is_act and include_phase:
			if onto.act_begin in a.is_a:
				phase = tr("begin of ")
			elif onto.act_end in a.is_a:
				phase = tr("end of ")
			case = 'gent'
		elif is_boundary and include_phase:
			if a.begin_of:
				phase = tr("begin of ")
			elif a.end_of:
				phase = tr("end of ")
			case = 'gent'

		line_index = ''
		if is_act and include_line_index:
			i = get_relation_object(a, onto.text_line)
			if i:
				line_index = tr(" (at line %d)") % i
			else:
				line_index = tr(" (the line is missing)")

		if is_act:
			stmt = get_executes(a)
		elif is_boundary:
			stmt = get_relation_object(a, onto.boundary_of)
		else:
			stmt = a
		assert stmt, f" ValueError: no stmt found for {str(a)}"
		stmt_name = get_relation_object(stmt, onto.stmt_name)
		assert stmt_name, f" ValueError: no stmt_name found for {str(stmt)}"

		if stmt_name.endswith("_loop_body"):
			# тело цикла XYZ
			# body of loop XYZ
			stmt_name = tr("body of loop", case) + " " + quote + stmt_name.replace("_loop_body", '') + quote
			include_type = False
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
			## with prefixed error name
			# localized_class_name = CLASS_NAMES[class_name].get(get_target_lang(), None) or class_name
			# explanation = f"{localized_class_name}: {expl}"
			## without error name
			explanation = expl
			result.append(explanation)
		else:
			print("<> Skipping explanation for: <>", class_name, "<>")

	# if not result and _auto_register:
	# 	register_explanation_handlers()
	# 	return format_explanation(onto, act_instance, _auto_register=False)

	return result
	# return ['Cannot format explanation for XYZY']


def format_by_spec(format_str: str, **params: dict):
	"Simple replace"
	placeholder_affices = (("<", ">"), ("<list-", ">"))
	for key, value in params.items():
		for prefix, suffix in (placeholder_affices or (("",""),)):
			format_str = format_str.replace(prefix + key + suffix, value)

	if not format_str.endswith('.') and not format_str.endswith('?'):
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

def _sort_linked_list(array, next_prop: "transitive onto.prop"):
	def cmp_to_key(prop_name):
		'Convert a cmp= function into a key= function'
		class K:
			def __init__(self, obj, *args):
				self.obj = obj
			def __lt__(self, other):
				return getattr(self.obj, prop_name).__contains__(other.obj)
			def __gt__(self, other):
				return getattr(other.obj, prop_name).__contains__(self.obj)
			def __eq__(self, other):
				return self.obj == other.obj
			def __le__(self, other):
				return getattr(self.obj, prop_name).__contains__(other.obj)
			def __ge__(self, other):
				return getattr(other.obj, prop_name).__contains__(self.obj)
			def __ne__(self, other):
				return self.obj != other.obj
		return K

	array.sort(key=cmp_to_key(next_prop.name))
	return array


def named_fields_param_provider(a: 'act_instance'):
	"""extract ALL field_* facts, no matter what law they belong to."""
	placeholders = {}
	for prop in a.get_properties():
		verb = prop.python_name
		if verb.startswith("field_"):  # признак того, что это специальное свойство [act >> str]
			fieldName = verb.replace("field_", "")
			value = prop[a][0]
			# convert to str
			value = {
				True: 'true',
				False: 'false',
			}.get(value, str(value))
			value = "\"" + value + "\""  # enclose
			if (fieldName in placeholders):
				# append to previous data
				value = placeholders.get(fieldName) + ", " + value

			placeholders[fieldName] = value
	return placeholders


def register_explanation_handlers():

	# read templates from file
	with open(MESSAGES_FILE) as f:
		for spec in f.readlines():
			spec = spec.strip()
			if not spec:
				continue
			class_name, format_str = class_formatstr(spec.split('\t'))
			register_handler(class_name, format_str, named_fields_param_provider)

	return
	# no more hardcode needed >>


	######### General act mistakes #########
	########========================########


	spec = """UpcomingNeighbour Oжидаемый-рано	Почему вы пропустили <A, B, C, ...> ?	Why did you skip <A, B, C, ...> ?"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		missed_acts = a.should_be_after
		# TODO: remove inner boundaries & convert b+e to one action
		# ...
		_sort_linked_list(missed_acts, onto.has_upcoming)
		missed_act = ', '.join(format_full_name(missed_act, 1,1,0) for missed_act in missed_acts)
		return {
			'<A, B, C, ...>': missed_act,
			}
	register_handler(class_name, format_str, _param_provider)

	spec = """NotNeighbour Hеожиданно	Почему вы выполнили <A> ?	Why did you execute <A> ?"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		return {
			'<A>': format_full_name(a, 0,1,0),
			}
	register_handler(class_name, format_str, _param_provider)

	spec = """WrongCondNeighbour Hе-при-том-условии	Почему вы выполнили <A>, когда условие <C> <TrueFalse>?	Why did you execute <A>, when the condition <C> <TrueFalse>?"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.has_causing_condition)
		cond_val = get_relation_object(cond_act, onto.expr_value)
		return {
			'<A>': format_full_name(a, 0,1,0),
			'<C>': format_full_name(a, 0,0,0),
			'<TrueFalse>': tr("is " + str(cond_val).lower()),
			}
	register_handler(class_name, format_str, _param_provider)

# 	spec = """ActEndsWithoutStart Конец-без-начала
# <начало акта А> не может выполняться позже <конец акта А>.
# Act <A> can't finish in this line because it didn't start yet."""
# 	class_name, format_str = class_formatstr(spec.split('\n'))

# 	def _param_provider(a: 'act_instance'):
# 		return {
# 			'<A>': format_full_name(a, 1,1,0),
# 			}
# 	register_handler(class_name, format_str, _param_provider)


# 	spec = """ActStartsAfterItsEnd Акт-начался-позже-чем-закончился
# Акт <A> не может начаться, потому что он уже закончился.
# Act <A> can't start in this line because it is already finished."""
# 	class_name, format_str = class_formatstr(spec.split('\n'))

# 	def _param_provider(a: 'act_instance'):
# 		return {
# 			'<A>': format_full_name(a, 1,1,0),
# 			}
# 	register_handler(class_name, format_str, _param_provider)


	# spec = """MisplacedBefore Раньше-объемлющего-акта	<B> не может выполняться до начала <A>, потому что <B> входит в <A>.	<B> is a part of <A> so <B> can't be executed before <A> starts"""
	# class_name, format_str = class_formatstr(spec.split('\t'))

	# def _param_provider(a: 'act_instance'):
	# 	correct_parent_act = get_relation_object(a, onto.context_should_be)
	# 	return {
	# 		'<A>': format_full_name(correct_parent_act, 0,0,0),
	# 		'<B>': format_full_name(a, 0,0,0),
	# 		}
	# register_handler(class_name, format_str, _param_provider)


	# spec = """MisplacedAfter Позже-объемлющего-акта	<B> не может выполняться после окончания <A>, потому что <B> входит в <A>	<B> is a part of <A> so <B> can't be executed after <A> ends"""
	# class_name, format_str = class_formatstr(spec.split('\t'))

	# def _param_provider(a: 'act_instance'):
	# 	correct_parent_act = get_relation_object(a, onto.context_should_be)
	# 	return {
	# 		'<A>': format_full_name(correct_parent_act, 0,0,0),
	# 		'<B>': format_full_name(a, 0,0,0),
	# 		}
	# register_handler(class_name, format_str, _param_provider)

	# EndedDeeper: Every act ends exactly when all its nested acts have ended, so act of the body of the loop 'work' cannot end until the end of act of the alternative 'choose' (the alternative 'choose' is included in the body of the loop 'work').
	spec = """EndedDeeper Конец-внутри-вложенного-акта	Действие не может завершиться до окончания всех вложенных действий, поэтому <A> не может закончиться до окончания действия <B>, которое входит в <A>	An action ends only when all its nested actions have ended, so <A> cannot end until <B> ends as <B> is a part of <A>"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		prev_act = get_relation_object(a, onto.precursor)
		nested = get_relation_subject(onto.student_parent_of, prev_act)
		return {
			'<A>': format_full_name(a, 0,1,0),
			'<B>': format_full_name(nested, 0,1,0),
			}
	register_handler(class_name, format_str, _param_provider)


	# WrongContext is left not replaced in case if absence of correct act (-> MisplacedWithout)
	spec = """WrongContext Вне-контекста	<B> не может выполняться в рамках <EX>, потому что <B> не является непосредственной частью <EX>	<B> can't be executed inside of <EX> because <B> is not a direct part of "<EX>"."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		# correct_parent_act = get_relation_object(a, onto.context_should_be) or get_relation_subject(onto.parent_of, a)
		wrong_parent_act = get_relation_object(a, onto.cause)

		return {
			# '<A>': format_full_name(correct_parent_act, 0,1,0, case='gent'),
			'<B>': format_full_name(a, 0,0,0),
			'<EX>': format_full_name(wrong_parent_act, 0,1,0) if wrong_parent_act else "__",
			}
	register_handler(class_name, format_str, _param_provider)


	# WrongContext is left not replaced in case if absence of correct act (-> MisplacedWithout)
	spec = """OneLevelShallower Через-уровень	<B> не может выполняться в рамках <EX>, потому что <B> является элементом <A_gent>, начните сначала <A>.	<B> cannot be executed within <EX> because <B> is an element of <A>, so start <A> first."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		correct_parent_act = get_relation_object(a, onto.context_should_be) or get_relation_subject(onto.parent_of, a)
		wrong_parent_act = get_relation_object(a, onto.cause)

		return {
			'<A_gent>': format_full_name(correct_parent_act, 0,1,0, case='gent'),
			'<A>': format_full_name(correct_parent_act, 0,1,0, case='nomn'),
			'<B>': format_full_name(a, 0,0,0),
			'<EX>': format_full_name(wrong_parent_act, 0,1,0) if wrong_parent_act else "__",
			}
	register_handler(class_name, format_str, _param_provider)


	# spec = """ExtraAct Лишний-акт
	# Не должно быть здесь   <A> must not happen here due to previous error(s)"""
	# class_name, format_str = class_formatstr(spec.split('\n'))

	# def _param_provider(a: 'act_instance'):
	# 	return {
	# 		'<A>': format_full_name(a, 1,1,0).capitalize(),
	# 		}
	# register_handler(class_name, format_str, _param_provider)


	# spec = """TooEarly
	# <A> следует выполнить позже, после некоторых пропущенных актов    <A> must happen later, after some missing acts"""
	# class_name, format_str = class_formatstr(spec.split('\n'))

	# def _param_provider(a: 'act_instance'):
	# 	return {
	# 		'<A>': format_full_name(a, 1,1,0).capitalize(),
	# 		}
	# register_handler(class_name, format_str, _param_provider)


	# spec = """DisplacedAct Перемещённый-акт
	# <A> должно произойти перед <B>, но не здесь    <A> must happen before <B> but not here"""
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

	spec = """TooEarlyInSequence Не-в-порядке-следования-рано	Следование выполняет все свои действия по порядку, поэтому <A> не может выполняться перед <B>.	A sequence executes its nested actions in order, so <A> cannot be executed before <B>"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		# missed_act = get_relation_object(a, onto.should_be_after)
		missed_acts = a.should_be_after
		missed_act = ', '.join(format_full_name(missed_act, 0,1,0) for missed_act in missed_acts)
		print(" **** missed_act", missed_act)
		return {
			'<A>': format_full_name(a, 0,1,0),
			# '<B>': format_full_name(missed_act, 0,1,0),
			'<B>': missed_act,
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """TooLateInSequence Не-в-порядке-следования-поздно	Следование выполняет все свои действия по порядку, поэтому <A> не может выполняться после <B>.	A sequence executes its nested actions in order, so <A> cannot be executed after <B>"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		extra_acts = a.should_be_before
		extra_act = ', '.join(format_full_name(extra_act, 0,1,0) for extra_act in extra_acts)
		print(" **** extra_act", extra_act)
		return {
			'<A>': format_full_name(a, 0,1,0),
			# '<B>': format_full_name(extra_act, 0,1,0),
			'<B>': extra_act,
			}
	register_handler(class_name, format_str, _param_provider)


# 	# переработано
# 	spec = """NoFirstOfSequence Следование-не-сначала
# Следование выполняет все действия по порядку от первого до последнего, поэтому выполнение следования <S> должно начинаться с этого: <B> (но не с этого: <A>)
# A sequence performs all actions in order from the first through the last, so the execution of the sequence <S> must start with <B> (but not with <A>)"""
# 	class_name, format_str = class_formatstr(spec.split('\n'))

# 	def _param_provider(a: 'act_instance'):
# 		st = get_relation_object(a, onto.should_be)
# 		seq = get_relation_object(a, onto.precursor)
# 		return {
# 			'<A>': format_full_name(a, 0,1,0),
# 			'<B>': format_full_name(st, 0,1,0),
# 			'<S>': format_full_name(seq, 0,0,0),
# 			}
# 	register_handler(class_name, format_str, _param_provider)


	# SequenceFinishedTooEarly: A sequence performs all its actions from the first through the last, so it's too early to finish the sequence of the body of the loop 'work' because not all actions of the sequence have completed (ex. alternative 'choose').
	spec = """SequenceFinishedTooEarly Следование-прервано	Следование выполняет все свои действия: нельзя закончить следование <A> не выполнив действия: <B1..Bn>.	A sequence always executes all its actions. The sequence <A> cannot finish until actions: <B1..Bn> are executed."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		# missed_act = get_relation_subject(onto.should_be_before, a)
		missed_acts = a.should_be_after
		missed_act = ', '.join(format_full_name(missed_act, 0,1,0) for missed_act in missed_acts)
		print(" **** SequenceFinishedTooEarly", missed_act)
		return {
			'<A>': format_full_name(a, 0,0,0),
			'<B1..Bn>': missed_act,
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """DuplicateOfAct Дубликат (sequence only)	Следование выполняет все свои действия ровно по 1 разу, поэтому во время выполнения действия <A> действие <B> должно выполниться ровно один раз.	A sequence executes each its action once, so each execution of <A> can contain only one execution of <B>"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		# sequence_act = get_relation_subject(onto.parent_of, a)
		item = get_executes(a)
		sequence = get_relation_subject(onto.body_item, item)
		return {
			'<B>': format_full_name(a, 0,0,0),
			'<A>': format_full_name(sequence, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)



	######### Alternative mistakes #########
	########========================########

	spec = """NoFirstCondition Нет-первого-условия	Развилка проверяет все свои условия по порядку до первого истинного. Поэтому выполнение развилки <A> должно начинаться с проверки её первого условия <B>.	An alternative evaluates its conditions in order until the first true condition. The alternative <A> should start with evaluating its first condition <B>."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		alt_act = get_relation_object(a, onto.precursor)
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
	# 	wrong_branch = get_executes(wrong_branch_act)
	# 	# wrong_cond = get_relation_object(wrong_branch, onto.cond)  # - fails in case of ELSE branch
	# 	correct_branch_act = get_relation_object(a, onto.should_be)
	# 	correct_branch = get_executes(correct_branch_act)
	# 	true_cond = get_relation_object(correct_branch, onto.cond)
	# 	alt_act = get_relation_subject(onto.student_parent_of, a)
	# 	return {
	# 		'<A>': format_full_name(alt_act, 0,0,0),
	# 		# '<B>': format_full_name(wrong_cond, 0,1,0),
	# 		'<C>': format_full_name(true_cond, 0,0,0),
	# 		'<D>': format_full_name(a, 0,0,0),
	# 		}
	# register_handler(class_name, format_str, _param_provider)


	spec = """BranchNotNextToCondition Ветка-без-условия	Развилка выполняет ветку, только если условие этой ветки истинно. Ветка <C> не может начаться, так как условие <B> еще не вычислено.	The alternative executes its branch only if the branch condition is true. The alternative <A> cannot execute the branch <C> because its condition <B> is not evaluated yet."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """ElseBranchNotNextToLastCondition Ветка-иначе-без-условия	Развилка выполняет ветку "ИНАЧЕ", только если все условия были ложными. Альтернативная ветка <C> не может начаться, пока условие <B> не вычислено.	An alternative executes its "ELSE" branch only if all its conditions are false. The alternative <A> cannot execute the branch <C> until its condition <B> is evaluated"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			# '<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """ElseBranchAfterTrueCondition Ветка-иначе-после-успешного-условия	Развилка выполняет ветку "ИНАЧЕ", только если все условия были ложными. Альтернативная ветка (ветка "ИНАЧЕ") не должна начинаться, поскольку условие <B> истинно.	An alternative executes its "ELSE" branch only if all its conditions are false. The alternative <A> must not execute the "ELSE" branch since the condition <B> is true"""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.precursor)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			# '<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """CondtionNotNextToPrevCondition Условие-не-по-порядку	Развилка проверяет свои условия по порядку до первого истинного. При выполнении развилки <A> условие <C> должно быть вычислено сразу после условия <B>, т.к. условие <B> ложно.	An alternative evaluates its conditions in order up to the first true condition. The alternative <A> should evaluate its condition <C> immediately after the condition <B> as <B> is false."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """ConditionTooEarly Условие-слишком-рано	Развилка проверяет свои условия по порядку до первого истинного. При выполнении развилки <A> условие <C> рано проверять, т.к. условие <B> еще не вычислено.	An alternative evaluates its conditions in order up to the first true condition. The alternative <A> cannot evaluate its condition <C> until the condition <B> is evaluated."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond = get_relation_object(a, onto.should_be_after)
		alt = get_relation_object(a, onto.context_should_be)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """ConditionAfterBranch Условие-после-ветки	Выполнив одну ветку, развилка завершается. При выполнении развилки <A> условие <B> не должно проверяться, потому что ветка <D> уже выполнена.	Each alternative executes no more than one alternative action and finishes. The alternative <A> must not evaluate its condition <B> because the branch <D> was executed."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		branch_act = get_relation_object(a, onto.precursor)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			'<D>': format_full_name(branch_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """DuplicateOfCondition Повтор-условия	Развилка проверяет все условия по порядку до первого истинного. При выполнении развилки <A> условие <B> не должно проверяться повторно.	An alternative evaluates its conditions in order up to the first true condition. The alternative <A> must not evaluate its condition <B> twice."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """NoNextCondition Нет-следующего-условия	Развилка проверяет все условия по порядку до первого истинного. При выполнении развилки <A> следующим должно проверяться условие <C>, так как условие <B> ложно.	An alternative evaluates its conditions in order up to the first true condition. The alternative <A> should evaluate its condition <C> next because the condition <B> is false."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		should_be = get_relation_object(a, onto.should_be)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			'<C>': format_full_name(should_be, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """BranchOfFalseCondition Ветка-при-ложном-условии	Развилка выполняет ветку, только если ее условие истинно. При выполнении развилки <A> не должна выполниться ветка <C>, потому что условие <B> ложно.	An alternative executes its branch only if its condition is true. The alternative <A> must not execute the branch <C> because its condition <B> is false."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.cause)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			'<C>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """AnotherExtraBranch Лишняя-вторая-ветка	Выполнив одну ветку, развилка завершается. При выполнении развилки <A> ветка <B> не должна начаться, потому что ветка <D> уже выполнилась.	An alternative executes only one branch. The alternative <A> must not start its branch <B> because the branch <D> was executed."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		prev_branch_act = get_relation_object(a, onto.cause)
		alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(a, 0,1,0),
			'<D>': format_full_name(prev_branch_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """BranchWithoutCondition Ветка-без-условия	Развилка выполняет ветку, только если условие этой ветки истинно. При выполнении развилки <A> ветка <C> не может начаться, потому что условие <B> не вычислено.	An alternative executes its branch when the branch condition evaluates to true. The alternative <A> must not execute the branch <C> without evaluating its condition <B> first."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		branch = get_executes(a)
		cond = get_relation_object(branch, onto.cond)
		alt_act = get_relation_subject(onto.branches_item, branch)
		# alt_act = get_relation_subject(onto.student_parent_of, a)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			'<C>': format_full_name(branch, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """NoBranchWhenConditionIsTrue Нет-ветки-при-истинном-условии	Развилка выполняет ветку, только если условие этой ветки истинно. При выполнении развилки <A> должна выполниться ветка <C>, потому что условие <B> истинно.	An alternative executes its branch when the corresponding condition is true. The alternative <A> must execute the branch <C> because its condition <B> is true."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		correct_branch = get_relation_object(a, onto.should_be)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			'<C>': format_full_name(correct_branch, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """LastFalseNoEnd Развилка-не-закончилась	Если все условия ложны и ветка "ИНАЧЕ" отсутствует, то развилка не выполнит ничего. Развилка <A>  должна завершиться, так как услови<е/я> <B1...Bn> ложн<о/ы> и ветка "ИНАЧЕ" отсутствует.	When all condtions of an alternative are false and "ELSE" branch does not exist, the alternative does not do anything. The alternative <A> does not have an 'else' branch so it must finish because its condition<s> <B1...Bn> <is/are> false."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_executes(cond_act)
		br = get_relation_subject(onto.cond, cond)
		alt = get_relation_subject(onto.branches_item, br)
		# alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """AlternativeEndAfterTrueCondition Развилка-закончилась-после-истиннного-условия	Когда вычисленное условие развилки истинно, выполняется сответствующая ветка. Развилка <A> не должна завершиться, пока ветка <C> истинного условия <B> не выполнена.	When a condition of an alternative evaluates to true, the alternative executes the corresponding branch. The alternative <A> should not finish until the branch <C> of successful condition <B> is executed."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_executes(cond_act)
		br = get_relation_subject(onto.cond, cond)
		alt = get_relation_subject(onto.branches_item, br)
		# alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	# NoAlternativeEndAfterBranch: Each alternative performs no more than one alternative action and terminates. The alternative 'choose' has executed the 'if-ready' branch and should finish.
	spec = """NoAlternativeEndAfterBranch Развилка-не-закончена-после-ветки	Развилка завершается, выполнив одну ветку. Развилка <A> выполнила ветку <B> и должна завершиться.	Each alternative finishes after executing one branch. The alternative <A> executed its branch <B> and should finish."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		# cond_act = get_relation_object(a, onto.precursor)
		# cond = get_executes(cond_act)
		# br = get_relation_subject(onto.cond, cond)
		alt = get_relation_object(a, onto.should_be)
		branch = get_relation_object(a, onto.precursor)
		return {
			'<A>': format_full_name(alt, 0,0,0),
			'<B>': format_full_name(branch, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """LastConditionIsFalseButNoElse Нет-ветки-иначе	Развилка выполняет ветку "ИНАЧЕ", только если все условия ложны. При выполнении развилки <A> услови<е/я> <B1...Bn> ложн<о/ы>, поэтому должна выполниться ветка "ИНАЧЕ".	An alternative executes its "ELSE" branch only if all conditions are false. The alternative <A> must execute its branch "ELSE" because the condition<s> <B1...Bn> <is/are> false."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		alt_act = get_relation_subject(onto.student_parent_of, cond_act)
		return {
			'<A>': format_full_name(alt_act, 0,0,0),
			'<B>': format_full_name(cond_act, 0,1,0),
			}
	register_handler(class_name, format_str, _param_provider)





	######### Lops mistakes #########
	########=================########

				# cond_then_body (-> true)
	spec = """NoIterationAfterSuccessfulCondition Нет-итерации	Когда условие продолжения цикла истинно, цикл должен продолжиться: начинается новая итерация цикла. Поскольку условие <B> истинно, должна начаться новая итерация цикла <A>.	If the loop continuation condition is true, the loop continues: its new iteration must begin. A new iteration of the loop <A> must begin because its condition <B> is true."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_executes(cond_act)
		loop = get_relation_subject(onto.cond, cond)

		print(cond_act, cond, loop)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


	spec = """LoopEndAfterSuccessfulCondition Конец-цикла-при-истинном-условии	Когда условие продолжения цикла истинно, цикл должен продолжиться: начинается новая итерация цикла. Поэтому, раз условие <B> истинно, цикл <A> заканчивать рано.	If the loop continuation condition is true, the loop continues: its new iteration must begin. It's too early to finish the loop <A> because its condition <B> is true."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_executes(cond_act)
		loop = get_relation_subject(onto.cond, cond)

		print(cond_act, cond, loop)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# a general conditional Loop
	spec = """NoLoopEndAfterFailedCondition Нет-конца-цикла	Цикл заканчивается, как только условие продолжения стало ложным. Так как условие <B> ложно, цикл <A> должен завершиться.	A loop ends when its continuation condition becomes false. Since the condition <B> is false, the loop <A> must end."""
				# a general conditional Loop
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_executes(cond_act)
		loop = get_relation_subject(onto.cond, cond)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# a general conditional Loop
	spec = """LoopEndsWithoutCondition Конец-цикла-без-проверки-условия	Цикл заканчивается, только если условие продолжения стало ложным. Поэтому цикл <A> не должен завершиться, пока условие <B> не вычислено.	A loop ends only when its condition becomes false. Since the condition <B> is not evaluated yet, the loop <A> must not end."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop = get_executes(a)
		cond = get_relation_object(loop, onto.cond)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# start_with_cond
	spec = """LoopStartIsNotCondition Цикл-начался-не-с-проверки-условия	Цикл <WHILE/FOREACH> является циклом с предусловием. Поэтому начать цикл <A> следует с проверки условия <B>.	The <WHILE/FOREACH> loop is preconditioned. So the loop <A> should first evaluate its condition <B>."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_object(a, onto.precursor)
		loop = get_executes(loop_act)
		cond = get_relation_object(loop, onto.cond)
		loop_type = loop and ([
					cls.name.replace("_loop", '').upper()
					for cls in (onto.while_loop, onto.foreach_loop)
					if cls in loop.is_a
				] or ['__'])[0] or ''

		return {
			'<WHILE/FOREACH>': loop_type,
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# start_with_body
	spec = """LoopStartIsNotIteration Цикл-начался-не-с-итерации	Цикл DO является циклом с постусловием. Поэтому цикл <A> следует начинать сразу с итерации.	The DO loop is post-conditioned. Therefore, the loop <A> should begin with a new iteration."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):

		loop_act = get_relation_object(a, onto.precursor)
		loop = get_executes(loop_act)
		# cond = get_relation_object(loop, onto.cond)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			# '<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# a general Loop
	spec = """IterationAfterFailedCondition Итерация-при-ложном-условии	Цикл заканчивается, когда условие продолжения стало ложным. Итерация цикла <A> не может начаться, потому что условие <B> ложно.	A loop ends when its condition becomes false. Since the condition <B> is false, the iteration of the loop <A> cannot start."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		cond_act = get_relation_object(a, onto.precursor)
		cond = get_executes(cond_act)
		loop = get_relation_subject(onto.cond, cond)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(cond_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# body_then_cond
	spec = """NoConditionAfterIteration Нет-проверки-условия	После итерации цикла <WHILE/DO/FOREACH> нужно решить, продолжать ли цикл или закончить его. После итерации цикла <A> следует вычислить условие <B>.	After an iteration of the <WHILE/DO/FOREACH> loop, its condition must be evaluated to determine whether to continue the loop or finish it. After the iteration of loop <A>, its condition <B> should be evaluated."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		body_act = get_relation_object(a, onto.precursor)
		body = get_executes(body_act)
		loop = get_relation_subject(onto.body, body)
		cond = get_relation_object(loop, onto.cond)
		loop_type = loop and ([
					cls.name.replace("_loop", '').upper()
					for cls in (onto.while_loop, onto.do_while_loop, onto.foreach_loop)
					if cls in loop.is_a
				] or ['__'])[0] or ''

		return {
			'<WHILE/DO/FOREACH>': loop_type,
			'<A>': format_full_name(loop, 0,0,0) if loop else '',
			'<B>': format_full_name(cond, 0,0,0) if cond else '',
			}
	register_handler(class_name, format_str, _param_provider)


				# body_then_cond
				# for тоже подходит!
				# conditional loop !
	spec = """NoConditionBetweenIterations Нет-проверки-условия-между-итерациями	После очередной итерации цикла <WHILE/DO/FOREACH> нужно решить, продолжать ли цикл или закончить его. Перед тем как перейти к следующей итерации цикла <A>, нужно вычислить условие <B>.	After an iteration of the <WHILE/DO/FOREACH> loop, it is to determine whether the loop continues or ends. Before proceeding to the next iteration of loop <A>, its condition <B> should be evaluated."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		body_act = get_relation_object(a, onto.precursor)
		body = get_executes(body_act)
		loop = get_relation_subject(onto.body, body)
		cond = get_relation_object(loop, onto.cond)
		loop_type = loop and ([
					cls.name.replace("_loop", '').upper()
					for cls in (onto.while_loop, onto.do_while_loop, onto.foreach_loop)
					if cls in loop.is_a
				] or ['__'])[0] or ''

		return {
			'<WHILE/DO/FOREACH>': loop_type,
			'<A>': format_full_name(loop, 0,0,0) if loop else '',
			'<B>': format_full_name(cond, 0,0,0) if cond else '',
			}
	register_handler(class_name, format_str, _param_provider)



				# ForLoop
	spec = """LoopStartsNotWithInit Цикл-FOR-начался-не-с-инициализации	Прежде чем начать цикл FOR, следует сначала выполнить инициализацию. В начале выполнения цикла <A> нужно выполнить инициализацию <B>.	Before starting a FOR loop it should be initialized. After starting the loop <A> it is necessary to execute its initialization <B>."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_object(a, onto.precursor)
		loop = get_executes(loop_act)
		init = get_relation_object(loop, onto.init)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(init, 0,0,0) if init else '',
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """InitNotAtLoopStart Инициализация-FOR-не-в-начале-цикла	Инициализация цикла FOR выполняется один раз в самом начале цикла. После <A> инициализацию <B> выполнять не следует.	The initialization of the FOR loop is executed once at the beginning of the loop. The initialization <B> should not be executed after <A>."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		some_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)

		return {
			'<A>': format_full_name(some_act, 0,1,0),
			'<B>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """NoConditionAfterForInit Нет-проверки-условия-после-инициализации-цикла-FOR	Цикл FOR является циклом с предусловием, т.е. он должен вычислить условие перед итерацией. После инициализации <A> следует вычислить условие цикла <B>.	The FOR loop is preconditioned, so it should evaluate its condition before a new iteration. After the initialization <A> the condition <B> should be evaluated."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		# init = get_relation_object(loop, onto.init)

		return {
			'<A>': format_full_name(init_act, 0,1,0),
			'<B!>': format_full_name(a, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """IterationAfterForInit Итерация-после-инициализации-цикла-FOR	Цикл FOR является циклом с предусловием, поэтому перед чем началом итерации необходимо вычислить условие цикла. После инициализации <A> следует вычислить условие цикла <B>.	The FOR loop is preconditioned, so it should evaluate its condition before starting a new iteration. After the initialization <A> the condition <B> should be evaluated."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		init_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(a, onto.should_be)

		return {
			'<A>': format_full_name(init_act, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """NoUpdateAfterIteration Нет-перехода-после-итерации-цикла-FOR	Цикл FOR имеет команду инкремента, которая обновляет значение переменной цикла. После итерации цикла <A> следует выполнить переход <B>.	The FOR loop has an increment command that updates the loop variable. After iteration of the loop <A> its update command <B> should be executed."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		# loop_act = get_relation_subject(onto.student_parent_of, a)
		update = get_relation_object(a, onto.should_be)
		loop = get_relation_subject(onto.update, update)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(update, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """UpdateNotAfterIteration Нет-перехода-после-итерации-цикла-FOR	Цикл FOR имеет команду инкремента, которая обновляет значение переменной цикла.  Переход <B> следует выполнять только после итерации цикла <A>.	The FOR loop has an increment command that updates the loop variable. The update command <B> should only be executed after the iteration of the loop <A>."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		update = get_executes(a)
		loop = get_relation_subject(onto.update, update)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(update, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """ForConditionAfterIteration Условие-после-итерации-цикла-FOR	Цикл FOR имеет команду инкремента, которая обновляет значение переменной цикла перед вычислением условия цикла. После итерации цикла <A> следует выполнить переход <B>.	The FOR loop has an increment command that updates the loop variable before the loop condition is evaluated. After iteration of the loop <A> its update command <B> should be executed."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		body_act = get_relation_object(a, onto.precursor)
		body = get_executes(body_act)
		loop = get_relation_subject(onto.body, body)
		update = get_relation_object(loop, onto.update)

		return {
			'<A>': format_full_name(loop, 0,0,0),
			'<B>': format_full_name(update, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForLoop
	spec = """NoConditionAfterForUpdate Нет-условия-после-перехода-цикла-FOR	Цикл FOR имеет команду инкремента, которая обновляет значение переменной цикла перед вычислением условия цикла. После перехода <A> следует вычислить условие <B>.	The FOR loop has an increment command that updates the loop variable before the loop condition is evaluated. After the update command <A> the condition <B> should be evaluated."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		update_act = get_relation_object(a, onto.precursor)
		cond = get_relation_object(a, onto.should_be)

		# init = get_relation_object(loop, onto.init)

		return {
			'<A>': format_full_name(update_act, 0,0,0),
			'<B>': format_full_name(cond, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForeachLoop
	spec = """NoForeachUpdateAfterSuccessfulCondition Нет-перехода-после-условия-цикла-FOREACH	Цикл FOREACH обходит коллекцию или перебирает итератор, переходя к очередному элементу при его наличии. Так как проверка на следующий элемент успешна (условие истинно), следует получить очередной элемент и начать итерацию цикла <B>.	The FOREACH loop traverses a collection or iterates over an iterator and proceeds to the next element is one exists. Since the check for the next element is successful (the condition is true), the next element should be retrieved and the iteration of the <B> loop should begin."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_subject(onto.student_parent_of, a)

		return {
			'<B>': format_full_name(loop_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForeachLoop
	spec = """ForeachUpdateNotAfterSuccessfulCondition Переход-не-после-истинного-условия-цикла-FOREACH	Цикл FOREACH обходит коллекцию или перебирает итератор, и переходить к следующему элементу должен непосредственно после проверки наличия очередного элемента. В цикле <B> переход к очередному элементу должен следовать сразу за успешной проверкой на следующий элемент.	The FOREACH loop traverses a collection or iterator and must go to the next element immediately after checking for the next element. The <B> loop should go to the next element right after a successful check for the next element."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_subject(onto.student_parent_of, a)

		return {
			'<B>': format_full_name(loop_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)


				# ForeachLoop
	spec = """NoIterationAfterForeachUpdate Нет-итерации-после-перехода-цикла-FOREACH	Цикл FOREACH обходит коллекцию или перебирает итератор, и после перехода к очередному элементу должен начинать новую итерацию. Сразу за переходом к очередному элементу должно следовать начало итерации цикла <B>.	The FOREACH loop traverses a collection or iterator and must start a new iteration after moving to the next element. Immediately after the advance to the next element, the iteration of the <B> loop should begin."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_subject(onto.student_parent_of, a)

		return {
			'<B>': format_full_name(loop_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)



				# ForeachLoop
	spec = """IterationNotAfterForeachUpdate Итерация-не-после-перехода-цикла-FOREACH	Цикл FOREACH обходит коллекцию или перебирает итератор, и начинать новую итерацию должен непосредственно после перехода к очередному элементу. Сразу за переходом к очередному элементу должно следовать начало итерации цикла <B>.	The FOREACH loop traverses a collection or iterator, and should start a new iteration immediately after moving to the next element. Right after the advance to the next element the iteration of the <B> loop should start."""
	class_name, format_str = class_formatstr(spec.split('\t'))

	def _param_provider(a: 'act_instance'):
		loop_act = get_relation_subject(onto.student_parent_of, a)

		return {
			'<B>': format_full_name(loop_act, 0,0,0),
			}
	register_handler(class_name, format_str, _param_provider)

