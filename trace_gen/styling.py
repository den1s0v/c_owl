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

Discovered later: Stan - HTML construction with Python code http://docs.g-vo.org/meetstan.html
Found there: https://wiki.python.org/moin/Templating

'''



import re


def make_lexer():
	'''create and return lexer function
	that recieves a string with tokens
	and returns a 2-tuple:
		0) count of chars consumed by token
		1) type of token found or None
	'''
	keyword_re = re.compile(r"(?:начался|началась|началось|began|закончился|закончилась|закончилось|ended|выполнился|выполнилась|выполнилось|executed|evaluated|calculated|если|иначе|делать|пока|для|от|до|шаг|с\s+шагом|if|else|do|while|for|from|to|with\s+step|step|каждого|в|из|по|к|foreach|each|in)(?=\s|\b|$)", re.I)

	struct_re = re.compile(r"(?:развилка|развилки|альтернативная|ветка|branch|alternative|условия|переход|update|итерация|iteration|иначe|условие|цикла|condition|of|loop|инициализация|init|initialization|цикл|следование|sequence)(?=\s|\b|$)", re.I)

	simple_mode = {
	  # The start state contains the rules that are intially used
	  'start': [
		{'regex': keyword_re, 'token': "keyword"},
		{'regex': re.compile(r"true|false|ложь|истина|not evaluated|не вычислено", re.I), 'token': "atom"},
		{'regex': re.compile(r"([\"])(?:\.|[^\"'])*\1", re.I), 'token': "string"},
		{'regex': re.compile(r"\d+(?:st|nd|rd|th)?", re.I),
		  # /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
		 'token': "number"},
		{'regex': re.compile(r"(?:\/\/|#).*"), 'token': "comment"},
		{'regex': struct_re, 'token': "struct"},
		{'regex': re.compile(r"действие|action|statement|stmt", re.I), 'token': "action"},
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

def parse_line(line: str) -> '[(token, style), ...]':
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


def prepare_tags_for_line(line: str) -> list:
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

# duplicate of txt2algntr.find_by_key_in(), for access convenience
def find_by_key_in(key, dict_or_list, _not_entry=None):
    _not_entry = _not_entry or set()
    _not_entry.add(id(dict_or_list))
    if isinstance(dict_or_list, dict):
        for k, v in dict_or_list.items():
            if k == key:
                yield dict_or_list
            elif id(v) not in _not_entry:
                yield from find_by_key_in(key, v, _not_entry)
    elif isinstance(dict_or_list, (list, tuple, set)):
        for d in dict_or_list:
            if id(d) not in _not_entry:
                yield from find_by_key_in(key, d, _not_entry)


def inline_class_as_style(html_tags, CSS_string=None):
	'insert css as `style=` attribute instead of `class=` and styles defined elsewhere'
	if not CSS_string:
		return html_tags
	
	cls2style = {}
	
	for html_tag in find_by_key_in("attributes", html_tags):
		attributes = html_tag["attributes"]
		if "class" not in attributes:
			continue
			
		css_classes = attributes["class"]
		for cls in css_classes[:]:
			if not cls:
				# remove this empty class
				css_classes.remove(cls)
				continue
			###
			# print("cls:", cls)
			###
			css = None
			if cls not in cls2style:
				pattern = r'\b' + cls + r'\s*\{([^}]+?)\}'
				RE_CSS_STYLE = re.compile(pattern)
				m = RE_CSS_STYLE.search(CSS_string)
				if m:
					css = m[1].strip()
				cls2style[cls] = css  # even if None
			else:
				css = cls2style[cls]
			
			if not css:
				# print("::debug::  skip CSS class", cls)
				continue
				
			existing_style = html_tag["attributes"].get("style", [])  # stored as array
			existing_style.append(css)
			# set or reassign
			html_tag["attributes"]["style"] = existing_style
			
			# remove class replaced with CSS
			css_classes.remove(cls)
			
		# remove class key if empty
		if not css_classes:
			del html_tag["attributes"]["class"]
	return html_tags
	

if __name__ == '__main__':
	# print(__doc__)

	from pprint import pprint
	tt = """
branch ELSE of name began 
	""".strip()
	
	for t in tt.splitlines():
		html_tags = prepare_tags_for_line(t.strip())
		print(to_html(html_tags))

	
	exit()
	
	###

	html_tags = prepare_tags_for_line("условие не_зелёный выполнилось 1-й раз - истина")
	pprint(html_tags)
	
	STYLE_HEAD = '''<style type="text/css" media="screen">
		span.algorithm {
		  font-family: courier; font-size: 10pt;
		}
		# div {
		#     border: 1px solid #000000;
		# }

		span.string { color: #555; font-style: italic }
		span.atom { color: #f08; font-style: italic; font-weight: bold; }
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
	
	# inline_class_as_style(html_tags, STYLE_HEAD)
	pprint(html_tags)
	print(to_html(html_tags))
