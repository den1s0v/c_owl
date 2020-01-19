from pycparser import parse_file, c_parser, c_ast, c_generator, plyparser
from collections import defaultdict
import re


def ast_to_code(ast_node):
	""" ast_to_code(ast_node) -> str
	Восстанавливает код Си по узлу pycparser-AST в нормализованном форматировании.
	"""
	generator = c_generator.CGenerator()
	return generator.visit(ast_node)


def coord2str(coord):
	""" coord2str(coord) -> str
	Форматирует суффикс местоположения (координату) в коде для вставки после '@' в iri создаваемых объектов в дереве алгоритма (Algorithm).
	Эта функция выделена отдельно для лёгкого изменения формата ковертации plyparser.Coord в строку. Например, можно убрать номер столбца из суффикса, изменив форматную строку.
	coord может быть строкой, или объектом pycparser.plyparser.Coord с целочисленными полями line, column.
	"""
	return "%d:%d" % (coord.line, coord.column)  if isinstance(coord, plyparser.Coord) else  coord

class FuncDefFinder(c_ast.NodeVisitor):
	""" A simple visitor for FuncDef nodes that remembers function definitions in self.functions list.
	"""
	def __init__(self):
		self.functions = []

	def visit_FuncDef(self, node):
		"The name is special : visit_<NodeName>"
		# print('%s at %s' % (node.decl.name, node.decl.coord))
		self.functions.append(node)

_iri_re = None

def iri_name_prepare(s):
	global _iri_re
	if not _iri_re:
		_iri_re = re.compile(r'[^\w\d\/#-]')
	return _iri_re.sub('', s)



def find_func_defs(ast):
	""" find_func_defs(ast) -> list of FuncDef nodes found in tree with root `ast` """
	v = FuncDefFinder()
	v.visit(ast)
	return v.functions

# def emit_triple(s,p,o):
# 	print(">: [%5s - %5s - %5s]", (s,p,o))


# множество использованных уникальных имён. Желательно очистить перед новым проходом с использованием функции ensure_unique()
uniq_names = set()

def ensure_unique(name, suffix_sep = '_'):
	""" ensure_unique(name, suffix_sep = '_') -> name of <name with suffix> if already in use.
	Проверяет, есть ли name в uniq_names, и если да, то для достижения уникальности прибавляет к нему суффикс `_X`, где X - целое число. Разделитель по умолчанию "_" можно изменить, указав параметр suffix_sep.
	Пример:

		>>> ensure_unique('no-name')
		no-name
		>>> ensure_unique('no-name')
		no-name_1
		>>> ensure_unique('no-name')
		no-name_2
	"""
	if name in uniq_names:
		i = 1
		new_name = name+suffix_sep+str(i)
		while new_name in uniq_names:
			i += 1
			new_name = name+suffix_sep+str(i)
		name = new_name

	uniq_names.add(name)
	return name

# известные стандартные предикаты для RDF
OWLPredicate = {
	"type" : 'rdf:type',
}

#####################
## блок в notebook ##
#####################

class AlgNode:
	"""Base for an algorithm node.
	Each subclass should parse all child nodes recursively on their creation step. """
	def __init__(self, type_name='stmt', ast_node=None, at='<NA>:NA:NA', parent=None, attributes=None):
		self.type_name = type_name
		self.ast_node = ast_node
		self.at = at
		self.parent = parent
		self.attributes = attributes or dict()
		# calculated attributes
		self.make_node_name()
		# print('=== %20s created.' % self.type_name)
	def make_node_name(self, name=None, loc=None):
#         self.node_name = "%s@%s" % (ensure_unique(name or self.type_name), loc or coord2str(self.at))
		self.node_name = iri_name_prepare("%s" % (ensure_unique(name or self.type_name), ))
	def search_up(self, node_class):
		if isinstance(self, node_class): return self
		elif self.parent:   return self.parent.search_up(node_class)
		else: print('!!! %s not found in tree!' % node_class.__name__); return None
	def get_triples(self):
		return []


