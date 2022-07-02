# msg2i18n.py

"First-time conversion of localization file to different (Spring) format. Don't run again since the result files were modified."


DIR = r'c:\D\Dev\YDev\CompPr\CompPrehension\src\main\resources\org\vstu\compprehension\models\businesslogic\domains' + "\\"

MESSAGES_FILE = DIR + "control-flow-statements-domain-messages.txt"

out_en = DIR + "messages_en.properties"
out_ru = DIR + "messages_ru.properties"



def class_formatstr(*args):
	""" Сохраняем все переводы в словарь """
	class_name, format_str_ru, format_str_en = args if len(args) == 3 else list(args[0])

	class_names_dict = dict(zip(("en", "ru"), class_name.split()))

	return class_names_dict, {
		"ru": format_str_ru,
		"en": format_str_en,
	}


def read_msgs():

	key_msgs = []

	# read templates from file
	with open(MESSAGES_FILE) as f:
		for spec in f.readlines():
			spec = spec.strip()
			if not spec:
				continue
			class_name, format_str = class_formatstr(spec.split('\t'))
			# register_handler(class_name, format_str, named_fields_param_provider)
			key_msgs.append((class_name, format_str))

	return key_msgs
	

def write_msgs(key_msgs: list):

	for lang_code, fname in [
		("en", out_en),
		("ru", out_ru),
	]:
		with open(fname, "w") as f:
			for class_names, format_strs in key_msgs:
				class_name = class_names["en"]
				format_str = format_strs[lang_code]
				f.write(f"{class_name}={format_str}\n")
	

if __name__ == '__main__':
	write_msgs(read_msgs())
