""" Creating c_schema ontology from scratch with code using owlready2.
 Manual: https://owlready2.readthedocs.io/en/latest """

from owlready2 import *

my_iri = 'http://vstu.ru/poas/se/c_schema_2019-12'

c_schema = get_ontology(my_iri)



	
	
	
with c_schema:
	
	
	####################################
	######## General Properties ########
	####################################
	
	# >
	class hasPart( FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # direct part
	# >
	class hasSibling( FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # base for Next
	# >
	class hasPartTransitive( TransitiveProperty,  # transitive !
		FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # base for FirstAct
	

	
	
	###############################
	######## Code Classes ########
	###############################
	
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
		
	
	
	
	
	#################################
	######## Code Properties ########
	#################################
	
	"""In addition, the following subclasses of Property are available: FunctionalProperty, InverseFunctionalProperty, TransitiveProperty, SymmetricProperty, AsymmetricProperty, ReflexiveProperty, IrreflexiveProperty. They should be used in addition to ObjectProperty or DataProperty (or the ‘domain >> range’ syntax)."""
	
	# ->
	class hasFirstSt( Block >> Statement , hasPart): pass
	# ->
	class hasLastSt( Block >> Statement , hasPart): pass
	# ->
	class hasNextSt( Statement >> Statement , hasSibling):
		comment = 'Ordering within Block'
		
	# ->
	class hasSubExpr( CodeElement >> Expression , hasPart): pass
	# -->
	class hasCondition( (Decision | Loop) >> Expression , hasSubExpr): pass
	class hasFORInit( FOR_st >> Expression , hasSubExpr): pass
	class hasFORUpdate( FOR_st >> Expression , hasSubExpr): pass
	
	# ->
	class hasSubStmt( Statement >> Statement , hasPart): pass
	# -->
	class hasBody( Statement >> Statement , hasSubStmt): pass
	# -->
	class hasThenBranch( IF_st >> Statement , hasSubStmt): pass
	class hasElseBranch( IF_st >> Statement , hasSubStmt): pass




	
	###############################
	######## Trace Classes ########
	###############################
	
	# >
	class TraceElement(Thing):
		comment = 'Base for Act & Context trace elements'
	# ->
	class Act(TraceElement): pass  # atomic "Act"
	# -->
	class ConditionAct(Act): pass  # expression Act, evals to True or False
	
	# ->
	class Context(TraceElement): pass
	# -->
	class BlockContext(Context): pass
	# -->
	class DecisionContext(Context): pass
	# --->
	class IF_Context(DecisionContext): pass
	# -->
	class LoopContext(Context): pass
	# --->
	class WHILE_Context(LoopContext): pass
	# --->
	class FOR_Context(LoopContext): pass
	# --->
	class DO_Context(LoopContext): pass
	
	



	
	###########################№######
	######## Trace Properties ########
	###########################№######
	
	# >
	class hasFirstAct( Context >> Act , hasPartTransitive): pass  # over hasFirst(c, a) & Act(a)
	# >
	class hasLastAct( Context >> Act , hasPartTransitive): pass  # over hasLast(c, a) & Act(a)
	# ->
	class hasFirst( Context >> TraceElement , hasPart): pass
	# ->
	class hasLast( Context >> TraceElement , hasPart): pass
	
	
	# >
	class hasNextAct( Act >> Act , hasSibling): pass
	# ->
	class hasNext( Context >> TraceElement , hasSibling): pass  # (hasNextL - on same nesting Level)
	# ->
	class before( Context >> TraceElement , hasPartTransitive): pass  # over hasNextL
		
	# ->
	class hasOrigin( TraceElement >> CodeElement , hasPart): pass
	
	# >
	class evalsTo( ConditionAct >> bool , DataProperty): pass
		
	