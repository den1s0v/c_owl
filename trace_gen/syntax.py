# syntax.py
'''Support for popular languages syntax (C, Java, Python, ?)
	Format a subset of syntax.
'''



import threading

# special storage that allows storing data isolated for each thread by dispatching calls from different threads internally
thread_globals = threading.local()

from common_helpers import jsObj
from trace_gen.json2alg2tr import tr, set_target_lang, get_target_lang
from trace_gen.styling import to_html


# EXISTING_TRACE = []
def get_existing_trace():
	'thread-safe wrapper for ex-global EXISTING_TRACE variable'
	try:
		return thread_globals.EXISTING_TRACE
	except AttributeError:
		trace = []
		thread_globals.EXISTING_TRACE = trace
		return trace


# SYNTAX = {}

# features of: Pseudocode / С / Python / JavaScript / etc.
# token : function(str or tag) -> tag or tags
def get_syntax(_init_default_syntax=True):
	'thread-safe wrapper for ex-global SYNTAX variable'
	try:
		return thread_globals.SYNTAX
	except AttributeError:
		# create & fill with defaults
		s = jsObj()
		s.INDENT_STEP = 2  # spaces

		s.ALLOW_HIDDEN_BUTTONS = True
		s.HIDE_ALL_BUTTONS = False
		# s.ALLOW_HIDDEN_BUTTONS = True
		# s.HIDE_ALL_BUTTONS = False

		s.FORCE_BUTTON_TOOLTIPS_IN_ENGLISH = False

		thread_globals.SYNTAX = s
		if _init_default_syntax:
			set_syntax("C")  # the default
		return s


SIMPLE_NODE_STATES = ('performed', )
COMPLEX_NODE_STATES = ('started', 'finished')
COMPLEX_NODE_STARTED = ('started', )
COMPLEX_NODE_FINISHED = ('finished', )

# Make begin & end buttons of complex acts look a little transparent
COMPLEX_ACTION_BUTTONS_DIMMING = True


BUTTON_TIP_FREFIX = {
	"ru": {
		'performed': 'Выполнится',
		'started': 'Начнётся',
		'finished': 'Закончится',
		# 'performed': 'Выполнить',
		# 'started': 'Начать',
		# 'finished': 'Закончить',
	},
	"en": {
		'performed': 'Perform',
		'started': 'Start',
		'finished': 'Finish',
	}
}

def set_indent_step(step: int):
	get_syntax().INDENT_STEP = step

def set_allow_hidden_buttons(allow: bool):
	get_syntax().ALLOW_HIDDEN_BUTTONS = allow

def set_hide_all_buttons(hide: bool):
	get_syntax().HIDE_ALL_BUTTONS = hide

def set_force_button_tooltips_in_english(force: bool):
	get_syntax().FORCE_BUTTON_TOOLTIPS_IN_ENGLISH = force


def set_syntax(programming_language_name: str):
	name = programming_language_name.capitalize()
	passthrough = lambda tag: tag
	call_tr = lambda s: tr(s)
	SYNTAX = get_syntax(_init_default_syntax=False)

	if name in ("Pseudocode", ):
		SYNTAX["BLOCK_OPEN"] = lambda: []
		SYNTAX["BLOCK_CLOSE"] = lambda: []
		SYNTAX["COMMENT"] = lambda tag: ["// ", tag]
		SYNTAX["CONDITION"] = passthrough
		SYNTAX["DO_KEYWORD"] = call_tr
		SYNTAX["ELSEIF_KEYWORD"] = call_tr
		SYNTAX["STATEMENT"] = passthrough
		SYNTAX["WHILE_KEYWORD"] = call_tr

	elif name in ("C", "C++", "Си", "Java"):
		SYNTAX["BLOCK_OPEN"] = lambda: ["{"]
		SYNTAX["BLOCK_CLOSE"] = lambda: ["}"]
		SYNTAX["COMMENT"] = lambda tag: ["// ", tag]
		SYNTAX["CONDITION"] = lambda tag: ["(", tag, ")"]
		SYNTAX["DO_KEYWORD"] = lambda s: "do"
		SYNTAX["ELSEIF_KEYWORD"] = lambda s: s.replace("else-if", "else if")
		SYNTAX["STATEMENT"] = lambda tag: [tag, ";"]
		SYNTAX["WHILE_KEYWORD"] = lambda s: "while"

	elif name in ("Python"):
		SYNTAX["BLOCK_OPEN"] = lambda: []
		SYNTAX["BLOCK_CLOSE"] = lambda: []
		SYNTAX["COMMENT"] = lambda tag: ["# ", tag]
		SYNTAX["CONDITION"] = lambda tag: [tag, ":"]
		SYNTAX["DO_KEYWORD"] = None
		SYNTAX["ELSEIF_KEYWORD"] = lambda s: s.replace("else-if", "elif")
		SYNTAX["STATEMENT"] = passthrough
		SYNTAX["WHILE_KEYWORD"] = lambda s: "while"

	else:
		print(f"### Warning (ignoring): Unknown syntax in set_syntax('{name}').")
		raise ValueError('Unknown syntax: `%s`' % name)
		return

	SYNTAX["name"] = name


