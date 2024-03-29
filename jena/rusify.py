# rusify.py

'''
Convert trace lines for CompPrehension questions from EN to RU (inline)
'''

import json
import re


json_in_file = "control-flow-statements-domain-questions_0.json"
json_out_file = "control-flow-statements-domain-questions.json"
strings_file = "extracts-en.txt"
translates_file = "extracts-ru.txt"

def extract_strings():
	with open(json_in_file) as f:
		data = json.load(f)
		
	with open(strings_file, "w") as f:
		for q in data:
			qdata = q.get("questionData")
			answerObjects = qdata["answerObjects"]
			for ao in answerObjects:
				f.write(ao["hyperText"])
				f.write('\n')
				f.write(ao["domainInfo"].split(':', maxsplit=2)[-1])
				f.write('\n' * 2)


def translate_strings():
	with open(json_in_file) as f:
		data = json.load(f)
		
	for q in data:
		qdata = q.get("questionData")
		# answerObjects = qdata["answerObjects"]
		# for ao in answerObjects:
		# 	t = ao["hyperText"]
		# 	t2 = replace_in_text(t)
		# 	assert t2 != t, t
		# 	ao["hyperText"] = t2
			
		# 	t = ao["domainInfo"].split(':', maxsplit=2)[-1]
		# 	t2 = replace_in_text(t)
		# 	assert t2 != t, t
		# 	ao["domainInfo"] = ao["domainInfo"].replace(t, t2)
		t = qdata["questionText"]
		### print(len(t)); continue
		t2 = replace_in_text(t)
		assert t2 != t, t
		# t2 = replace_in_text(t2)
		qdata["questionText"] = t2
		
		
			
	# write it back
	with open(json_out_file + '.ru'*0, "w") as f:
		json.dump(data, f, indent=2)


def add_questionName():
	with open(json_in_file) as f:
		data = json.load(f)
		
	for q in data:
		qdata = q.get("questionData")
		statementFacts = qdata["statementFacts"]
		qname = None
		for fact in statementFacts:
			if fact["verb"] == "algorithm_name":
				qname = fact["object"]
				break
		if qname:
			qdata["questionName"] = qname
		else:
			print('questionName was not found ...')
			
	# write it back
	with open(json_in_file, "w") as f:
		json.dump(data, f, indent=2)


