import c2onto
from c2onto import ensure_unique, retract_unique_name, iri_name_prepare, OWLPredicate

# NOTHING = 'owl:Nothing'  # replace with some appropriate value
OWLStdEntity = {"Nothing": 'CustomNothing'}
OWLStdEntity.update(OWLPredicate)


class TraceNode:
	"""Base for an trace node. """
	def __init__(self, type_name='trace_elem', parent=None, alg_node=None, attributes=None):
		self.type_name = type_name
		self.parent = parent
		self.alg_node = alg_node
		self.attributes = attributes or dict()
		if "N" not in self.attributes:
			self.attributes["N"] = -1  # execution count (nth time)
		# calculated attributes
		self.make_node_name(name=attributes["name"] if (attributes and "name" in attributes) else None)
		print('=== %20s created.' % self.node_name)

	def make_node_name(self, name=None, N=None):
		""" set N="omit" to disable appending of N.
			if N=None (the default) then self.attributes["N"] is used
		 """
		# точка расширения для настройки имён
		# ...
		# удалить текущее имя из уникальных, если есть
		if "id" in self.attributes:
			retract_unique_name(self.attributes["id"])
		suffix = ""
		if N == "omit":
			pass  # omit N from id
		else:
			if N is None and self.attributes["N"] > -1:
				N = self.attributes["N"]
			if N:
				suffix = "-N" + str(self.attributes["N"])
		_id = (name or self.type_name) + suffix
		self.attributes["id"] = iri_name_prepare(ensure_unique(_id))
		self.node_name = iri_name_prepare("%s" % self.attributes["id"])

	def search_up(self, node_class):
		if isinstance(self, node_class): return self
		elif self.parent:   return self.parent.search_up(node_class)
		else: print('!!! %s not found in tree!' % node_class.__name__); return None
	def get_triples(self):
		triples = []
		if self.alg_node:
			triples += [
					(self.node_name, "hasOrigin", self.alg_node.node_name),
			]
		# if self.parent:
		#     triples += [
		#             (self.node_name, "hasContext", 54self.parent.node_name),
		#     ]
		if self.attributes["N"] > -1:
			triples += [
					(self.node_name, "hasN", self.attributes["N"]),
			]
		return triples

class ActNode(TraceNode):
	""" Act of trace """
	def __init__(self, parent, alg_node=None, name='unkn_act', N=-1, type_name=None, attributes=None):
		super().__init__(type_name=type_name or'Act',
							  alg_node=alg_node,
							  parent=parent,
							  attributes={ "name":name, "N":N }
						  )
		if attributes:
			self.attributes.update(attributes)
		self.sub_acts = []
		self.next_acts = []

	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], self.type_name),
		]
		# call parent
		triples += super().get_triples()
		# при отсутствии явно заданных начала и конца - атомарный акт
		if not self.sub_acts:
			triples += [
				# перенаправляем на СЕБЯ для определённости
				(self.node_name, "hasDirectPart", self.node_name),
				# замкнуть начало и конец на себе самом
				(self.node_name, "hasFirstAct", self.node_name),
				(self.node_name, "hasLastAct", self.node_name),
			]
			return triples

		# else
		# отправка списка первого уровня вложенности ...
		triples += [
			(self.node_name, "hasFirstAct", self.sub_acts[0].node_name),
			(self.node_name, "hasLastAct", self.sub_acts[-1].node_name),
		]
		prev_act = None
		for act in self.sub_acts:
			triples += [
				(self.node_name, "hasDirectPart", act.node_name),
			]
			triples += act.get_triples()
			if prev_act:
				triples += [
					(prev_act.node_name, "hasNextAct", act.node_name),
				]
			prev_act = act

		# отправка связок со следующими актами ...
		for act in self.next_acts:
			triples += [
				(self.node_name, "hasNextAct", act.node_name),
			]
		return triples


class ConditionActNode(ActNode):  ## No transt inheritance for now ConditionAct < ExpressionAct < ActNode.
	""" Condition Act of a loop or IF """
	def __init__(self, parent, alg_node=None, name='unkn_cond', N=-1, evals_to=None):
		super().__init__(type_name='ConditionAct',
							  parent=parent,
							  alg_node=alg_node,
							  name=name,
							  attributes={ "name":name, "N":N, "evals_to": bool(evals_to) }
						  )
	def get_triples(self):
		triples = [
			# (self.node_name, OWLPredicate["type"], self.type_name),
		]
		# call parent
		triples += super().get_triples()
		if self.attributes["evals_to"] is not None:
			triples += [
				(self.node_name, "evalsTo", self.attributes["evals_to"]),
			]
		return triples

