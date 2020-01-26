import c2onto
from c2onto import ensure_unique, retract_unique_name, iri_name_prepare, OWLPredicate

NOTHING = 'owl:Nothing'  # replace to some appropriate value


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
	def __init__(self, parent, alg_node=None, name='unkn_act', N=-1):
		super().__init__(type_name='Act',
							  alg_node=alg_node,
							  parent=parent,
							  attributes={ "name":name, "N":N }
						  )
		self.sub_acts = []
		self.next_acts = []

	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], self.type_name),
		]
		# call parent
		triples += super().get_triples()
		# при отсутствии явно заданных начала и конца - перенаправляем на NOTHING для определённости
		if not self.sub_acts:
			triples += [
				(self.node_name, "hasDirectPart", NOTHING),
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

class Trace(ActNode):
	""" Root for trace tree created from .tr file """
	def __init__(self, alg_root=None, text_to_parse=None):
		super().__init__(alg_node=alg_root,
							  parent = None,
							  name='Trace',
							 )
		self.type_name = 'Trace'
		# self.make_node_name(N='omit')  # also works OK with `name='Trace'` at __init__

		self.nodes = []  # all trace tree nodes
		self.plain_acts_sequence = []  # "leaf" nodes only
		# {name_str -> obj} - use in parsing lookup
		self.act_names = dict()

		if text_to_parse:
			self.parse(text_to_parse)

	def parse(self, text):
		assert self.alg_node, 'Algorithm root is not set to Trace.alg_node !'

		labeled_tokens = self._parse_text(text)
		print(labeled_tokens)

		context_stack = [self]  # the Trace is the context for everything else

		for act_name, beg_lbs, end_lbs, val in labeled_tokens:
			for begin_name in beg_lbs:
				act = self._make_act(begin_name, parent=context_stack[-1], is_new=True)
				context_stack.append(act)

			act = self._make_act(act_name, parent=context_stack[-1], is_new=True)
			self.plain_acts_sequence.append(act)

			for end_name in end_lbs:
				act = context_stack[-1]
				if act.attributes["name"] == end_name: ### нужно сравнение с оглядкой на алгоритм!
					context_stack.pop()
				else:
					raise Exception("Trace Error: Cannot close %s after %s because current context is %s." % (end_name, act_name, act.attributes["name"]))






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
		evals_to = ""

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
				evals_to = ""
		return labeled_tokens

	def _resolve_alg_name(self, token):
		""" -> resolved alg_node or Exception """
		if token in self.act_names:
			return self.act_names[token]
		else:
			return None ### !

	def _make_act(self, token, parent, is_new=False):
		""" -> ActNode object """
		if token in self.act_names:
			return self.act_names[token]
		else:
			name, N = parse_trace_token(token)
			### заглушка!
			act = ActNode(self, parent=parent, name=name, N=N)
			parent.sub_acts.append(act)
			self.act_names[token] = act
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
			(self.node_name, OWLPredicate["type"], self.type_name),
		]
		# call parent
		triples += ActNode.get_triples(self)
		# при отсутствии явно заданных начала и конца - замыкаемся на себя (могут быть проблемы с концом неполной трассы)
		if not self.acts:
			self.acts.append(self)
		# стандартная отправка списка ...
		if self.acts:
			triples += [
				(self.node_name, "hasFirstAct", self.acts[0].node_name),
				(self.node_name, "hasLastAct", self.acts[-1].node_name),
			]
		prev_act = None
		for act in self.acts:
			triples += [
				(self.node_name, "hasAct", act.node_name),
			]
			triples += act.get_triples()
			if prev_act:
				triples += [
					(prev_act.node_name, "hasNextAct", act.node_name),
				]
			prev_act = act
		return triples


# class ActContextNode(TraceNode):
#     """ Context (compound Act) can be labelled with BeginLabel and/or EndLabel """
#     def __init__(self, parent, alg_node=None, name='unkn_context', N=-1):
#         TraceNode.__init__(self, type_name='ActContext',
#                               alg_node=alg_node,
#                               parent = parent,
#                               N = N,
#                               attributes={ "name":name, }
#                           )
#         self.begin = None
#         self.end = None
#     def get_begin(self):
#         if not self.begin:
#             self.begin = BeginLabelNode(self)
#         return self.begin
#     def get_end(self):
#         if not self.end:
#             self.end = EndLabelNode(self)
#         return self.end
#     def get_triples(self):
#         triples = [
#             (self.node_name, OWLPredicate["type"], self.type_name),
#         ]
#         # call parent
#         triples += TraceNode.get_triples(self)
#         return triples

# class AbstractLabelNode(TraceNode):
#     """ Abstract Act's label """
#     def __init__(self, parent, type_name='Any~Label'):
#         assert isinstance(parent, ActContextNode), 'Label must be connected to ActContextNode via parent parameter.'
#         TraceNode.__init__(self, type_name=type_name,
#                               parent = parent,
#                               attributes={ "name":parent.node_name+'_'+type_name, }
#                           )
#     def get_triples(self):
#         triples = [
#             (self.node_name, OWLPredicate["type"], self.type_name),
#             (self.node_name, "isLabelOf", self.parent.node_name),
#         ]
#         # call parent  -  unnesessary (no appropriate properties assigned)
# #         triples += TraceNode.get_triples(self)
#         # call context
#         triples += self.parent.get_triples()
#         #         # call context, & prevent duplicates
#         #         parent_triples = self.parent.get_triples()
#         #         for pt in parent_triples:
#         #             if pt not in triples:
#         #                 triples.append(pt)
#         return triples

# class BeginLabelNode(AbstractLabelNode):
#     """ Act's labell: begin of Context """
#     def __init__(self, parent):
#         AbstractLabelNode.__init__(self, type_name='BeginLabel',  parent = parent)
# class EndLabelNode(AbstractLabelNode):
#     """ Act's label: end of Context """
#     def __init__(self, parent):
#         AbstractLabelNode.__init__(self, type_name='EndLabel', parent = parent)


# uniq_names.clear()
# using existing alg

# tr = Trace(alg)



print('\n\o/')
print(' H')
print('/|')
