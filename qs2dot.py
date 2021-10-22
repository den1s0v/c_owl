# qs2dot.py

# import math

import graphviz
from graphviz import nohtml


class Node:
	def __init__(self, **kw):
		self.name = ''
		self.i = 0
		self.mistakes = set()
		self.incoming = list()
		self.outgoing = list()

		for k,v in kw.items():
			setattr(self, k, v)

	def is_connected_to(self, other):
		if other in self.outgoing  and  self in other.incoming:
			return '>'
		if other in self.incoming  and  self in other.outgoing:
			return '<'
		return None

	def connect_to(self, to):
		# guard: do not allow duplicated and reverse connections
		self.disconnest_from(to)
		# connect
		self.outgoing.append(to)
		to.incoming.append(self)

	def disconnest_from(self, other):
		if other in self.outgoing  and  self in other.incoming:
			self.outgoing.remove(other)
			other.incoming.remove(self)
		if other in self.incoming  and  self in other.outgoing:
			self.incoming.remove(other)
			other.outgoing.remove(self)

	def mistakes_of_children(self):
		ms = set()
		for child in self.outgoing:
			ms.update(child.mistakes)
		return ms


def lay_questions_on_graph(n2ms: dict):
	""" n2ms - dict: name -> mistakes set
	"""
	# print(*n2ms.keys())

	nodes = []

	# make all nodes (unconnected yet), merging equal ones
	i = 0
	for name, mistakes in n2ms.items():
		existing_node = None
		for node in nodes:
			if node.mistakes == mistakes:
				existing_node = node
				break

		if existing_node:
			existing_node.name = (existing_node.name + " " + name).strip()
		else:
			node = Node(name=name, i=i, mistakes=set(mistakes))
			nodes.append(node)
			i += 1  # in fact, i equals to `len(nodes)`

	def _connect_nodes(node1, node2, _visited_nodes=()):
		if node1.is_connected_to(node2):
			return
		if node1.mistakes < node2.mistakes:
			in_use = False
			for subn in node2.outgoing:
				if node1.mistakes < subn.mistakes:  # 1 < s < 2
					_connect_nodes(node1, subn)
					in_use = True
				elif subn.mistakes < node1.mistakes:  # s < 1 < 2
					# place 1 between s and 2
					subn.disconnest_from(node2)
					node1.connect_to(subn)  # direction is as "arrow" shows
					node2.connect_to(node1)
					in_use = True
			if not in_use:
				node2.connect_to(node1)

		if node1.mistakes > node2.mistakes:
			in_use = False
			for subn in node2.incoming:
				if node1.is_connected_to(subn):
					return
				if node1.mistakes > subn.mistakes:  # 1 > s > 2
					_connect_nodes(node1, subn)
					in_use = True
				elif subn.mistakes > node1.mistakes:  # s > 1 > 2
					# place 1 between s and 2
					subn.disconnest_from(node2)
					subn.connect_to(node1)
					node1.connect_to(node2)
					in_use = True
			if not in_use:
				node1.connect_to(node2)


	# connect nodes in order of inclusion
	for node1 in nodes:
		for node2 in nodes:
			if node1 is node2:
				continue
			_connect_nodes(node1, node2)

	# add additional-mistakes list to names of nodes
	for node in nodes:
		child_mistakes = node.mistakes_of_children()
		mistakes_diff = node.mistakes - child_mistakes
		node.name = "\n".join([fit_name_series_for_drawing(node.name), *sorted(mistakes_diff), *(["(+ dependent)"] if child_mistakes else [])])

		### print(node.name)


	# make DOT picture from the graph data
	dot = graphviz.Digraph(comment='CompPrehension questions dependencies', format='png')
	dot.attr('node', shape='box')

	for node in reversed(nodes):
		dot.node(str(node.i), nohtml(node.name))


	# for i, node1 in enumerate(nodes):
	for node1 in nodes:
		for node2 in nodes:
			if node1 is not node2 and node2 in node1.outgoing:
				dot.edge(str(node1.i), str(node2.i))  #, constraint='false')


	dot.render('c:/temp/cph-qs', view=True)


def fit_name_series_for_drawing(long_name):
	W = 40
	if len(long_name) > W:
		# L = len(long_name)
		# part_len = round(L / ((L + 11) / W))
		cur_s = ''
		res = ''
		while long_name:
			word, sep, long_name = long_name.partition(" ")
			cur_s += word + sep
			if len(cur_s) >= W:
				res += cur_s + "\n"
				cur_s = ''

		long_name = res.strip()

	return "%s (%d tasks)" % (long_name, long_name.count(" ") + 1)

def graphviz_tutorial():
	''' https://graphviz.readthedocs.io/en/stable/manual.html#basic-usage '''
	# Create a graph object:
	dot = graphviz.Digraph(comment='The Round Table')
	# dot  #doctest: +ELLIPSIS
	# <graphviz.dot.Digraph object at 0x...>
	# Add nodes and edges:

	dot.node('A', 'King Arthur')
	dot.node('B', 'Sir Bedevere the Wise')
	dot.node('L', 'Sir Lancelot the Brave')

	dot.edges(['AB', 'AL'])
	dot.edge('B', 'L', constraint='false')
	# Check the generated source code:

	print(dot.source)  # doctest: +NORMALIZE_WHITESPACE
	# // The Round Table
	# digraph {
	#     A [label="King Arthur"]
	#     B [label="Sir Bedevere the Wise"]
	#     L [label="Sir Lancelot the Brave"]
	#     A -> B
	#     A -> L
	#     B -> L [constraint=false]
	# }

	# Save and render the source code, optionally view the result:
	# (creates a PDF file also, and runs default PDF viewer with it)
	dot.render('c:/temp/round-table.gv', view=True)  # doctest: +SKIP
	# 'test-output/round-table.gv.pdf'
