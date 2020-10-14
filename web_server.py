# web_server.py

import re

from flask import Flask, request, render_template, jsonify, url_for, redirect

# import the flask extension
from flask_caching import Cache  

from ctrlstrct_test import process_algorithm_and_trace_from_text


cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__, template_folder='web_exp/views', static_folder='web_exp/static',)

# bind the cache instance on to the app 
cache.init_app(app)

# @app.route('/index.html')
# @app.route('/index/')
# @app.route('/')
# @app.route('/demo/')
@app.route('/iswc/demo/')
def index():
	return render_template('index.html')
	
@app.route('/favicon.ico')
def icon():
	url = url_for('static', filename='ISWC2020_logo_v.png')
	return redirect(url)
	# return render_template('index.html')
	
@app.errorhandler(404)
def http_404_handler(error):
    # return "<p>HTTP 404 Error Encountered</p>", 404
	url = url_for('index')
	return redirect(url)

@app.route('/process', methods = ['POST'])
# caching is for debug only! Disable when is in public access!
# @cache.cached(timeout=100)  # time seconds
def process_data():
	try:
		feedback = process_algorithm_and_trace_request(request.json)
		return jsonify(feedback)
	except Exception as ex:
		raise ex
		return dict(messages=[f"Error processing the request - {ex.__class__.__name__}: {str(ex)}"])





def process_algorithm_and_trace_request(json):
	assert "alg" in json
	assert "trace" in json
	
	alg_text = json["alg"].strip()
	trace_text = json["trace"].strip()
	
	# convert data from a webpage
	
	full_text = """algorithm user_alg
{open_brace}
{alg}
{close_brace}

user_alg {boolean_chain}user_trace
{open_brace}
{trace}
{close_brace}""".format(
		alg=alg_text,
		trace=trace_text,
		boolean_chain=json["boolean_chain"] + " " if "boolean_chain" in json else '',
		open_brace="{",
		close_brace="}",
	)
	
	alg_line_i = 3
	trace_line_i = alg_line_i + len(alg_text.split("\n")) + 3
	
	print(full_text)
	print(dict(alg_line_i=alg_line_i, trace_line_i=trace_line_i))
	
	feedback = process_algorithm_and_trace_from_text(full_text)
	
	###
	# from pprint import pprint
	# pprint(feedback)
	
	formatted_feedback = {"messages": [], "mistakes": []}
	
	# convert result for use in a webpage
	def convert_line_index(i: int):
		return i - trace_line_i
	
	if "messages" in feedback:
		for s in feedback["messages"]:
			if "line" in s:
				s = __LINE_IDNEX_RE.sub(lambda s: f"line {convert_line_index(int(s.group(1)))}", s)
			formatted_feedback["messages"].append(s)
	
	if "mistakes" in feedback:
		for m in feedback["mistakes"]:
			d = {
				# ', '.join
				"names": ([camelcase_to_snakecase(s) for s in m["classes"]]),
				"act_abbr": ', '.join(str(o) for o in m["name"]),
			}
			if m["text_line"]:
				d["text_line"] = m["text_line"][0] - trace_line_i,
			if "should_be_before" in m and m["should_be_before"]:
				line = m["should_be_before"][0].text_line
				if line is not None:
					d["should_be_before_line"] = convert_line_index(line)
			formatted_feedback["mistakes"].append(d)
	
	# return str(feedback)
	return formatted_feedback


__CAMELCASE_RE = re.compile(r"([a-z])([A-Z])")
__LINE_IDNEX_RE = re.compile(r"line\s*(\d+)")

def camelcase_to_snakecase(s: str, sep='_') -> str:
	return __CAMELCASE_RE.sub(lambda m: f"{m.group(1)}{sep}{m.group(2)}", s).lower()



def debug():	
	text = """
// алгоритм 10_while
{
пока красный -> ложь,ложь // ожидание  (правильно истина,ложь)
	ждать
ждать_секунды(3)
идти
}

/* 
SKIP____10_while 10 (с.3) проверка условия (While_Loop)
10_while (с.3) проверка условия (While_Loop)
*/ {
началась программа
	начался цикл ожидание 1-й раз
		условие цикла (красный) выполнилось 1-й раз - истина // проверка условия
		началась итерация 1 цикла ожидание
			ждать выполнилось 1-й раз
		закончилась итерация 1 цикла ожидание
		условие цикла (красный) выполнилось 2-й раз - ложь
	закончился цикл ожидание 1-й раз
	ждать_секунды(3) выполнилось 1-й раз
	идти выполнилось 1-й раз
закончилась программа
}
	"""
	
	feedback = process_algorithm_and_trace_from_text(text)
	
	from pprint import pprint
	pprint(feedback)


if __name__ == "__main__":
	# debug()
	app.run(debug = 1, port=2020)
	# app.run(debug = 1, host="109.206.169.214", port=2020)
	

