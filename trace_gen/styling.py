# styling.py
'''Format algorithm & trace textual representation as colored HTML

A piece of HTML is a plain string or dict (the same as JS object) (see below).

The basic structure of HTML tag as Python dict:
{
    "tag": "span",
    "attributes": {"class": ["variable", "more", "classes"], "act_type": ["performed"]},
    "content": "plain text or list of another HTML-tag-like dicts"
}

The resulting HTML should be something like this:

<span class="variable more classes" act_type="performed">
    plain text or list of another HTML-tag-like dicts
</span>


See also: `to_html()` function below for how to convert html_tags to HTML string.
'''



import re

from trace_gen.json2alg2tr import tr, set_target_lang, get_target_lang


def make_lexer():
    '''create and return lexer function 
    that recieves a string with tokens 
    and returns a 2-tuple:
        0) count of chars consumed by token
        1) type of token found or None
    '''
    keyword_re = re.compile(r"(?:начался|началась|началось|began|закончился|закончилась|закончилось|ended|выполнился|выполнилась|выполнилось|executed|evaluated|calculated|если|иначе|делать|пока|для|от|до|шаг|с\s+шагом|if|else|do|while|for|from|to|with\s+step|step|каждого|в|из|по|к|foreach|each|in)(?=\s|$)", re.I)

    struct_re = re.compile(r"развилка|развилки|альтернативная|ветка|branch|alternative|условия|переход|update|итерация|iteration|иначe|условие|цикла|condition|of|loop|инициализация|init|initialization|цикл|следование|sequence", re.I)

    simple_mode = {
      # The start state contains the rules that are intially used
      'start': [
        {'regex': keyword_re, 'token': "keyword"},
        {'regex': re.compile(r"true|false|ложь|истина", re.I), 'token': "atom"},
        {'regex': re.compile(r"\d+(?:st|nd|rd|th)?", re.I),
          # /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
         'token': "number"},
        {'regex': re.compile(r"(?:\/\/|#).*"), 'token': "comment"},
        {'regex': struct_re, 'token': "struct"},
        {'regex': re.compile(r"действие|action", re.I), 'token': "action"},
        {'regex': re.compile(r"программа|program", re.I), 'token': "program"},
        {'regex': re.compile(r"функция|function", re.I), 'token': "function"},
        {'regex': re.compile(r"й|раз|time", re.I), 'token': None},
        {'regex': re.compile(r"[\wа-яё\d]+", re.I), 'token': "variable"}
      ],
    }
    
    state = 'start'
    def lexer(token) -> (int, str or None):
        for matcher in simple_mode[state]:
            m = matcher['regex'].match(token)
            if m:
                return len(m[0]), matcher['token']
            # else:
            #     print("No match for:", matcher['token'], token)
        return 1, None  # consume 1 char anyway
    
    return lexer


_lexer = make_lexer()

def parse_line(line) -> '[(token, style), ...]':
    tokens = []
    while(line):
        L, style = _lexer(line)
        tok = line[:L]  # .strip()
        if not style and tokens and (not tokens[-1][1]):
            tokens[-1] = (tokens[-1][0] + tok, style)
        else:
            tokens.append((tok, style))
        line = line[L:] # .lstrip()
    return tokens
        

# def wrap_word(word, style=None) -> str:
#     if style:
#         return f'<span class="{style}">{word}</span>'
#     else:
#         return word
        
# def wrap_tags(text) -> str:
#     html = "<div class=\"\">"
#     lines = text.splitlines()
#     for line in lines:
#         leading_spaces = len(line) - len(line.lstrip())
#         html += "&nbsp;" * leading_spaces
#         html += '<span class="">'
#         for word, style in parse_line(line.lstrip()):
#             html += wrap_word(word, style)
            
#         html += "</span>\n<br>\n"
#     return html + "</div>"

def prepare_tag_for_word(word, style=None) -> str:
    if style:
        return {
            "tag": "span",
            "attributes": {"class": [style]},  #, "act_type": "performed"
            "content": word
        }
    return word  # otherwise, no tag required


