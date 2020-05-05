# ctrlstrct.swrl

RULES_DICT = {

# помечаем минусом в начале отключенные правила

"hasNextAct_to_beforeAct": """
	 next(?a, ?b) -> before(?a, ?b)
 """ ,

"BeforeActTransitive": """
	before(?a, ?b), before(?b, ?c) -> before(?a, ?c)
	""",
	# act(?a),
	# act(?b),
	# act(?c),
	


"-ActStartsAfterEnd": """
	Context(?c)
	Block(?block)
	Statement(?stmt1)
	Act(?act1)
	Act(?act)

	hasContext(?act1, ?c)
	hasContext(?act,  ?c)
	hasFirst(?block, ?stmt1)
	executes(?c, ?block)
	executes(?act1, ?stmt1)
	before(?act, ?act1)

	hasIndex(?c, ?index)
	executes(?act, ?stmt)
	hasSource(?stmt, ?src)
	hasLocationSuffix(?stmt, ?stlbl)
	swrlb:stringConcat(?msg, "ActBeforeStartOfBlockError: act `", ?src, "` (", ?stlbl, "#", ?index, ") is placed before start of block.")
	 -> message(ERRORS, ?msg)
		
	""",

"DuplicatesOfAct": """
	sequence(?block), 
	executes(?block_act_b, ?block), 
	executes(?block_act_e, ?block), 

	act_begin(?act1),
	act_begin(?act2),

	body_item(?block, ?st), 
	executes(?act1, ?st), 
	executes(?act2, ?st), 
	
	before(?act1, ?act2), 
	
	before(?block_act_b, ?act1), 
	before(?block_act_b, ?act2), 
	before(?act1, ?block_act_e), 
	before(?act2, ?block_act_e), 

	DifferentFrom(?act1, ?act2),
	
	IRI(?act2, ?act2_iri),
	
	stringConcat(?cmd, "trace_error{message=DuplicateActsOfStmtError; arg=", ?act2_iri, "}")
	 -> CREATE(INSTANCE, ?cmd)
""",

"-MissingAct": """
	
""",


}
