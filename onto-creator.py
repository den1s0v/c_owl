""" Creating c_schema ontology from scratch with code using owlready2.
 Manual: https://owlready2.readthedocs.io/en/latest """

from owlready2 import *

my_iri = 'http://vstu.ru/poas/se/c_schema_2020-01'

c_schema = get_ontology(my_iri)






with c_schema:


	####################################
#	######## General Properties ########
	####################################

	""" |  In addition, the following subclasses of Property are available: FunctionalProperty, InverseFunctionalProperty, TransitiveProperty, SymmetricProperty, AsymmetricProperty, ReflexiveProperty, IrreflexiveProperty. They should be used in addition to ObjectProperty or DataProperty (or the ‘domain >> range’ syntax)."""

	# mixins to be used with property constructor call
	references = [ObjectProperty, AsymmetricProperty, IrreflexiveProperty]
	referencesToUnique = [ObjectProperty, FunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
	referencesToUniqueOrSelf = [ObjectProperty, FunctionalProperty, AsymmetricProperty]
	referencedByUnique = [ObjectProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
	mutualUnique = [ObjectProperty, FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
	hasUniqueData = [FunctionalProperty, DataProperty]  # should I remove DataProperty ?

	# # >
	# class referencesTo( FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # direct part
	# # >
	# class hasOnePart( FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # direct part
	# # >
	# class hasSibling( FunctionalProperty, InverseFunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # (directed) base for any Next
	# # >
	# class hasOnePartTransitive( TransitiveProperty,  # transitive !
	# 	FunctionalProperty, AsymmetricProperty, IrreflexiveProperty): pass  # base for FirstAct
	# # >
	# class hasUniqueData( FunctionalProperty, DataProperty): pass  # datatype property base

	class hasDirectPart( ObjectProperty , *references ): pass
	class hasPart(  ObjectProperty , *references ): pass  # transitive over hasDirectPart (defined thru SWRL!)



	###############################
#	######## Code Classes ########
	###############################

	# >
	class Algorithm(Thing):
		comment = 'Root of an algorithm tree.'
	# >
	class CodeElement(Thing):
		comment = 'Base for Statements & Expresions, etc.'
	# ->
	class Atom(CodeElement):
		comment = 'Abstract atomic executable thing, i.e. a Statement or Expresion executed "in one step".'
	# ->
	class Function(CodeElement): pass
	# ->
	class Statement(CodeElement): pass
	# -->
	class Empty_st(Statement): pass
	# -->
	class FuncCall(Statement , Atom):  #
		comment = 'let a FuncCall is an Atom, for now ...'
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

	# -->
	class BREAK_st(Statement , Atom): pass
	# -->
	class CONTINUE_st(Statement , Atom): pass
	# -->
	class RETURN_st(Statement , Atom): pass

	# ->
	class Expression(CodeElement , Atom): pass





	#################################
#	######## Code Properties ########
	#################################

	# ->
	class hasSubExpr( CodeElement >> Expression , hasDirectPart): pass
	# ->
	class hasSubStmt( CodeElement >> Statement ,  hasDirectPart): pass

	# -->
	class hasCondition( (Decision | Loop) >> Expression , hasSubExpr , *referencesToUnique): pass
	class hasFORInit(   FOR_st >> Expression , 			  hasSubStmt , *referencesToUnique): pass
	class hasFORUpdate( FOR_st >> Expression , 			  hasSubStmt , *referencesToUnique): pass

	# ->
	class hasBody( (Loop | Function) >> Statement ,  hasSubStmt , *referencesToUnique): pass
	# ->
	class hasThenBranch( IF_st >> Statement ,  hasSubStmt , *referencesToUnique): pass
	class hasElseBranch( IF_st >> Statement ,  hasSubStmt , *referencesToUnique): pass

	# ->
	class hasFirstSt( Block >> Statement , *referencesToUnique): pass
	# ->
	class hasLastSt( Block >> Statement , *referencesToUnique): pass
	# ->
	class hasNextSt( Statement >> Statement , *mutualUnique):
		comment = 'Ordering within Block'

	# ->
	class hasFunc( Algorithm >> Function , *references): pass

	# ->
	class hasName( Function >> str , *hasUniqueData): pass
	# ->
	class callOf( FuncCall >> Function , *referencesToUnique): pass

	# ->
	class breaksLoop( BREAK_st >> Loop , 	*referencesToUnique): pass
	# ->
	class continuesLoop( CONTINUE_st >> Loop , *referencesToUnique): pass
	# ->
	class returnsFrom( RETURN_st >> Function , *referencesToUnique): pass





	###############################
#	######## Trace Classes ########
	###############################

	# >
	class TraceElement(Thing):
		comment = 'Base for Acts & other trace elements (if added in future)'
	# ->
	class Act(TraceElement): pass  # atomic or compound "Act"

	# -->
	class Trace(Act):
		comment = 'A trace based on an Algorithm'

	# -->
	class ExpressionAct(Act): pass  # expression Act, evals to some typed value
	# --->
	class ConditionAct(ExpressionAct): pass  # boolean expression Act, evals to True or False

	# # # >
	# # class ActLabel(Thing):
	# # 	comment = 'A mark attached to Act'
	# # ->
	# class ActContext(TraceElement): pass

	# # ->
	# class BeginLabel(TraceElement):
	# 	comment = 'A mark pointing to begin of a Context (compound Act)'
	# # ->
	# class EndLabel(TraceElement):
	# 	comment = 'A mark pointing to end of a Context (compound Act)'


	##################################
#	######## Trace Properties ########
	##################################

	# >
	class hasAct( Act >> Act , *references): pass
	# >
	class hasFirstAct( Act >> Act , *referencesToUniqueOrSelf):
		comment = 'Should always be used with non-empty Trace.'
	# >
	class hasLastAct( Act >> Act , *referencesToUniqueOrSelf): pass

	# Остаётся минимум - только последовательность актов и транзитивное "ДО"
	# >
	class hasNextAct( Act >> Act , *mutualUnique): pass
	# ->
	class beforeAct( Act >> Act , *references): pass  # transitive over hasNextAct (defined thru SWRL!)

	# >
	class hasContext( Act >> Act , *referencesToUnique): pass

	# >
	class hasOrigin( TraceElement >> CodeElement , *referencesToUnique): pass
	# >
	class hasN( Act >> int , *hasUniqueData): pass

	# >
	class evalsTo( ConditionAct >> bool , *hasUniqueData): pass

	# # >
	# class hasBeginLabel( Act >> BeginLabel , *references): pass
	# # >
	# class hasEndLabel( Act >> EndLabel , *references): pass

	# # >
	# class isLabelOf( (BeginLabel | EndLabel) >> ActContext , *referencesToUnique): pass


	##############################
#	######## Rule Classes ########
	##############################

	swrl_rules = []

	# >
	class GenericRule(Thing):
		comment = 'Base for all rules'
		# name
	# ->
	class TraceRule(GenericRule):
		comment = 'Base for all trace rules'

	# -->
	class SequenceRule(TraceRule): pass

	# Тестовый алгоритм
		# void main()
		# {		# main_body
		#     A();
		#     B();
		#     C();
		#     D();
		# }
	# Правильная трасса
		# :begin main_body#1
		#     A#1
		#     B#1
		#     C#1
		#     D#1
		# :end main_body#1


	# -->
	class SequenceRule(TraceRule): pass
	# --->
	class ActOutOfContextRule(SequenceRule): pass
	# Срабатывает, если есть акт `act`, непосредственно вложенный в акт `act_c` (контекст),
	# в то время как их первоисточники в алгоритме (st и st_c) не состоят в таком же отношении вложенности (контекст st - st_c_actual - отличается от st_c, указанного в трассе):
	swrl_rules += """
		hasContext(?act, ?act_c)
		hasOrigin(?act, ?st)
		hasOrigin(?act_с, ?st_с)
		hasDirectPart(?st_c_actual, ?st)

		DifferentFrom(?st_с, ?st_c_actual)
		 -> message(ERRORS, "ActOutOfContextError")
		"""

	# Тестовая трасса
		#     A#1
		# :begin main_body#1
		#     A#2
		#     B#1
		#     C#1
		#     D#1
		# :end main_body#1
	swrl_rules += """  !!!!!
		:Context(?c)
		:Block(?block)
		:Statement(?stmt1)
		:Act(?act1)
		:Act(?act)

		:hasContext(?act1, ?c)
		:hasContext(?act,  ?c)
		:hasFirst(?block, ?stmt1)
		:hasOrigin(?c, ?block)
		:hasOrigin(?act1, ?stmt1)
		:before(?act, ?act1)

		:hasIndex(?c, ?index)
		:hasOrigin(?act, ?stmt)
		:hasSource(?stmt, ?src)
		:hasLocationSuffix(?stmt, ?stlbl)
		swrlb:stringConcat(?msg, "ActBeforeStartOfBlockError: act `", ?src, "` (", ?stlbl, "#", ?index, ") is placed before start of block.")
		 -> c_schema:message(c_schema:ERRORS, ?msg)
		"""

	# ---->
	class ActIsContainedInSequenceRule(SequenceRule): pass
	# ---->
	class OnlyOneActExcecutionInSequenceRule(SequenceRule): pass
	# ---->
	class ExecuteActABeforeActBInSequenceRule(SequenceRule): pass

	# -->
	class AlternativeRule(TraceRule): pass
	# --->
	class AlternativeActExecuteRule(AlternativeRule): pass

	# -->
	class LoopRule(TraceRule): pass
	# --->
	class ExecuteBodyActAfterFalseConditionActRule(LoopRule): pass

	# --->
	class WHILE_Rule(LoopRule): pass
	# ---->
	class WhileLoopBodyActExecuteRule(WHILE_Rule): pass



	#################################
#	######## Rule Properties ########
	#################################

	# >
	class description( GenericRule >> str , DataProperty, FunctionalProperty): pass



	###############################
#	######## Error Classes ########
	###############################

	# >
	class GenericError(Thing):
		comment = 'Base for all errors'
	# ->
	# class Act(TraceElement): pass  # atomic "Act"


	##################################
#	######## Error Properties ########
	##################################





	############################
#	######## SWRL Rules ########
	############################

	rules = {
# 		"BeforeActTransitive": """ Act(?b) ^ Act(?c) ^ :Act(?a) ^ beforeAct(?a, ?b) ^ beforeAct(?b, ?c) -> beforeAct(?a, ?c) """ ,
		"hasNextAct_to_beforeAct": """
			 hasNextAct(?a, ?b) -> beforeAct(?a, ?b)
		 """ ,
		"beforeAct_transitive": """
			 beforeAct(?a, ?b), beforeAct(?b, ?c) -> beforeAct(?a, ?c)
		""" ,

		"hasDirectPart_to_hasPart": """
			 hasDirectPart(?a, ?b) -> hasPart(?a, ?b)
		""" ,
		"hasPart_transitive": """
			 hasPart(?a, ?b), hasPart(?b, ?c) -> hasPart(?a, ?c)
		""" ,

# 		"NextL_to_before": """
#         """ ,
	}

	for r in rules.values():
		Imp().set_as_rule(r)



def upload_rdf_to_SPARQL_endpoint(graphStore_url, rdf_file_path):
	import requests
	with open(rdf_file_path, 'rb') as f:
		r = requests.post(
			graphStore_url,  # ex. 'http://localhost:3030/my_dataset/data',
			files={'file': ('onto.rdf', f, 'rdf/xml')}
		)

	if r.status_code != 200:
		print('\nError uploading file! HTTP response code: %d\nReason: %s\n' % (r.status_code, r.reason))
		return False
	else:
		print('Uploading file successful.')
		return True


def main():

	############################
	######## Export RDF ########
	############################

	# onto_name = c_schema.base_iri.split('/')[-1]  # adds '#' at end
	onto_name = my_iri.split('/')[-1]
	rdf_filename = onto_name + '.rdf'

	c_schema.save(file=rdf_filename, format='rdfxml')
	print("Saved RDF file: {} !".format(rdf_filename))

	# upload_rdf_to_SPARQL_endpoint('http://localhost:3030/c_owl/data', rdf_filename)



if __name__ == '__main__':
	# print()
	# print('TODO: переделать транзитивные свойства на обычные, но с SWRL-правилами')
	# print('TODO: А то ризонер ругается :)')
	# print()
	main()