def prepare_tags_for_line(line) -> list:
    elements = []
    leading_spaces = len(line) - len(line.lstrip())
    if leading_spaces > 0:
        elements += ["&nbsp;" * leading_spaces]
    elements += [prepare_tag_for_word(word, style) for word, style in parse_line(line.lstrip())]
    return elements


def prepare_tags_for_text(multiline_text) -> dict:
    html = {'tag': "div", "content": []}
    lines = multiline_text.splitlines()
    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        if leading_spaces > 0:
            html["content"] += ["&nbsp;" * leading_spaces]
        
        html["content"] += prepare_tags_for_line(line.lstrip())
        html["content"] += [{"tag": "br"}]
    return html


def to_html(element: str or dict or list, sep='') -> str:
    if not element:
        return ''
        
    if isinstance(element, (str, int)):
        return str(element)
        
    if isinstance(element, (list, tuple)):
        inner = sep.join(map(to_html, element))
        return inner
    
    if isinstance(element, dict):
        tag = element.get('tag', "")
        attrs = ''.join(f' %s="%s"' % (k, to_html(v, sep=" ").replace('"', r'')) for k, v in element.get('attributes', {}).items())
        # inner = ''.join(map(to_html, element.get('content', ())))
        inner = to_html(element.get('content', ()))
        if not tag:
            return inner
            
        head = f'<{tag}{attrs}'
        if inner or attrs:
        	# full form
            html = f'{head}>{inner}</{tag}>'
        else:
        	# short form
            html = f'{head} />'
        return html
    
    return 'UNKNOWN(%s)' % type(element).__name__
    

INDENT_STEP = 2  # spaces
SIMPLE_NODE_STATES = ('performed', )
COMPLEX_NODE_STATES = ('started', 'finished')

BUTTON_TIP_FREFIX = {
    "ru": {
        'performed': 'Выполнится',
        'started': 'Начнётся',
        'finished': 'Закончится',
    },
    "en": {
        'performed': 'Perform',
        'started': 'Start',
        'finished': 'Finish',
    }
}

def set_indent_step(step: int):
    global INDENT_STEP
    INDENT_STEP = step

    
# features of: Pseudocode / С / Python / JavaScript / etc.
# token : function(str or tag) -> tag or tags
SYNTAX = {}

def set_syntax(programming_language_name: str):
    name = programming_language_name.capitalize()
    SYNTAX["name"] = name
    passthrough = lambda tag: tag;
    call_tr = lambda s: tr(s);
    
    if name in ("Pseudocode", ):
        SYNTAX["BLOCK_OPEN"] = lambda: []
        SYNTAX["BLOCK_CLOSE"] = lambda: []
        SYNTAX["COMMENT"] = lambda tag: ["// ", tag]
        SYNTAX["CONDITION"] = passthrough
        SYNTAX["DO_KEYWORD"] = call_tr
        SYNTAX["ELSEIF_KEYWORD"] = call_tr
        SYNTAX["STATEMENT"] = passthrough
        SYNTAX["WHILE_KEYWORD"] = call_tr
    
    elif name in ("C", "Си"):
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


set_syntax("C")  # the default
# set_syntax("Pseudocode")  # the default
# set_syntax("Python")


# def escape_quotes(s):
#     'HTML-escape quotes'
#     return s.replace("'", '&apos;').replace('"', r'&quot;')
#     # .replace('\\', '\\\\')

def _get_act_button_tip(act_name_json, phase):
    lang = get_target_lang()
    return BUTTON_TIP_FREFIX[lang][phase] + " " + (act_name_json.replace("'", '"'))


