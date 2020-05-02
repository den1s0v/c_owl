""" Creating c_schema ontology from scratch with code using owlready2.
 Manual: https://owlready2.readthedocs.io/en/latest """

from owlready2 import *

def make_ontology(iri=None):
	""" -> Owlready2 ontology object """
	my_iri = iri or 'http://vstu.ru/poas/se/seqloopalt_20-03'

	c_schema = get_ontology(my_iri)

	with c_schema:


		####################################
	#	######## General Properties ########
		####################################

		""" |  In addition, the following subclasses of Property are available: FunctionalProperty, InverseFunctionalProperty, TransitiveProperty, SymmetricProperty, AsymmetricProperty, ReflexiveProperty, IrreflexiveProperty. They should be used in addition to ObjectProperty or DataProperty (or the ‘domain >> range’ syntax)."""

		# mixins to be used with property constructor call
		references = [ObjectProperty]
		referencesToUnique = [ObjectProperty, FunctionalProperty, AsymmetricProperty, IrreflexiveProperty]
		referencesToUniqueOrSelf = [ObjectProperty, FunctionalProperty]
		referencedByUnique = [ObjectProperty, InverseFunctionalProperty, ]
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

		class hasDirectPart( ObjectProperty , *references ): pass  # a part of unique whole
		class hasPart(  ObjectProperty , *references ): pass  # transitive over hasDirectPart (defined thru SWRL!)


		###################################
	#	######### General Classes #########
		###################################

		# >
		class WithID(Thing):
			comment = 'Root of an algorithm tree.'

		class hasID(  WithID >> int , *hasUniqueData ): pass  # instead of stating individuals AllDifferent



		##############################
	#	######## Code Classes ########
		##############################

		# >
		class Algorithm(WithID):
			comment = 'Root of an algorithm tree.'
		# >
		class CodeElement(WithID):
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
		class hasFirstSt( Block >> Statement , hasSubStmt , *referencesToUnique): pass
		# ->
		class hasLastSt( Block >> Statement  , hasSubStmt , *referencesToUnique): pass
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
		class TraceElement(WithID):
			comment = 'Base for Acts & other trace elements (if added in future)'
		# ->
		class Act(TraceElement): pass  # atomic or compound "Act"

		# -->
		class ActBegin(Act):
			pass
		# -->
		class ActEnd(Act):
			pass

		# -->
		class Trace(Act):
			comment = 'A trace based on an Algorithm'

		# -->
		# class TraceAtom(Act):
		# 	comment = 'An atomic act that does not contain any acts'
		# 	equivalent_to = [Act & hasDirectPart.has_self(True)]
		# 	# an act should be classified as TraceAtom by its hasDirectPart value set to Nothing

		# -->
		class ExpressionAct(Act): pass  # expression Act, evals to some typed value
		# --->
		class ConditionAct(ExpressionAct): pass  # boolean expression Act, evals to True or False

		# # # >
			# # class ActLabel(WithID):
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
		# class hasAct( Act >> Act , AsymmetricProperty): pass  # Reflexive allowed

		# use hasDirectPart and hasPart to express acts nesting!
		# set A.hasDirectPart = Nothing to describe atomic act.

		# # >
		# class hasFirstAct( Act >> Act , hasDirectPart,  *referencesToUniqueOrSelf):
		# 	comment = 'Should always be used with non-empty Trace.'
		# >
		class hasBegin( Act >> ActBegin , *referencesToUnique): pass  # transitive over hasFirstAct (defined thru SWRL!)

		# # >
		# class hasLastAct( Act >> Act , hasDirectPart, *referencesToUniqueOrSelf): pass
		# >
		class hasEnd( Act >> ActEnd , *referencesToUnique): pass  # transitive over hasLastAct (defined thru SWRL!)

		# связь "следующий" в последовательности простых и составных актов (в началах и концах составных актов будет ветвление - разделение и схождение этих связей, соответственно).
		# >
		class hasNextAct( Act >> Act , *mutualUnique):
			comment = ''
		# # >
		# class hasNextAtom( TraceAtom >> TraceAtom , *mutualUnique):
		# 	comment = 'sequential link between TarceAtom instances'

		# транзитивное "ДО"
		# >
		class beforeAct( Act >> Act , *references): pass  # transitive over hasNextAct (defined thru SWRL!)

		# # >
		# class hasContext( Act >> Act , *referencesToUnique): pass  # use hasDirectPart (as inverse) instead

		# >
		class executes( TraceElement >> CodeElement , *referencesToUnique): pass
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

		def makeStringConcatPredicates(res_var : str, message : str, field_var_tuples: list) -> str:

			retry_ids = ""
			arguments = ""
			for field,var in field_var_tuples:
				retry_ids += "hasID(%s, %s_id), " % (var,var)
				arguments += """, "%s: ", %s_id""" % (field,var)

			return """%s stringConcat(%s, "%s "%s, ".")
		""" % (retry_ids, res_var, message, arguments)



		# print(makeStringConcatPredicates("?msg", "ActBeforeStartOfBlockError", [("a", "?a_act"),("b", "?b_act")]))


		swrl_rules = {}

		# >
		# class GenericRule(WithID):
		# 	comment = 'Base for all rules'
			# name
		# ->
		# class TraceRule(GenericRule):
		# 	comment = 'Base for all trace rules'

		# -->
		# class SequenceRule(TraceRule): pass

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
		# class SequenceRule(TraceRule): pass
		# --->
		# class ActOutOfContextRule(SequenceRule): pass
		# Срабатывает, если есть акт `act`, непосредственно вложенный в акт `act_c` (контекст),
		# в то время как их первоисточники в алгоритме (st и st_c) не состоят в таком же отношении вложенности (контекст st - st_c_actual - отличается от st_c, указанного в трассе):
		swrl_rules["ActOutOfContextError"] = """
			hasDirectPart(?act_c, ?act),
			executes(?act, ?st),
			executes(?act_c, ?st_c),
			hasDirectPart(?st_c_actual, ?st),

			DifferentFrom(?st_c, ?st_c_actual),
			 %s -> message(ERRORS, ?msg)
		""" % makeStringConcatPredicates("?msg", "ActOutOfContextError", [("act", "?act"),("context_stmt_expected", "?st_c_actual"),("context_stmt_found", "?st_c")])

		# Тестовая трасса
			#     A#1
			# :begin main_body#1
			#     A#2
			#     B#1
			#     C#1
			#     D#1
			# :end main_body#1


		# ---->
		# class ActIsContainedInSequenceRule(SequenceRule): pass
		# ---->
		# class OnlyOneActExcecutionInSequenceRule(SequenceRule): pass
		swrl_rules["DuplicateActsOfStmtError"] = """
			Block(?block),
			executes(?block_act, ?block),
			hasDirectPart(?block, ?st),

			executes(?act1, ?st),
			executes(?act2, ?st),
			hasDirectPart(?block_act, ?act1),
			hasDirectPart(?block_act, ?act2),

			DifferentFrom(?act1, ?act2)
		 -> message(ERRORS, "DuplicateActsOfStmtError")
		 """

		# ---->
		# class ExecuteActABeforeActBInSequenceRule(SequenceRule): pass

		# -->
		# class AlternativeRule(TraceRule): pass
		# --->
		# class AlternativeActExecuteRule(AlternativeRule): pass

		# -->
		# class LoopRule(TraceRule): pass
		# --->
		# class ExecuteBodyActAfterFalseConditionActRule(LoopRule): pass

		# --->
		# class WHILE_Rule(LoopRule): pass
		# ---->
		# class WhileLoopBodyActExecuteRule(WHILE_Rule): pass



		#################################
	#	######## Rule Properties ########
		#################################

		# >
		# class description( GenericRule >> str , DataProperty, FunctionalProperty): pass



		###############################
	#	######## Error Classes ########
		###############################

		# >
		class GenericError(Thing):
			comment = 'Base for all errors'
		# ->

		# persistent instance (global object)
		GenericError("ERRORS")  # to attach log messages


		##################################
	#	######## Error Properties ########
		##################################

		# >
		class message( GenericError >> str ): pass



		############################
	#	######## SWRL Rules ########
		############################

		rules = {
			# "BeforeActTransitive": """ Act(?b) ^ Act(?c) ^ :Act(?a) ^ beforeAct(?a, ?b) ^ beforeAct(?b, ?c) -> beforeAct(?a, ?c) """ ,
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

			# "hasFirstAct_to_hasBegin": """
			# 	 hasFirstAct(?a, ?b) -> hasBegin(?a, ?b)
			# """ ,
			# "hasBegin_transitive": """
			# 	 hasBegin(?a, ?b), hasBegin(?b, ?c) -> hasBegin(?a, ?c)
			# """ ,

			# "hasLastAct_to_hasEnd": """
			# 	 hasLastAct(?a, ?b) -> hasEnd(?a, ?b)
			# """ ,
			# "hasEnd_transitive": """
			# 	 hasEnd(?a, ?b), hasEnd(?b, ?c) -> hasEnd(?a, ?c)
			# """ ,

			# # связь before между началами и концами составных актов - через атомарные
			# "beforeAct_up": """
			# 	 hasNextAct(?e, ?b), hasEnd(?a, ?e), hasBegin(?n, ?b) -> beforeAct(?a, ?n)
			# """ ,


			# "NextL_to_before": """
	        # """ ,
		}

		for name, r in [*rules.items(), *swrl_rules.items()]:
			Imp(name).set_as_rule(r)

	return c_schema


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


def _main():

	c_schema = make_ontology()


	############################
	######## Export RDF ########
	############################

	onto_name = c_schema.base_iri.split('/')[-1][:-1]  # adds '#' at end
	# onto_name = my_iri.split('/')[-1]
	rdf_filename = onto_name + '.rdf'

	c_schema.save(file=rdf_filename, format='rdfxml')
	print("Saved RDF file: {} !".format(rdf_filename))

	# upload_rdf_to_SPARQL_endpoint('http://localhost:3030/c_owl/data', rdf_filename)



if __name__ == '__main__':
	_main()
