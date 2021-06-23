# web_server.py

import re
import sys

from flask import Flask, request, render_template, jsonify, url_for, redirect

# # import the flask extension
# from flask_caching import Cache

from ctrlstrct_test import process_algorithm_and_trace_from_text, process_algorithm_and_trace_from_json, make_act_json, process_algorithms_and_traces, add_styling_to_trace
from ctrlstrct_run import make_trace_for_algorithm
from trace_gen.txt2algntr import AlgorithmParser, create_algorithm_from_text
from trace_gen.blockly_helpers import create_algorithm_from_blockly_xml
import trace_gen.styling as styling
import trace_gen.syntax as syntax
from trace_gen.json2alg2tr import set_target_lang

from common_helpers import Checkpointer, camelcase_to_snakecase

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

	@app.route('/blockly_test/<lang>/')
	@app.route('/blockly_test/')
	def blockly_test(lang='en'):
		return render_template('blockly_test.html', language=lang)

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
		return '<p>HTTP 404 Error Encountered</p><p>Requested URL: %s</p>Get me <a href="%s">Home</a>' % (request.url, url), 404
		# return redirect(url)


	@app.route('/available_syntaxes', methods=['GET'])
	def available_syntaxes():
		return {"available_syntaxes": ["C++", "Java", "Python", ]}


	@app.route('/creating_task', methods=['POST'])
	def creating_task():
		# print(request.json)
		try:
			assert 'algorithm_text' in request.json, 'Bad json: No "algorithm_text" key in JSON payload!'

			algorithm_text = request.json['algorithm_text']
			user_language = request.json.get('user_language', 'en')
			set_target_lang(user_language)
			if algorithm_text.startswith("<xml"):
				res = create_algorithm_from_blockly_xml(algorithm_text)
			else:
				res = create_algorithm_from_text(algorithm_text.splitlines())

			# if error
			assert not isinstance(res, str), res

			if isinstance(res, AlgorithmParser):
				###
				# from pprint import pprint
				# pprint(res.algorithm)

				# trace_json = ()
				trace_json = make_trace_for_algorithm(res.algorithm)
				trace_json = add_styling_to_trace(res.algorithm, trace_json, user_language)

				# if error
				assert not isinstance(trace_json, str), trace_json

				algorithm_tags = syntax.algorithm_to_tags(res.algorithm, user_language, request.json.get('syntax', request.json.get('task_lang', 'C')))
				algorithm_html = styling.to_html(algorithm_tags)

				return dict(
					syntax_errors=(),
					algorithm_json=res.algorithm,
					algorithm_as_html=algorithm_html,
					trace_json=trace_json
				)

		except Exception as ex:
			res = f"{type(ex)}: {ex}"
			print_exception(ex)
			print("request.json :")
			print(request.json)
			print("The error above reported as response, continue.")
			return dict(
				syntax_errors=(res,),
				algorithm_json=None,
				algorithm_as_html=None,
				trace_json=()
			)

		return dict(syntax_errors=("Server error: /creating_task command is not implemented",))  # debug



	@app.route('/verify_trace_act', methods=['POST'])
	def verify_trace_act():
		### print(request.json)
		ch = Checkpointer()
		try:
			assert 'algorithm_json' in request.json, 'Bad json: No "algorithm_json" key in JSON payload!'

			user_language = request.json.get('user_language', 'en')
			set_target_lang(user_language)
			ch.hit("set target lang")

			# extend the trace
			res = make_act_json(**{
				k:v for k,v in request.json.items() if k in ("algorithm_json", "algorithm_element_id", "act_type", "existing_trace_json", "user_language")
				})
			ch.hit("make acts")

			# if error
			assert not isinstance(res, str), res

			if isinstance(res, list):

				algorithm_json = request.json["algorithm_json"]

				# verify the obtained trace with reasoner
				full_trace = res
				alg_tr = {
				    "trace_name"    : "http_trace",
				    "algorithm_name": "http",
				    "trace"         : full_trace,
				    "algorithm"     : algorithm_json,
				    "header_boolean_chain" : '',   # leave empty
				}
				# update acts data (inplace): write mistake explanations
				_mistakes, err_msg = process_algorithms_and_traces([alg_tr], write_mistakes_to_acts=True)

				assert not err_msg, err_msg
				ch.hit("process algorithms and traces")

				### print("After reasoning: ", *full_trace, sep='\n *\t')

				algorithm_tags = syntax.algorithm_to_tags(algorithm_json, user_language, request.json.get('syntax', request.json.get('task_lang', 'C')), existing_trace=full_trace)
				algorithm_html = styling.to_html(algorithm_tags)
				ch.hit("HTML prepared")
				ch.since_start("Finished processing the request in")

				return dict(
					full_trace_json=full_trace,  ## res,
					algorithm_json=algorithm_json,  # pass back
					algorithm_as_html=algorithm_html,
					processing_errors=(),
				)
		except Exception as ex:
			res = f"{type(ex)}: {ex}"
			print_exception(ex)
			print("request.json :")
			print(request.json)
			ch.since_start("Finished the request with exception in")
			return dict(
				processing_errors=(res,),
				full_trace_json=(),
				algorithm_json=None,
				algorithm_as_html=None,
			)
			print("The error above reported as response, continue.")

		return dict(trace_line_json={"as_string": "Dummy act line!", "id": 49, "loop": "waiting", "executes": 7, "gen": "he", "phase": "started", "_n": 4})  # debug



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

	# @app.route('/process_as_json', methods=['POST'])
	# def process_data_as_json():
	# 	try:
	# 		feedback = process_algorithm_and_trace_as_json_request(request.json)
	# 		return jsonify(feedback)
	# 	except Exception as ex:
	# 		raise ex
	# 		return dict(messages=[f"Error processing the request - {ex.__class__.__name__}: {str(ex)}"])


	return app

def print_exception(ex, print_args=()):
	import traceback
	print(''.join(traceback.format_exception(etype=type(ex), value=ex, tb=ex.__traceback__)))
	if print_args: print(*print_args)


def process_algorithm_and_trace_as_text_request(json):
	assert "alg" in json
	assert "trace" in json

	# should create var on first execution
	if '__LINE_IDNEX_RE' not in globals():
		global __LINE_IDNEX_RE
		__LINE_IDNEX_RE = re.compile(r"(line|строк\w+)\s*(\d+)")

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


if __name__ == "__main__":
	host = None
	port = None

	# check if something config passed from command line
	for arg in sys.argv[1:]:
		if arg.startswith('host='):
			host = arg.replace('host=', '')
			print("Using host specified on command line:", host)
		elif arg.startswith('port='):
			port = arg.replace('port=', '')
			print("Using port specified on command line:", port)


	app = create_app()  # Flask app

	host = host or ('localhost' if RUN_LOCALLY else "109.206.169.214")
	port = port or 2020

	if DEBUG:
		app.run(debug=DEBUG, host=host, port=port)
	else:
		from waitress import serve
		serve(app, host=host, port=port)