# set_syntax("C")  # the default
# set_syntax("Pseudocode")
# set_syntax("Python")


# def escape_quotes(s):
#     'HTML-escape quotes'
#     return s.replace("'", '&apos;').replace('"', r'&quot;')
#     # .replace('\\', '\\\\')

def _get_act_button_tip(act_name, phase):
	lang = get_target_lang() if not get_syntax().FORCE_BUTTON_TOOLTIPS_IN_ENGLISH else 'en'
	name = act_name.get(lang, None) or act_name.get("en", "[action]") if isinstance(act_name, dict) else str(act_name)
	return BUTTON_TIP_FREFIX[lang][phase] + " " + (name.replace("'", '"'))

def _make_alg_button(alg_node_id, act_name, state_name, allow_states=None) -> list or tuple:
	SYNTAX = get_syntax()
	if SYNTAX.HIDE_ALL_BUTTONS or allow_states is None or (SYNTAX.ALLOW_HIDDEN_BUTTONS and (state_name not in allow_states)):
		return ()
	if not SYNTAX.ALLOW_HIDDEN_BUTTONS and (state_name not in allow_states):
		state_name = list(allow_states)[0]

	state_tip = _get_act_button_tip(act_name, state_name)
	icon_name = "play" if state_name != "finished" else "stop"
	# icon_role = "disabled" if COMPLEX_ACTION_BUTTONS_DIMMING and state_name != "performed" else ""
	return [
		{
			"tag": "span",
			"attributes": {
				"class": ["alg_button"],
				"algorithm_element_id": [str(alg_node_id)],
				# for compprehension
				"id": ["answer_%s:%d" % (state_name, alg_node_id)],
				"act_type": [state_name],
				"data-tooltip": [state_tip],
				"data-position": ["top left"],
				# "onclick": ["on_algorithm_element_clicked(this)"], # `onmouseup` event works too.
			},
			"content": [{
				"tag": "i",
				"attributes": {
					"class": [icon_name, "small icon"],  ### icon_role,
				},
				"content": ''
			},
			]
		},
	]

def _make_alg_tag(alg_node, token_type, inner='', states_before=None, states_after=None, trailing_content=None):
	more_attrs = {}
	if alg_node:
		id_ = alg_node["id"]

	all_states = tuple([*(states_before or ()), *(states_after or ())])

	if all_states:
		if all_states != SIMPLE_NODE_STATES:
			all_states = COMPLEX_NODE_STATES
		act_name = alg_node["act_name"]
		# вычислить целевое состояние по последнему акту трассы
		# all_states[0]  # started / performed
		state_name = find_state_for_alg_id(id_, all_states)

		inner = [
			*_make_alg_button(id_, act_name, state_name, states_before),
			inner,
			*_make_alg_button(id_, act_name, state_name, states_after),
			*([trailing_content] if trailing_content else ()),
		]

	return {
		"tag": "span",
		"attributes": {"class": [token_type], **more_attrs},
		"content": inner
	}


def find_state_for_alg_id(algorithm_element_id, states):
	'''Для составных актов сосотяние кнопки зависит от последнего акта в трассе'''
	assert states
	if len(states) > 1:
		# iterate the trace up from the bottom
		for act in reversed(get_existing_trace()):
			if act["executes"] == algorithm_element_id and act["is_valid"] == True:
				# "phase":    "string",  // "started"/"finished"/"performed"
				last_phase = act["phase"]
				return {
					"started": "finished",
					"finished": "started",
					"performed": "performed", # this should never match
				}[last_phase]
	return states[0]  # started / performed


