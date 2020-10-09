# web_server.py

# from flask import Flask

from ctrlstrct_test import process_algorithm_and_trace_from_text
 
# app = Flask(__name__)
 
# @app.route("/")
# def hello():
#     return "Hello, World!"
  
if __name__ == "__main__":
	# app.run()
	
	text = """
// алгоритм 10_while
{
пока красный -> ложь,ложь // ожидание
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