def replace_in_text(text=None):
	if not text:
		with open(strings_file) as f:
			text = f.read()
	
	# hard patch
	text = text.replace('Start ELSE branch of alternative choice-else', 'Закончить ветку ИНАЧЕ развилки choice')

	text = text.replace('begin program', 'начать программу')
	text = text.replace('<span class="program">program</span> <span class="keyword">began</span>', '<span class="program">программа</span> <span class="keyword">началась</span>')
	text = text.replace('end program', 'закончить программу')
	text = text.replace('<span class="program">program</span> <span class="keyword">ended</span>', '<span class="program">программа</span> <span class="keyword">закончилась</span>')
	
	
	text = text.replace('execute statement', 'выполнить действие')
	text = text.replace('Perform statement', 'Выполнить действие')
	text = re.sub('<span class="action">statement</span> (.+?) <span class="keyword">executed</span>', r'<span class="action">действие</span> \1 <span class="keyword">выполнено</span>', text)


	text = text.replace('evaluate condition', 'вычислить условие')
	text = text.replace('Perform condition', 'Вычислить условие')
	text = re.sub('<span class="struct">condition</span> (.+?) <span class="keyword">evaluated</span>', r'<span class="struct">условие</span> \1 <span class="keyword">вычислено</span>', text)


	text = text.replace('begin alternative', 'начать развилку')
	text = text.replace('Start alternative', 'Начать развилку')
	text = re.sub(r'(?:^|:)<span class="struct">alternative</span> (.+?) <span class="keyword">began</span>', r'<span class="struct">развилка</span> \1 <span class="keyword">началась</span>', text, flags=re.M)
	text = text.replace('end alternative', 'закончить развилку')
	text = text.replace('Finish alternative', 'Закончить развилку')
	text = re.sub(r'(?:^|:)<span class="struct">alternative</span> (.+?) <span class="keyword">ended</span>', r'<span class="struct">развилка</span> \1 <span class="keyword">закончилась</span>', text, flags=re.M)


	text = re.sub('begin (.+?) branch with condition', r'начать ветку \1 с условием', text)
	text = re.sub('Start (.+?) branch with condition', r'Начать ветку \1 с условием', text)
	text = re.sub('<span (.+?) <span class="struct">branch</span> <span class="variable">with</span> <span class="struct">condition</span> (.+?) <span class="keyword">began</span>', r'<span class="struct">ветка</span> <span \1 <span class="struct">с условием</span> \2 <span class="keyword">началась</span>', text)
	text = re.sub('end (.+?) branch with condition', r'закончить ветку \1 с условием', text)
	text = re.sub('Finish (.+?) branch with condition', r'Закончить ветку \1 с условием', text)
	text = re.sub('<span (.+?) <span class="struct">branch</span> <span class="variable">with</span> <span class="struct">condition</span> (.+?) <span class="keyword">ended</span>', r'<span class="struct">ветка</span> <span \1 <span class="struct">с условием</span> \2 <span class="keyword">закончилась</span>', text)
	

	text = re.sub('begin (ELSE) branch of alternative', r'начать ветку \1 развилки', text)
	text = re.sub(r'Start (ELSE) branch of alternative (\S+)-else', r'Начать ветку ИНАЧЕ развилки \2', text)
	text = re.sub('<span class="keyword">ELSE</span> <span class="struct">branch</span> <span class="struct">of</span> <span class="struct">alternative</span> (.+?) <span class="keyword">began</span>', r'<span class="struct">ветка</span> <span class="keyword">ELSE</span> <span class="struct">развилки</span> \1 <span class="keyword">началась</span>', text)
	text = re.sub('end (ELSE) branch of alternative', r'закончить ветку \1 развилки', text)
	text = re.sub(r'Finish (ELSE) branch of alternative (\S+)-else', r'Закончить ветку ИНАЧЕ развилки \2', text)
	text = re.sub('<span class="keyword">ELSE</span> <span class="struct">branch</span> <span class="struct">of</span> <span class="struct">alternative</span> (.+?) <span class="keyword">ended</span>', r'<span class="struct">ветка</span> <span class="keyword">ELSE</span> <span class="struct">развилки</span> \1 <span class="keyword">закончилась</span>', text)
	

	text = text.replace('begin loop', 'начать цикл')
	text = text.replace('Start loop', 'Начать цикл')
	text = re.sub(r'(?:^|:)<span class="struct">loop</span> (.+?) <span class="keyword">began</span>', r'<span class="struct">цикл</span> \1 <span class="keyword">начался</span>', text, flags=re.M)
	text = text.replace('end loop', 'закончить цикл')
	text = text.replace('Finish loop', 'Закончить цикл')
	text = re.sub(r'(?:^|:)<span class="struct">loop</span> (.+?) <span class="keyword">ended</span>', r'<span class="struct">цикл</span> \1 <span class="keyword">закончился</span>', text, flags=re.M)


	text = text.replace('begin iteration of loop', 'начать итерацию цикла')
	text = text.replace('Start iteration of loop', 'Начать итерацию цикла')
	text = re.sub(r'<span class="struct">iteration</span> <span class="struct">of</span> <span class="struct">loop</span> (.+?) <span class="keyword">began</span>', r'<span class="struct">итерация цикла</span> \1 <span class="keyword">началась</span>', text)
	text = text.replace('end iteration of loop', 'закончить итерацию цикла')
	text = text.replace('Finish iteration of loop', 'Закончить итерацию цикла')
	text = re.sub(r'<span class="struct">iteration</span> <span class="struct">of</span> <span class="struct">loop</span> (.+?) <span class="keyword">ended</span>', r'<span class="struct">итерация цикла</span> \1 <span class="keyword">закончилась</span>', text)

	# tricks patches
	text = re.sub('Finish (.+?) с условием', r'Закончить ветку \1 с условием', text)
	text = re.sub(r'Finish (\S*?IF)', r'Закончить ветку \1', text)
	
	text = re.sub('Start (.+?) с условием', r'Начать ветку \1 с условием', text)
	text = re.sub(r'Start (\S*?IF)', r'Начать ветку \1', text)


	return text

if __name__ == '__main__':
	# extract_strings()
	
	# print(re.sub('a(.+?)b', r'AAA \1 BBB', "axxb"))
	# print(re.search(r'(?:^|:)a(.+?)b', "x\naxxb", re.M))
	# text = """X\n<span class="struct">alternative</span> '<span class="variable">checking_red</span>' <span class="keyword">began</span>"""
	# text = re.sub(r'(?:^|:)<span class="struct">alternative</span> (.+?) <span class="keyword">began</span>', r'<span class="struct">развилка</span> \1 <span class="keyword">началась</span>', text, flags=re.M)
	# print(text)

	# exit()
	
	
	# text = replace_in_text()
	# with open(translates_file, "w") as f:
	# 	f.write(text)
	
	print(replace_in_text("Start ELSE branch of alternative choice-else"))
	print(replace_in_text("Start ELSE branch of alternative choice-else"))
	
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	# print(replace_in_text("title=\"Start loop over_first\""))
	# print(replace_in_text("title=\"Finish loop over_first\""))
	# print(replace_in_text("title=\"Start iteration of loop over_first\""))
	# print(replace_in_text("title=\"Finish iteration of loop over_first\""))
	
	translate_strings()
	
	# add_questionName()
	
	print('Done.')
