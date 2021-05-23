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

	struct_re = re.compile(r"развилка|развилки|альтернативная|ветка|branch|alternative|условия|переход|update|итерация|iteration|иначe|условие|цикла|condition|of|loop|инициализация|init|initialization|цикл|следование|sequence", re.I)

	simple_mode = {
	  # The start state contains the rules that are intially used
	  'start': [
		{'regex': keyword_re, 'token': "keyword"},
		{'regex': re.compile(r"true|false|ложь|истина|not evaluated|не вычислено", re.I), 'token': "atom"},
		{'regex': re.compile(r"\d+(?:st|nd|rd|th)?", re.I),
		  # /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
		 'token': "number"},
		{'regex': re.compile(r"(?:\/\/|#).*"), 'token': "comment"},
		{'regex': struct_re, 'token': "struct"},
		{'regex': re.compile(r"действие|action|statement", re.I), 'token': "action"},
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



if __name__ == '__main__':
	# print(__doc__)

	from pprint import pprint
	html_tags = prepare_tags_for_line("условие не_зелёный выполнилось 1-й раз - истина")
	pprint(html_tags)
	print(to_html(html_tags))