def _make_line_tag(indent, inner='', css_class='code-line', indent_attr='margin-left'):
	return {
		"tag": "div",
		"attributes": {"class": [css_class], "style": [indent_attr + ': %dem;' % indent] if indent else ()},
		"content": inner
	}
def _make_block_tag(indent, inner='', indent_attr='margin-left'):
	return _make_line_tag(indent, inner, css_class='code-block', indent_attr=indent_attr)


def _make_block_with_braces(indent, block_json, inner=()):
	SYNTAX = get_syntax()
	return [
	# кнопка для начала тела цикла
	_make_line_tag(indent,
		_make_alg_tag(block_json, '',
			inner=[
				*(SYNTAX["BLOCK_OPEN"]() or [""]),
			],
			states_after=COMPLEX_NODE_STARTED,
			trailing_content="&nbsp;" * (SYNTAX.INDENT_STEP))
		),
	# # тело цикла
	# algorithm_to_tags(block_json, indent=indent + SYNTAX.INDENT_STEP),
	_make_block_tag(SYNTAX.INDENT_STEP, inner, indent_attr='padding-left'),
	# закрыть тело цикла (если требуется по синтаксису)
	# кнопка для конца тела цикла
	_make_line_tag(indent,
		_make_alg_tag(block_json, '',
			inner=[
				*(SYNTAX["BLOCK_CLOSE"]() or [""]),
			],
			states_after=COMPLEX_NODE_FINISHED,
			trailing_content="&nbsp;" * (SYNTAX.INDENT_STEP) # немного пробелов, т.к. строка короткая
		)),
	]