class Algorithm(AlgNode):
	""" Root for an algoritmh tree created from pycparser`s AST, """
	def __init__(self, ast_node=None, entry_func_name='main'):
		AlgNode.__init__(self, type_name='ALG',
							  ast_node=ast_node,
							  at='root',
							  parent = None,
							 )
		self.functions = [FuncDefNode(node, self)
						  for node in find_func_defs(ast_node)]
		# search for 'main' function
		self.entry_func = [f for f in self.functions if f.attributes["name"] == entry_func_name]
		self.entry_func = None  if not self.entry_func else self.entry_func[0]
		# set ALG start to main's first statement
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "Algorithm"),
		]

		for func in self.functions:
			triples += [
				(self.node_name, "hasFunc", func.node_name),
			]
			triples += func.get_triples()
		return triples
	def find_finction_by_name(self, func_name):
		for func in self.functions:
			if func_name == func.attributes["name"]:
				return func
		return None


def parse_ast_node_as_stmt(ast_node, parent, make_empty=True):
	if not ast_node:
		return EmptyStmtNode(parent)  if make_empty else  None

	if(isinstance(ast_node, c_ast.Compound)):        return BlockNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.FuncCall)):        return FuncCallNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.If)):        return IfNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.For)):        return ForNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.While)):        return WhileNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.DoWhile)):        return DoWhileNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.Break)):        return BreakNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.Continue)):        return ContinueNode(ast_node, parent)
	if(isinstance(ast_node, c_ast.Return)):        return ReturnNode(ast_node, parent)

	# default: unknown
	return AlgNode('UNKN')

def parse_ast_node_as_expr(ast_node, parent):
# def parse_ast_node_as_expr(ast_node, parent, make_empty=True):
	# simplest solution: just one Expr class - for now
	return GenericExprNode(ast_node, parent)
	#      # default: unknown
	#     return AlgNode('UNKN')

class EmptyStmtNode(AlgNode):
	def __init__(self, parent):
		AlgNode.__init__(self, type_name='EMPTY_STMT',
							  ast_node=None,
							  at=parent.at,
							  parent = parent
						)
		self.make_node_name(name="empty")
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "Empty_st"),
		]
		return triples

class GenericExprNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='Expr',
							  ast_node=ast_node,
							  at=ast_node.coord if ast_node else parent.at,
							  parent = parent
						)
		self.code_string = ast_to_code(ast_node)
		# remove spaces that not allowed in IRI
		self.make_node_name(name='expr-%s' % self.code_string)
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "Expression"),
		]
		return triples

class FuncDefNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='FuncDef',
							  ast_node=ast_node,
							  at=ast_node.decl.coord,
							  parent = parent,
							  attributes={
								  "name":ast_node.decl.name,
							  })
		self.make_node_name(name='funcdecl-'+self.attributes["name"]+'()')
		print(self.node_name)
		self.body = parse_ast_node_as_stmt(ast_node.body, self)
		if isinstance(self.body, BlockNode):
			# зададим блоку явное имя тела функции
			self.body.make_node_name(name='seq-'+self.attributes["name"]+'-body')
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "Function"),
			(self.node_name, "hasName", self.attributes["name"]),
			(self.node_name, "hasBody", self.body.node_name),
		]
		triples += self.body.get_triples()
		return triples

class BlockNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='seq',
							  ast_node=ast_node,
							  at='NA',
							  parent = parent,
						)
		self.statements = [parse_ast_node_as_stmt(node, self)
						  for node in ast_node.block_items] if ast_node.block_items else []
		self.find_location()
		self.make_node_name()

	def find_location(self):
		loc = ['?','?']
		if self.statements:
			first_at = self.statements[0].at
			if not isinstance(first_at,str):
				loc[0] = first_at.line
			last_at = self.statements[-1].at
			if not isinstance(last_at,str):
				loc[1] = last_at.line
