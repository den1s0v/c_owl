""" Creating c_schema ontology from scratch with code using owlready2.
 Manual: https://owlready2.readthedocs.io/en/latest """

from owlready2 import *

my_iri = 'http://vstu.ru/poas/se/c_schema_2019-12'

c_schema = get_ontology(my_iri)



with c_schema:
	
	######## Code Classes ########
	
	# >
	class CodeElement(Thing):
		"""docstring for CodeElement"""
		comment = 'Base for Statements & Expresions, etc.'
	# ->
	class Statement(CodeElement): pass
	# -->
	class Block(Statement): pass
	# --->
	class ControlFlow(Statement): pass
	# ---->
	class Decision(ControlFlow): pass
	# ----->
	class IF_st(Decision): pass
	# ----->
	# class SWITCH_st(Decision): pass
	# ---->
	class Loop(ControlFlow): pass
	# ----->
	class FOR_st(Loop): pass
	# ----->
	class WHILE_st(Loop): pass
	# ----->
	class DO_st(Loop): pass
	
	# ->
	class Expression(CodeElement): pass
		
	######## Code Properties ########
	
	"""In addition, the following subclasses of Property are available: FunctionalProperty, InverseFunctionalProperty, TransitiveProperty, SymmetricProperty, AsymmetricProperty, ReflexiveProperty, IrreflexiveProperty. They should be used in addition to ObjectProperty or DataProperty (or the ‘domain >> range’ syntax)."""
	
	# >
	class firstSt( Block >> Statement ,
		FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass
	# >
	class lastSt( Block >> Statement ,
		FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass
	# >
	class nextSt( Statement >> Statement ,
		FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty):
		comment = 'Ordering within Block'
		
	# >
	class hasSubExpr( CodeElement >> Expression ,
		FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass
	# ->
	class hasCondition( Decision | Loop >> Expression , hasSubExpr): pass
	class hasFORInit( FOR_st >> Expression , hasSubExpr): pass
	class hasFORUpdate( FOR_st >> Expression , hasSubExpr): pass
	
	# >
	class hasSubStmt( Statement >> Statement ,
		FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass
	# ->
	class hasBody( Statement >> Statement , hasSubStmt): pass
	# ->
	class hasThenBranch( IF_st >> Statement , hasSubStmt): pass
	class hasElseBranch( IF_st >> Statement , hasSubStmt): pass



	
	######## Trace Classes ########
	
	# >
	class TraceElement(Thing):
		comment = 'Base for Act & Context trace elements'
	
	
	
		
	