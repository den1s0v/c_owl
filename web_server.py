# web_server.py

import re

from flask import Flask, request, render_template, jsonify, url_for, redirect

# # import the flask extension
# from flask_caching import Cache  

from ctrlstrct_test import process_algorithm_and_trace_from_text, process_algorithm_and_trace_from_json
from trace_gen.txt2algntr import AlgorithmParser, create_algorithm_from_text

from options import DEBUG, RUN_LOCALLY


def create_app():

	# cache = Cache(config={'CACHE_TYPE': 'simple'})

	app = Flask(__name__, template_folder='web_exp/views', static_folder='web_exp/static',)

	# bind the cache instance on to the app 
	# cache.init_app(app)

	@app.route('/index.html')
	@app.route('/index/')
	@app.route('/')
	def index():
		return render_template('index.html')
		
	@app.route('/demo/')
	@app.route('/iswc/demo/')
	def demo():
		return render_template('demo.html')
		
	@app.route('/api_test/')
	@app.route('/test/')
	def api_test():
		return render_template('api_test.html')
		
	@app.route('/favicon.ico')
	def icon():
		url = url_for('static', filename='fireball.png')
		return redirect(url)
		# return render_template('index.html')
		
	@app.errorhandler(404)
	def http_404_handler(error):
		# return "<p>HTTP 404 Error Encountered</p>", 404
		if not 'static' in request.url:
			url = url_for('static', filename=request.path)
			return redirect(url)
		
		url = url_for('index')
		return redirect(url)


	@app.route('/creating_task', methods=['POST'])
	def creating_task():
		print(request.json)
		assert 'algorithm_text' in request.json, 'Bad json!'
		res = create_algorithm_from_text(request.json['algorithm_text'].splitlines())
		if isinstance(res, AlgorithmParser):
			return dict(
				syntax_errors=(), 
				algorithm_json=res.algorithm,
				algorithm_update_lines={},
				trace_json=()
			)
		if isinstance(res, str):
			return dict(
				syntax_errors=(res,), 
				algorithm_json=None,
				algorithm_update_lines={},
				trace_json=()
			)
			
		return dict(syntax_errors=("Server error: /creating_task command is not implemented",))
	


	@app.route('/verify_trace_act', methods=['POST'])
	def make_trace_act():
		print(request.json)
		assert 'algorithm_json' in request.json, 'Bad json!'
		# res = create_algorithm_from_text(request.json['algorithm_json'].splitlines())
		# if isinstance(res, AlgorithmParser):
		# 	return dict(
		# 		syntax_errors=(), 
		# 		algorithm_json=res.algorithm,
		# 		algorithm_update_lines={},
		# 		trace_json=()
		# 	)
		# if isinstance(res, str):
		# 	return dict(
		# 		syntax_errors=(res,), 
		# 		algorithm_json=None,
		# 		algorithm_update_lines={},
		# 		trace_json=()
		# 	)
			
		# return dict(trace_line_json={"message":"Server error: /make_trace_act command is not implemented"})
	
		return dict(trace_line_json={"as_string": "Dummy act line!", "id": 49, "loop": "waiting", "executes": 7, "gen": "he", "phase": "started", "_n": 4})






	@app.route('/process_as_text', methods=['POST'])
	# caching is for debug only! Disable when is in public access!
	# @cache.cached(timeout=100)  # time seconds
	def process_data_as_text():
		try:
			feedback = process_algorithm_and_trace_as_text_request(request.json)
			return jsonify(feedback)
		except Exception as ex:
			raise ex
			return dict(messages=[f"Error processing the request - {ex.__class__.__name__}: {str(ex)}"])

	@app.route('/process_as_json', methods=['POST'])
	def process_data_as_json():
		try:
			feedback = process_algorithm_and_trace_as_json_request(request.json)
			return jsonify(feedback)
		except Exception as ex:
			raise ex
			return dict(messages=[f"Error processing the request - {ex.__class__.__name__}: {str(ex)}"])


	return app



def process_algorithm_and_trace_as_text_request(json):
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
	
	def convert_line_index_in_str(s):
		if "line" in s or "строк" in s:
			res = __LINE_IDNEX_RE.sub(lambda m: f"{m.group(1)} {convert_line_index(int(m.group(2)))}", s)
			print("Replaced line index: ", s, "->", res)
			s = res
		return s
	
	if "messages" in feedback:
		for s in feedback["messages"]:
			s = convert_line_index_in_str(s)
			formatted_feedback["messages"].append(s)
	
	if "mistakes" in feedback:
		for m in feedback["mistakes"]:
			d = {
				# ', '.join
				# "names": ([camelcase_to_snakecase(s) for s in m["classes"]]),
				"names": m["classes"],
				"act_abbr": ', '.join(str(o) for o in m["name"]),
				"explanation": '; <br>&nbsp;&nbsp; '.join(convert_line_index_in_str(o) for o in m["explanations"]),
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


def process_algorithm_and_trace_as_json_request(json):
	feedback = process_algorithm_and_trace_from_json(json, process_kwargs={'reasoning': "jena", 'debug_rdf_fpath': 'test_data/http_task_dump.rdf'})
	###
	# from pprint import pprint
	# pprint(feedback)
	
	formatted_feedback = {"messages": [], "mistakes": []}
	formatted_feedback["messages"] = feedback["messages"]
	
	if "mistakes" in feedback:
		for m in feedback["mistakes"]:
			d = {
				"names": m["classes"],
				"act_abbr": ', '.join(str(o) for o in m["name"]),
				"explanation": '; <br>&nbsp;&nbsp; '.join(m["explanations"]),
			}
			if m["text_line"]:
				d["text_line"] = m["text_line"][0],
			if "should_be_before" in m and m["should_be_before"]:
				line = m["should_be_before"][0].text_line
				if line is not None:
					d["should_be_before_line"] = line
			formatted_feedback["mistakes"].append(d)
	
	# return str(feedback)
	return formatted_feedback


__CAMELCASE_RE = re.compile(r"([a-z])([A-Z])")
__LINE_IDNEX_RE = re.compile(r"(line|строк\w+)\s*(\d+)")

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
	app = create_app()  # Flask app
	
	host = 'localhost' if RUN_LOCALLY else "109.206.169.214"
	
	if DEBUG:
		app.run(debug = DEBUG, host=host, port=2020)
	else:	
		from waitress import serve
		serve(app, host=host, port=2020)