class Trace(ActNode):
	""" Root for trace tree created from .tr file """
	def __init__(self, alg_root=None, text_to_parse=None):
		super().__init__(alg_node=alg_root,
							  parent = None,
							  name='TRACE',
							 )
		self.type_name = 'Trace'
		# self.make_node_name(N='omit')  # also works OK with `name='Trace'` at __init__

		self.nodes = []  # all trace tree nodes
		self.plain_acts_sequence = []  # "leaf" nodes only
		# {name_str -> alg_obj} - use in parsing lookup
		self.name2alg = dict()

		if text_to_parse:
			self.parse(text_to_parse)

	def parse(self, text):
		assert self.alg_node, 'Algorithm root is not set to Trace.alg_node !'

		labeled_tokens = self._parse_text(text)

		self._resolve_names([ [n,*bs,*es] for n,bs,es,_ in labeled_tokens ])

		context_stack = [self]  # the Trace is the context for everything else
		# finished_acts = []      # acts finished on previous iteration

		# цикл составления трассы
		for act_name, beg_lbs, end_lbs, val in labeled_tokens:
			# new_acts = []

			for begin_name in beg_lbs:
				act = self._make_act(begin_name, parent=context_stack[-1])
				context_stack.append(act)
				# new_acts.append(act)

			act = self._make_act(act_name, parent=context_stack[-1], evals_to=val)
			self.plain_acts_sequence.append(act)
			# new_acts.append(act)

			# if finished_acts:
				# 	for pr_act in finished_acts:
				# 		for new_act in new_acts:
				# 			pr_act.next_acts.append(new_act)
				# finished_acts.clear()
				# finished_acts.append(act)

			for end_name in end_lbs:
				act_to_close = context_stack[-1]
				is_ok = False
				if act_to_close.attributes["name"] == end_name:
					is_ok = True
				elif act_to_close.alg_node == self.name2alg[end_name]:  # сравнение с оглядкой на алгоритм
					is_ok = True
					print("Trace warning: Using different names to open and close the same compound act `%S`: `%s`, `%s`" % (act_to_close.alg_node.attributes["name"], act_to_close.attributes["name"], end_name))
				if is_ok:
					context_stack.pop()
				else:
					raise Exception("Trace Error: Cannot close %s after %s because the context is %s." % (end_name, act_name, act_to_close.attributes["name"]))

				# finished_acts.append(act)   # ... TODO
		if context_stack != [self]:
			print("Trace warning: The trace is not complete or contains errors. The contexts stack remaining at the end of provided trace is expected to contain the Trace only, but found: [%s]" % str(list(map(lambda a:"%s[%s]"%(a.attributes["name"],a.node_name), self.context_stack))))

	def _resolve_names(self, names):
		""" fills self.name2alg dict with a mapping the given names to algorithm nodes. """
		for items in names:
			if isinstance(items, str):
				items = (items, )
			for item in items:
				if item in self.name2alg:
					continue

				alg_node_found = self._resolve_name(item)
				if alg_node_found:
					# имена-синонимы ...
					if alg_node_found in self.name2alg.values():
						print("Trace warning: Using different names to refer the same algorithm node `%s`: {%s}" % (alg_node_found.node_name, str([key for (key, value) in self.name2alg.items() if value == alg_node_found])))

					self.name2alg[item] = alg_node_found

				else:
					raise Exception("Trace Error: Cannot resolve act name %s over algorithm." % (item, ))

	def _resolve_name(self, name):
		""" -> resolved alg_node or None or Exception if the name is ambiguious.
		searches given name within the algorithm nodes. """
		attempt_params = [
			{
				"args": dict(reverse_check=0, ignore_case=0),
				"many_is_ok": False		# `Cat` matches `Cat`, `Catty`.
			},{
				"args": dict(reverse_check=0, ignore_case=1),
				"many_is_ok": True		# `Cat` matches `cat`, `category`, `CATTY`.
			},{
				"args": dict(reverse_check=1, ignore_case=0),
				"many_is_ok": True		# `Cat` matches `Cat`, `Ca`, `C`.
			},{
				"args": dict(reverse_check=1, ignore_case=1),
				"many_is_ok": True		# `Cat` matches `cat`, `c`, `CAT`.
			},
		]
		candidates = None

		for params in attempt_params:
			found_candidates = self.alg_node.find_candidates_by_subname(name, **params["args"
				])
			if not candidates or 1 <= len(found_candidates) < len(candidates):
				candidates = found_candidates
			if len(candidates) == 1:
				break
			# if len(candidates) == 0:
			# 	continue
			if len(candidates) > 1 and not params["many_is_ok"]:
				break

		if len(candidates) > 1:
			raise Exception("Trace Error: Cannot resolve ambiguious act name `%s` over algorithm. Possible resolutons are: {%s}" % (name, tuple(candidates.keys())))
		return next(iter(candidates.values()))  if candidates else  None

	def _parse_text(self, text):
		""" -> list of labelled tokens.
		Each item is tuple of following form:
		(
			"act_name",
			["begins_name1", "begins_name2", ...],
			["ends_name1", "ends_name2", ...],
			"evals_to_value1"
		)
		"""
		labeled_tokens = []  # accumulating result

		tokens_list = [L.strip().split() for L in text.splitlines()]

		COMMENT_SIGNS = ('#', '//')
		MARK_SIGNS = (':', '.')
		MARK_CHARS = ''.join(MARK_SIGNS)
		BEGIN_MARKS = {'begin', 'begins', 'beginof', 'begin-of', 'begin_of',  }
		END_MARKS = {'end', 'ends', 'endof', 'end-of', 'end_of',  }
		EVALS_TO_SIGNS = {'>', '->', '-->', '=', '=', '-',  }

		curr_act = None  # (string) token representing an act
		begin_labels = []
		end_labels = []
		evals_to = None

		for line_i, line_tokens in enumerate(tokens_list):
			if not line_tokens:
				continue

			token = line_tokens[0]
			if token.startswith(COMMENT_SIGNS):
				continue

			rest_of_tokens = line_tokens[1:]
			if token.startswith(MARK_SIGNS):
				# labels line
				mark = token.strip(MARK_CHARS).lower()
				if mark in BEGIN_MARKS:
					begin_labels += rest_of_tokens
				elif mark in END_MARKS:
					end_labels += rest_of_tokens
				else:
					line_n = line_i + 1
					raise SyntaxError("Unrecognized label mark: '%s'" % mark+(' at line %d of trace' % line_n)+':\n'+("%d:\t%s\n" % (line_n, ' '.join(line_tokens)))
									  +' Expected one of:\n %s\n  or\n %s'%(str(BEGIN_MARKS),str(END_MARKS)))
		        # print(mark)
				if end_labels and not curr_act:
					# cannot apply end_labels to previous act
					line_n = line_i + 1
					raise SyntaxError("Unexpected END labels: %s.\n No preceeding act found to attach these labels." % str(end_labels)+(' At line %d of trace' % line_n)+':\n'+("%d:\t%s\n" % (line_n, ' '.join(line_tokens))))

				if curr_act and end_labels:
					# commit end_labels to previous act
					last_begin_labels, last_end_labels,last_evals_to = labeled_tokens[-1][1:]
					labeled_tokens[-1] = (
						curr_act,
						last_begin_labels,
						last_end_labels + end_labels,
						last_evals_to,
					)
					end_labels.clear()

			else:
				# act line
				if len(rest_of_tokens) == 2 and (rest_of_tokens[0] in EVALS_TO_SIGNS):
					# `expression -> VALUE` row
					evals_to = rest_of_tokens[1]
				elif rest_of_tokens:
					line_n = line_i + 1
					raise SyntaxError("Unknown format: multiple acts on the same line, or wrong `expression -> VALUE` format."+(' At line %d of trace' % line_n)+':\n'+("%d:\t%s\n" % (line_n, ' '.join(line_tokens))))

				curr_act = token

				# make new act item
				assert not end_labels
				labeled_tokens.append( (
						curr_act,
						[] + begin_labels,
						[],  # end_labels is empty
						evals_to,
				) )
				begin_labels.clear()
				evals_to = None
		return labeled_tokens

	# def _resolve_alg_name(self, token):
		# 	""" -> resolved alg_node or Exception """
		# 	if token in self.name2alg:
		# 		return self.name2alg[token]
		# 	else:
		# 		return None ### !

	def _make_act(self, name, parent, evals_to=None):
		""" -> ActNode object """
		alg_node = self.name2alg[name]

		if evals_to is not None:
			# пока поддерживается парсинг только логических значений (для условий циклов/развилок)
			act = ConditionActNode(parent=parent, name=name, alg_node=alg_node, evals_to=self._parse_cond_value(evals_to))
		else:
			act = ActNode(parent=parent, name=name, alg_node=alg_node)
		parent.sub_acts.append(act)
		self.nodes.append(act)
		return act

	def _parse_cond_value(self, token):
		""" _parse_cond_value(str) -> True/False """
		return {
			"true" : True,
			"1" : True,
			"yes" : True,
			"truth" : True,

			"false" : False,
			"0" : False,
			"no" : False,
			"lie" : False,
		}.get(token.lower(), None)

	def get_triples(self):
		triples = [
			# (self.node_name, OWLPredicate["type"], self.type_name),
		]
		# при отсутствии явно заданных начала и конца - замыкаемся на себя (могут быть проблемы с концом неполной трассы?)
		if not self.plain_acts_sequence:
			self.plain_acts_sequence.append(self)
		# стандартная отправка списка ...
		if self.plain_acts_sequence:
			triples += [
				(self.node_name, "hasBegin", self.plain_acts_sequence[0].node_name),
				(self.node_name, "hasEnd", self.plain_acts_sequence[-1].node_name),
			]
		prev_act = None
		for act in self.plain_acts_sequence:
			if prev_act:
				triples += [
					(prev_act.node_name, "hasNextAct", act.node_name),
				]
			prev_act = act
		# call parent
		triples += super().get_triples()
		return triples



print('tr2onto definitions OK')

print('\n\\o/')
print(' H')
print('/|')