#         self.at = "%s-%s" % (str(loc[0]), str(loc[1]))
		self.at = "%s%s" % (str(loc[0]),  '_'  if len(self.statements) > 1 else  '')

	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "Block"),
		]
		if self.statements:
			triples += [
				(self.node_name, "hasFirstSt", self.statements[0].node_name),
				(self.node_name, "hasLastSt", self.statements[-1].node_name),
			]

		prev_st = None
		for st in self.statements:
			triples += [
				(self.node_name, "hasSubStmt", st.node_name),
			]
			triples += st.get_triples()
			if prev_st:
				triples += [
					(prev_st.node_name, "hasNextSt", st.node_name),
				]
			prev_st = st
		return triples


class FuncCallNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='FuncCall',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent,
							  attributes={
								  "name":ast_node.name.name,
							  })
		self.make_node_name(name = "call-%s()" % self.attributes["name"])
		self.called_func = None
		print(self.node_name)
	def get_triples(self):
		# calc later, because possibly not all functions are known by root Algorithm instance at init() stage :)
		self.called_func = self.search_up(Algorithm).find_finction_by_name(self.attributes["name"])  # can be None
		triples = [
			(self.node_name, OWLPredicate["type"], "FuncCall"),
		]
		if self.called_func:
			triples += [
				(self.node_name, "callOf", self.called_func.node_name),
			]
		return triples


class IfNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='IF',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		self.cond    = parse_ast_node_as_expr(ast_node.cond,  self)
		self.iftrue  = parse_ast_node_as_stmt(ast_node.iftrue,  self)
		self.iffalse = parse_ast_node_as_stmt(ast_node.iffalse, self, make_empty=False)
		self.make_node_name(name="if-%s" % self.cond.code_string[:20])
		print(self.node_name)
		# зададим блокам явное имя ветви ветвления
		if isinstance(self.iftrue, BlockNode):
			self.iftrue.make_node_name(name="seq-if-true-%s" % self.cond.code_string[:20])
		if isinstance(self.iffalse, BlockNode):
			self.iffalse.make_node_name(name="seq-if-false-%s" % self.cond.code_string[:20])
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "IF_st"),
			(self.node_name, "hasCondition", self.cond.node_name),
		]
		triples += self.cond.get_triples()
		if self.iftrue:
			triples += [
				(self.node_name, "hasThenBranch", self.iftrue.node_name),
			]
			triples += self.iftrue.get_triples()
		if self.iffalse:
			triples += [
				(self.node_name, "hasElseBranch", self.iffalse.node_name),
			]
			triples += self.iffalse.get_triples()
		return triples


class LoopNode(AlgNode):
	def __init__(self, **kwargs):
		AlgNode.__init__(self, **kwargs)
		self.stmt  = parse_ast_node_as_stmt(self.ast_node.stmt,  self)
		self.cond    = parse_ast_node_as_expr(self.ast_node.cond,  self)
		# зададим блокам явное имя тела цикла
		if isinstance(self.stmt, BlockNode):
			self.stmt.make_node_name(name="seq-%s-body-%s" % (self.type_name, self.cond.code_string[:20]))

	def get_triples(self):
		triples = []

		if self.stmt:
			triples += [
				(self.node_name, "hasBody", self.stmt.node_name),
				(self.node_name, "hasCondition", self.cond.node_name),
			]
			triples += self.stmt.get_triples()
			triples += self.cond.get_triples()
		return triples


