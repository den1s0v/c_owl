# jena2json.py
# write rules from usual Jena-rules file to JSON for compPrehension format

import json
import re

# OUT_FILE = "domain_laws.json"
OUT_FILE = "control-flow-statements-domain-laws.json"


TASK_MAP = [
	("rdfs4core.rules", {
		"name": "rdfs_subset_positive",
		"positive": True,
	}),
	# Duplicate this as there no way to include these to both positive and negative
	("rdfs4core.rules", {
		"name": "rdfs_subset_negative",
		"positive": False,
	}),
	("loop_names.ttl", {
		"name": None,
		"positive": True,
	}),
	# Duplicate this as there no way to include these to both positive and negative
	("loop_names.ttl", {
		"name": None,
		"positive": False,
	}),
	("alg_rules.ttl", {
		"name": None,
		"positive": True,
	}),
	("trace_rules.ttl", {
		"name": None,
		"positive": False,
	}),
]

# alg_rules.ttl
# trace_rules.ttl

def main():
	print("Exporting Jena rules as laws ...")
	all_laws = []
	for fname, config in TASK_MAP:
		laws = read_laws_from_file(fname, config)
		all_laws.extend(laws)
		# print(laws)
		print('.')

	with open(OUT_FILE, 'w', encoding='utf-8') as f:
		json.dump(all_laws, f, ensure_ascii=False, indent=2)

	print("Don't forget to copy the result to:")
	print(r"c:\D\Work\YDev\CompPr\CompPrehension\src\main\resources\org\vstu\compprehension\models\businesslogic\domains" '\\')



def read_laws_from_file(fname, config) -> list:
	with open(fname) as f:
		lines = f.readlines()

	if config["name"]:
		# simple rule list separated by blank lines
		law = create_Law(config)
		for line in lines:
			line = line.strip()
			if line:
				law["formulations"].append(create_Rule(gen_name(), line))
		return [law]
	else:
		# multiline rules in [] grouped by comment-titles
		laws = SectionedRulesReader(lines, config).laws
		return laws

def create_Rule(name, formulation=None):
	return  {
		"name": name,
		"formulation": formulation or '',
		"backend": "Jena"
	  }

def create_Law(law_config, formulations=None):
	if "concepts" not in law_config: law_config["concepts"] = None
	if "tags" not in law_config: law_config["tags"] = None

	law = {
		**law_config,
		"formulations": formulations or [],
	  }
	if not law["concepts"]: law["concepts"] = []
	if not law["tags"]: law["tags"] = []
	return law


AUTOGEN_N = 0

def gen_name():
	global AUTOGEN_N
	AUTOGEN_N += 1
	return "autogen_%d" % AUTOGEN_N


def header2name_and_tags(line):
	return line.replace(" ", "_"), line.replace(" and ", " ").split()

class SectionedRulesReader:
	def __init__(self, lines, default_config):
		self.lines = lines
		self.ci = 0  # current i
		self.laws = []
		self.law_config = default_config
		self.in_rule = False
		self.rule_config = {}

		while self.ci < len(lines):
			# self.ci = i
			line = self.lines[self.ci].strip()
			# line = line.strip()
			if line:
				if line.startswith("#"):
					self.handle_comment(line)
				elif line.startswith("@"):
					pass
				elif line.startswith("["):
					self.begin_rule(line)
				elif line.startswith("]"):
					self.in_rule = False
				else:
					self.handle_code(line)

			# increment
			self.ci += 1

	def handle_comment(self, line: 'current line'):
		# line = self.lines[self.ci].strip()
		if ('#####' in line and
			'#####' in self.lines[self.ci + 2].strip()):
			line = self.lines[self.ci + 1].lstrip("#").strip()
			name, tags = header2name_and_tags(line)
			self.law_config["name"] = name
			self.law_config["tags"] = [{'name': tag} for tag in tags]
			# create law
			### print(self.law_config)
			self.laws.append(create_Law(self.law_config))

			self.ci += 2
		else:
			pass

	def begin_rule(self, line: 'current line'):
		name = None
		tags = []
		self.in_rule = True
		if ':' in line:
			name = line.lstrip('[').rstrip(':')
		prev_line = self.lines[self.ci - 1].lstrip("#").strip()
		if prev_line:
			prev_line = prev_line.replace("Rule: ", '')
			m = re.search(r'\[(.+)\]', prev_line)
			if m:
				tags = m[1].replace(" & ", ' ').split()
				prev_line = prev_line.replace(m[1], '').strip(" ][")
				name = prev_line

		self.rule_config["name"] = name or gen_name()

		law = self.laws[-1]
		law_tags = law["tags"]
		for tag in [{'name': tag} for tag in tags]:
			if tag not in law_tags:
				law_tags.append(tag)

		law["formulations"].append(create_Rule(**self.rule_config))




	def handle_code(self, line: 'current line'):
		if not self.in_rule:
			print("Warning: code line outside of a rule: line", self.ci + 1)
			return
		law = self.laws[-1]
		rule = law["formulations"][-1]
		rule["formulation"] = (rule["formulation"].rstrip('.') + " " + line).strip() + '.'

		for m in re.finditer(r'rdf:type my:(\w+)', line):
			concept = m[1]
			concept = {"name": concept}
			if concept not in law["concepts"]:
				law["concepts"].append(concept)
		# ...


if __name__ == '__main__':
	main()