def _make_alg_tag(alg_node, token_type, inner='', states=None):
    more_attrs = {}
    if alg_node:
        id_ = alg_node["id"]
        more_attrs.update({"algorithm_element_id": [id_], })
    
    if states:
        act_name = alg_node["act_name"]
        # вычислить целевое состояние по последнему акту трассы
        # ... TODO
        state_name = states[0]  # 'performed'
        # ...
        
        states_attr = {state: _get_act_button_tip(act_name, state) for state in states}
        BUTTON_TIPS[id_] = states_attr
        # states_attr = escape_quotes(str(states_attr))
        # more_attrs.update({"act_types": [states_attr]})
        inner = [
        	# <i class="play icon"></i>
	        {
		        "tag": "span",
		        "attributes": {
		        	"class": ["hidable tooltip"],
		        	"algorithm_element_id": [str(id_)], 
		        	"state": [state_name], 
		        	# **states_attr,
		        	"onclick": ["on_algorithm_element_clicked(this)"], # `onmouseup` event works too.
	        	},
		        "content": [{
				        "tag": "i",
				        "attributes": {
				        	"class": ["play", "icon"],
			        	},
				        "content": ''
		        	},
		        	{
				        "tag": "span",
				        "attributes": {
				        	"class": ["tooltiptext"],
			        	},
				        "content": states_attr[state_name]
		        	}
	        	]
        	},
        	inner
    	]
    
    return {
        "tag": "span",
        "attributes": {"class": [token_type], **more_attrs},
        "content": inner
    }


def _make_line_tag(indent, inner=''):
    return {
        "tag": "div",
        "attributes": {"class": ['line'], "style": ['margin-left: %dem;' % indent]},
        "content": inner
    }

BUTTON_TIPS = {}  # подсказки к кнопкам (в теги не получилось вставить - вернём отдельно)

def get_button_tips():
    return BUTTON_TIPS