class ForNode(LoopNode):
	def __init__(self, ast_node, parent):
		LoopNode.__init__(self, type_name='FOR',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		init_code = ast_to_code(ast_node.init)
		self.make_node_name(name="for-%s-%s-%s" % (init_code, self.cond.code_string, ast_to_code(ast_node.next)))
		self.init = parse_ast_node_as_stmt(self.ast_node.init,  self)
		self.next = parse_ast_node_as_stmt(self.ast_node.next,  self)

		# "починить" позиции для пустых частей заголовка for
		if(isinstance(self.init, EmptyStmtNode)):
			self.init.at.column = self.at.column + 4
		if(isinstance(self.cond, EmptyStmtNode)):
			self.cond.at.column = self.init.at.column + 1 + len(init_code)
		if(isinstance(self.next, EmptyStmtNode)):
			self.next.at.column = self.cond.at.column + 1 + len(self.cond.code_string)
		# print(self.node_name)

	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "FOR_st"),
		]
		if self.init:
			triples += [
				(self.node_name, "hasFORInit", self.init.node_name),
			]
			triples += self.init.get_triples()
		if self.next:
			triples += [
				(self.node_name, "hasFORUpdate", self.next.node_name),
			]
			triples += self.next.get_triples()
		# call parent
		triples += LoopNode.get_triples(self)
		return triples


class WhileNode(LoopNode):
	def __init__(self, ast_node, parent):
		LoopNode.__init__(self, type_name='WHILE',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		self.make_node_name(name="while-%s" % self.cond.code_string[:20])

	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "WHILE_st"),
		]
		# call parent
		triples += LoopNode.get_triples(self)
		return triples


class DoWhileNode(LoopNode):
	def __init__(self, ast_node, parent):
		LoopNode.__init__(self, type_name='DO_WHILE',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		self.make_node_name(name="do-while-%s" % self.cond.code_string[:20])

	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "DO_st"),
		]
		# call parent
		triples += LoopNode.get_triples(self)
		return triples


class BreakNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='BREAK',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		self.loop = self.parent.search_up(LoopNode)
		self.make_node_name(name="break-%s" % self.loop.type_name)
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "BREAK_st"),
		]
		if self.loop:
			triples += [
				(self.node_name, "breaksLoop", self.loop.node_name),
			]
		return triples

class ContinueNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='CONTINUE',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		self.loop = self.parent.search_up(LoopNode)
		self.make_node_name(name="continue-%s" % self.loop.type_name)
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "CONTINUE_st"),
		]
		if self.loop:
			triples += [
				(self.node_name, "continuesLoop", self.loop.node_name),
			]
		return triples


class ReturnNode(AlgNode):
	def __init__(self, ast_node, parent):
		AlgNode.__init__(self, type_name='RETURN',
							  ast_node=ast_node,
							  at=ast_node.coord,
							  parent = parent
						)
		self.expr = parse_ast_node_as_expr(ast_node.expr,  self)
		self.function = self.parent.search_up(FuncDefNode)
		self.make_node_name(name="return-from-"+self.function.attributes["name"])
	def get_triples(self):
		triples = [
			(self.node_name, OWLPredicate["type"], "RETURN_st"),
			(self.node_name, "hasSubExpr", self.expr.node_name),
		]
		triples += self.expr.get_triples()
		if self.function:
			triples += [
				(self.node_name, "returnsFrom", self.function.node_name),
			]
		return triples

#####################
## блок в notebook ##
#####################



# обработать префиксы сущностей OWL
def make_namespace_prefix(name, default_prefix=':', known_prefixes=None):
    """ Prepends default_prefix to name if required and no one of known_prefixes present """
    if name.startswith(default_prefix):
        return name
    if name.startswith( tuple(known_prefixes or () ) ):
        return name
    # no known_prefix present
    return default_prefix + name


def triple_to_sparql_insert(triple, prefix_str=""):

    s = """INSERT DATA
{
%s %s %s .
}""" % triple
    return prefix_str + s


print('c2onto definitions OK')

if __name__ == "__main__":

	# СМ. локальный Jupyter

	alg_filename = 'examples/ex2f.c'
	ast = parse_file(alg_filename, use_cpp=False)

	function_defs = find_func_defs(ast)

	if not function_defs:
		print('no functions detected.')
		exit(0)

	for fd in function_defs:
		print()
		fd.show()