def algorithm_to_tags(algorithm_json:dict or list, user_language: str=None, syntax:str=None, existing_trace=None, indent=0) -> list:
	""" Create new tree of html-tags with additional info about nodes """
	if user_language:
		set_target_lang(user_language)  # usually set once on the topmost recursive call
	if syntax:
		set_syntax(syntax)  # usually set once on the topmost recursive call
	if existing_trace is not None:
		# existing_trace tells which states to select for statements buttons
		EXISTING_TRACE = get_existing_trace()
		EXISTING_TRACE.clear()
		EXISTING_TRACE.extend(existing_trace)

	if isinstance(algorithm_json, (list, tuple)):
		return [algorithm_to_tags(el, indent=indent) for el in algorithm_json]

	if isinstance(algorithm_json, str):
		assert 0, algorithm_json
		# return algorithm_json

	SYNTAX = get_syntax()

	if isinstance(algorithm_json, dict):
		if algorithm_json["type"] == "algorithm":
			algorithm_json = algorithm_json["entry_point"]

		# temporary solution ...
		if algorithm_json["type"] == "func":
			algorithm_json = algorithm_json["body"]

		type_ = algorithm_json["type"]
		name = algorithm_json.get("name") or algorithm_json.get("stmt_name")

		if type_ in ("expr", ):
			return _make_alg_tag(algorithm_json, "variable", name, states_before=SIMPLE_NODE_STATES)

		if type_ == "stmt":
			return _make_line_tag(indent, SYNTAX["STATEMENT"](_make_alg_tag(algorithm_json, "variable", name, states_before=SIMPLE_NODE_STATES)))

		if type_ == "return":
			inner = [
				_make_alg_tag(algorithm_json, "keyword", "return", states_before=SIMPLE_NODE_STATES),  # <- not `name` here.
			]
			if "return_expr" in algorithm_json:
				inner += [
					"&nbsp;",
					_make_alg_tag(0, "variable", algorithm_json["return_expr"]),
				]
			return _make_line_tag(indent, SYNTAX["STATEMENT"](inner))

		if type_ in ("break", "continue", ):
			return _make_line_tag(indent, SYNTAX["STATEMENT"](_make_alg_tag(algorithm_json, "keyword", name, states_before=SIMPLE_NODE_STATES)))

		elif type_ == "sequence":  # and not name.endswith("_loop_body"):
			# # recurse with list
			# return algorithm_to_tags(algorithm_json["body"], indent=indent)  # indent++ ??
			# list of lines
			# return [_make_line_tag(indent, algorithm_to_tags(el, indent=indent)) for el in algorithm_json["body"]]
			return [(algorithm_to_tags(el, indent=indent)) for el in algorithm_json["body"]]

		elif type_.endswith("_loop"):
			loop_type = type_.replace("_loop", '')

			if loop_type == 'while':
				return _make_line_tag(0, [
					# заголовок цикла
					_make_line_tag(indent, [
						_make_alg_tag(algorithm_json, 'keyword',
							inner=SYNTAX["WHILE_KEYWORD"](loop_type),
							states_before=COMPLEX_NODE_STARTED, states_after=COMPLEX_NODE_FINISHED),
						"&nbsp;",
						*SYNTAX["CONDITION"](algorithm_to_tags(algorithm_json["cond"])),
						"&nbsp;" * 2,
						_make_alg_tag(None, 'comment',
							inner=SYNTAX["COMMENT"](name))
					]),
					*_make_block_with_braces(indent, algorithm_json["body"], inner=algorithm_to_tags(algorithm_json["body"], indent=0))
				])

			if loop_type == 'do_while':
				# заголовок цикла
				header_line = _make_line_tag(indent, [])
				if SYNTAX["DO_KEYWORD"]:
					# syntax like C++/Java with do-while loop
					header_line["content"] += [
						_make_alg_tag(algorithm_json, 'keyword',
							inner=SYNTAX["DO_KEYWORD"](loop_type),
							states_before=COMPLEX_NODE_STARTED, states_after=COMPLEX_NODE_FINISHED),
						"&nbsp;" * 2,
						_make_alg_tag(None, 'comment',
							inner=SYNTAX["COMMENT"](name))
					]
				else:
					# Python case: emulate with `WHILE(TRUE): IF(): BREAK`.
					header_line["content"] += ['==Python не поддерживает DO-WHILE==']

				body_lines = _make_block_with_braces(indent, algorithm_json["body"], inner=algorithm_to_tags(algorithm_json["body"], indent=0))

				if not SYNTAX["DO_KEYWORD"]:
					# TODO: Python case: emulate with `IF(): BREAK`
					footer_line = []

				# # закрыть тело цикла (если требуется по синтаксису)
				# body_end_lines = (SYNTAX["BLOCK_CLOSE"]() and [_make_line_tag(indent, SYNTAX["BLOCK_CLOSE"]())])

				if SYNTAX["DO_KEYWORD"]:  # make 'WHILE' end
					footer_line = _make_line_tag(indent, [
						_make_alg_tag(None, 'keyword',
									inner=SYNTAX["WHILE_KEYWORD"](loop_type)),
						"&nbsp;",
						*SYNTAX["STATEMENT"](SYNTAX["CONDITION"](algorithm_to_tags(algorithm_json["cond"]))),
					])

				return _make_line_tag(0, [
					header_line,
					*body_lines,
					# *body_end_lines,
					footer_line
				])

			# for, ... and more
			else:
				raise NotImplementedError('Not implemented for loop type: ' + loop_type)

		elif type_ == "alternative":
			result = []
			# цикл по веткам
			for branch in algorithm_json["branches"]:
				# заголовок ветки
				line = _make_line_tag(indent, [])
				if branch["type"] == "if":
					# добавить кнопку для всей развилки
					line["content"].append(
						_make_alg_tag(algorithm_json, 'keyword',
							inner=tr(branch["type"]) if SYNTAX["name"] == 'Pseudocode' else branch["type"],
							states_before=COMPLEX_NODE_STARTED, states_after=COMPLEX_NODE_FINISHED))
				else:
					# добавить просто ключевое слово - начало ветки
					line["content"].append(
						_make_alg_tag(algorithm_json, 'keyword',
							inner=SYNTAX["ELSEIF_KEYWORD"](branch["type"])))

				if 'cond' in branch:  # эта ветка - не ELSE
					line["content"].append(" ")
					line["content"].append(SYNTAX["CONDITION"](algorithm_to_tags(branch["cond"])))

				if branch["type"] == "if":
					# добавить название развилки
					line["content"] += [
						"&nbsp;" * 2,
						_make_alg_tag(None, 'comment',
							inner=SYNTAX["COMMENT"](name))
					]

				result.append(line)

				result += _make_block_with_braces(indent, branch, inner=algorithm_to_tags(branch["body"], indent=0))

			return _make_line_tag(0, result)

		else:
			print("Warning in algorithm_to_tags(): unknown node type:", type_)
	return ''


if __name__ == '__main__':
	# print(__doc__)

	from pprint import pprint
	# html_tags = prepare_tags_for_line("условие не_зелёный выполнилось 1-й раз - истина")
	# pprint(html_tags)
	# print(to_html(html_tags))