def algorithm_to_tags(algorithm_json:dict or list, user_language: str=None, syntax:str=None, indent=0) -> list:
    """ Create new tree of html-tags with additional info about nodes """
    if user_language:
        set_target_lang(user_language)  # usually set once on the topmost recursive call
        BUTTON_TIPS.clear()
    if syntax:
        set_syntax(syntax)  # usually set once on the topmost recursive call
        
    if isinstance(algorithm_json, (list, tuple)):
        return [algorithm_to_tags(el, indent=indent) for el in algorithm_json]
    
    if isinstance(algorithm_json, str):
        assert 0, algorithm_json
        # return algorithm_json
        
    if isinstance(algorithm_json, dict):
        if algorithm_json["type"] == "algorithm":
            algorithm_json = algorithm_json["entry_point"]
            
        # id_ = algorithm_json["id"]
        type_ = algorithm_json["type"]
        name = algorithm_json["name"]
        # act_name = algorithm_json["act_name"]
            
        if type_ in ("expr", ):
            return _make_alg_tag(algorithm_json, "variable button", name, states=SIMPLE_NODE_STATES)
        
        if type_ in ("stmt", ):
            return _make_line_tag(indent, SYNTAX["STATEMENT"](_make_alg_tag(algorithm_json, "variable button", name, states=SIMPLE_NODE_STATES)))
        
        elif type_ == "sequence":  # and not name.endswith("_loop_body"):
            # # recurse with list
            # return algorithm_to_tags(algorithm_json["body"], indent=indent)  # indent++ ??
            # list of lines
            # return [_make_line_tag(indent, algorithm_to_tags(el, indent=indent)) for el in algorithm_json["body"]]
            return [(algorithm_to_tags(el, indent=indent)) for el in algorithm_json["body"]]
            
        elif type_.endswith("_loop"):
            loop_type = type_.replace("_loop", '')
            
            if loop_type == 'while':
                return [
                    # заголовок цикла
                    _make_line_tag(indent, [
                        _make_alg_tag(algorithm_json, 'keyword button', 
                            inner=SYNTAX["WHILE_KEYWORD"](loop_type),
                            states=COMPLEX_NODE_STATES),
                        "&nbsp;",
                        *SYNTAX["CONDITION"](algorithm_to_tags(algorithm_json["cond"])),
                        "&nbsp;" * 2,
                        _make_alg_tag(None, 'comment', 
                            inner=SYNTAX["COMMENT"](name))
                    ]),
                    # кнопка для тела цикла
                    _make_line_tag(indent, 
                        _make_alg_tag(algorithm_json["body"], 'button', 
                            inner=[
		                        *SYNTAX["BLOCK_OPEN"](),
		                        "&nbsp;" * (INDENT_STEP),
                            ],
                            states=COMPLEX_NODE_STATES)
                        ),
                    # тело цикла
                    algorithm_to_tags(algorithm_json["body"], indent=indent + INDENT_STEP),
                    # закрыть тело цикла (если требуется по синтаксису)
                    *(SYNTAX["BLOCK_CLOSE"]() and [_make_line_tag(indent, SYNTAX["BLOCK_CLOSE"]())]),
                ]
                
            if loop_type == 'do_while':
                # заголовок цикла
                header_line = _make_line_tag(indent, [])
                if SYNTAX["DO_KEYWORD"]:
                    # syntax like C++/Java with do-while loop 
                    header_line["content"] += [
                        _make_alg_tag(algorithm_json, 'keyword button', 
                            inner=SYNTAX["DO_KEYWORD"](loop_type),
                            states=COMPLEX_NODE_STATES),
                        # "&nbsp;",
                        # *SYNTAX["CONDITION"](algorithm_to_tags(algorithm_json["cond"])),
                        "&nbsp;" * 2,
                        _make_alg_tag(None, 'comment', 
                            inner=SYNTAX["COMMENT"](name))
                    ];
                else:
                    # Python case: emulate with `WHILE(TRUE): IF(): BREAK`.
                    header_line["content"] += ['==Python не поддерживает DO-WHILE==']
                    
                # кнопка для тела цикла
                body_start_line = _make_line_tag(indent, 
                    _make_alg_tag(algorithm_json["body"], 'button', 
                        inner=[
	                        *SYNTAX["BLOCK_OPEN"](),
	                        "&nbsp;" * (INDENT_STEP),
                        ],
                        states=COMPLEX_NODE_STATES)
                    )
                # тело цикла
                body_lines = algorithm_to_tags(algorithm_json["body"], indent=indent + INDENT_STEP)
                
                if not SYNTAX["DO_KEYWORD"]:
                    # TODO: Python case: emulate with `IF(): BREAK`
                    footer_line = []
                
                # закрыть тело цикла (если требуется по синтаксису)
                body_end_lines = (SYNTAX["BLOCK_CLOSE"]() and [_make_line_tag(indent, SYNTAX["BLOCK_CLOSE"]())])
                
                if SYNTAX["DO_KEYWORD"]:
                    footer_line = _make_line_tag(indent, [
                        _make_alg_tag(None, 'keyword button', 
                                    inner=SYNTAX["WHILE_KEYWORD"](loop_type)),
                        "&nbsp;",
                        *SYNTAX["STATEMENT"](SYNTAX["CONDITION"](algorithm_to_tags(algorithm_json["cond"]))),
                    ])
                    
                return [
                    header_line,
                    body_start_line,
                    *body_lines,
                    *body_end_lines,
                    footer_line
                ]
                
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
                        _make_alg_tag(algorithm_json, 'keyword button',
                            inner=tr(branch["type"]) if SYNTAX["name"] == 'Pseudocode' else branch["type"],
                            states=COMPLEX_NODE_STATES))
                else:
                    # добавить просто ключевое слово - начало ветки
                    line["content"].append(
                        _make_alg_tag(algorithm_json, 'keyword',
                            inner=SYNTAX["ELSEIF_KEYWORD"](branch["type"]),
                            states=None))
                    
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
                
                # кнопка для тела ветки
                result.append(_make_line_tag(indent, 
                    _make_alg_tag(branch, 'button', 
                        inner=[
	                        *SYNTAX["BLOCK_OPEN"](),
	                        "&nbsp;" * (INDENT_STEP),
                        ],
                        states=COMPLEX_NODE_STATES)
                    ))

                # тело ветки
                result += algorithm_to_tags(branch["body"], indent=indent + INDENT_STEP)
                
                # закрыть тело ветки (если требуется по синтаксису)
                result += (SYNTAX["BLOCK_CLOSE"]() and _make_line_tag(indent, SYNTAX["BLOCK_CLOSE"]())),
                
            return result

    return ''


if __name__ == '__main__':
    # print(__doc__)
    
    from pprint import pprint
    html_tags = prepare_tags_for_line("условие не_зелёный выполнилось 1-й раз - истина")
    pprint(html_tags)
    print(to_html(html_tags))
