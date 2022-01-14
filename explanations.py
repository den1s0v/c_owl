import re

from common_helpers import camelcase_to_snakecase


MESSAGES_FILE = "jena/control-flow-statements-domain-messages.txt"


# from owlready2 import *

from trace_gen.json2alg2tr import get_target_lang
from onto_helpers import get_relation_object, get_relation_subject


onto = None  # TODO: remove global var


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
CLASS_NAMES = {}  # "en-name" -> {"lang" -> "local-name"}


def get_executes(act, *_):
	onto = act.namespace
	boundary = get_relation_object(act, onto.executes)
	return get_relation_object(boundary, onto.boundary_of)

def get_base_classes(classes) -> set:
		return {sup for cl in classes for sup in cl.is_a}


def get_leaf_classes(classes) -> set:
		# print(classes, "-" ,base_classes)
		return set(classes) - get_base_classes(classes)

def class_name_to_readable(s):
	sep = " "
	res = s.replace("-", sep)
	if res == s:
		res = camelcase_to_snakecase(s, sep).capitalize()
	return res


# def format_full_name(a: 'act or stmt', include_phase=False, include_type=True, include_line_index=False, case='nomn', quote="'"):
	# """ -> begin of loop waiting (at line 45) """

	# assert False, "Deprecated function: format_full_name()"

	# try:

	# 	is_act = bool({onto.act_begin, onto.act_end, onto.trace} & set(a.is_a))
	# 	is_boundary = onto.boundary in a.is_a

	# 	### print(" * ! is_boundary:", is_boundary, "for a:", a)

	# 	phase = ''
	# 	if is_act and include_phase:
	# 		if onto.act_begin in a.is_a:
	# 			phase = tr("begin of ")
	# 		elif onto.act_end in a.is_a:
	# 			phase = tr("end of ")
	# 		case = 'gent'
	# 	elif is_boundary and include_phase:
	# 		if a.begin_of:
	# 			phase = tr("begin of ")
	# 		elif a.end_of:
	# 			phase = tr("end of ")
	# 		case = 'gent'

	# 	line_index = ''
	# 	if is_act and include_line_index:
	# 		i = get_relation_object(a, onto.text_line)
	# 		if i:
	# 			line_index = tr(" (at line %d)") % i
	# 		else:
	# 			line_index = tr(" (the line is missing)")

	# 	if is_act:
	# 		stmt = get_executes(a)
	# 	elif is_boundary:
	# 		stmt = get_relation_object(a, onto.boundary_of)
	# 	else:
	# 		stmt = a
	# 	assert stmt, f" ValueError: no stmt found for {str(a)}"
	# 	stmt_name = get_relation_object(stmt, onto.stmt_name)
	# 	assert stmt_name, f" ValueError: no stmt_name found for {str(stmt)}"

	# 	if stmt_name.endswith("_loop_body"):
	# 		# тело цикла XYZ
	# 		# body of loop XYZ
	# 		stmt_name = tr("body of loop", case) + " " + quote + stmt_name.replace("_loop_body", '') + quote
	# 		include_type = False
	# 	else:
	# 		stmt_name = quote + stmt_name + quote

	# 	type_ = ''
	# 	if include_type:
	# 		onto_classes = get_leaf_classes(stmt.is_a)
	# 		onto_classes = {c.name for c in onto_classes}  # convert to strings
	# 		onto_classes &= ALGORITHM_ITEM_CLASS_NAMES
	# 		if onto_classes:
	# 			onto_class = next(iter(onto_classes))
	# 			# make the name more readable
	# 			if onto_class in {"if", "else-if", "else"}:
	# 				# onto_class += "-branch"
	# 				onto_class = tr("%s-branch") % onto_class
	# 			else:
	# 				onto_class = tr(onto_class, 'gent' if include_phase else 'nomn')
	# 			type_ = f"{onto_class} "
	# 		else:
	# 			type_ = tr("unknown structure")
	# 		type_ = type_.strip() + " "

	# 	### print(phase, type_, quote, stmt_name, quote, line_index)
	# 	full_msg = phase + type_ + stmt_name  # + line_index
	# 	if full_msg != stmt_name:
	# 		# wrap in additional quotes
	# 		full_msg = "«%s»" % full_msg
	# 	if line_index:
	# 		full_msg += line_index
	# 	return full_msg
	# except Exception as e:
	# 	print(e)
	# 	# raise e
	# 	# return tr("[unknown]")
	# 	return tr("__")


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
			templates = FORMAT_STRINGS[class_name]
			format_str = templates.get(get_target_lang(), None) or templates.get("en", '__')
			params = PARAM_PROVIDERS[class_name](act_instance)
			expl = format_by_spec(
				format_str,
				**params
			)
			## with prefixed error name
			# localized_class_name = CLASS_NAMES[class_name].get(get_target_lang(), None) or class_name
			# explanation = f"{localized_class_name}: {expl}"
			## without error name
			explanation = {
				"names": {lang: class_name_to_readable(name) for lang,name in CLASS_NAMES[class_name].items()},
				"explanation": expl,
				"explanation_by_locale": {lang: format_by_spec(format_str, **params) for lang, format_str in templates.items()},
			}
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
	# placeholder_affices = None
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
		class_names_dict = {}  # ? use {en -> class_name} by default ?

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
			def __init__(self, obj, *_):
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
			## value = prop[a][0]
			for value in prop[a]:
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
