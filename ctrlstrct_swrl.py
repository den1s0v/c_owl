# ctrlstrct.swrl

RULES_DICT = {

# помечаем минусом в начале отключенные правила


                ###################
                ###################
################ Служебные правила ################
                ###################
                ###################


"hasNextAct_to_beforeAct": """
	next(?a, ?b) -> before(?a, ?b)
 """ ,

"BeforeActTransitive": """
	before(?a, ?b), before(?b, ?c) -> before(?a, ?c)
	""",
	# act(?a),
	# act(?b),
	# act(?c),
	
"parent_of_to_contains_child": """
	parent_of(?a, ?b) -> contains_child(?a, ?b)
 """ ,

"parent_of_to_contains_act": """
    parent_of(?a, ?b), act(?a), act(?b) -> contains_act(?a, ?b)
 """ ,

"contains_actTransitive": """
	contains_act(?a, ?b), contains_act(?b, ?c) -> contains_act(?a, ?c)
	""",


"DepthOfProgramIs0": """
	algorithm(?a), entry_point(?a, ?e), executes(?p, ?e) -> depth(?p, 0)
	""",

"DepthIncr": """
	act_begin(?a), next(?a, ?b), act_begin(?b), 
	depth(?a, ?da), add(?db, ?da, 1)
	 -> depth(?b, ?db), parent_of(?a, ?b)
	""",

"DepthSame_be": """
	act_begin(?a), next(?a, ?b), act_end(?b), 
	depth(?a, ?da), parent_of(?p, ?a)
	 -> depth(?b, ?da), parent_of(?p, ?b), corresponding_end(?a, ?b)
	""",
 # + добавить проверку на Начало А - Конец Б (должен был быть Конец А) - CorrespondingActsMismatch_Error
"DepthSame_eb": """
	act_end(?a), next(?a, ?b), act_begin(?b), 
	depth(?a, ?da), parent_of(?p, ?a)
	 -> depth(?b, ?da), parent_of(?p, ?b)
	""",

"DepthDecr": """
	act_end(?a), next(?a, ?b), act_end(?b), 
	depth(?a, ?da), subtract(?db, ?da, 1), 
	parent_of(?p, ?a)
	 -> depth(?b, ?db), corresponding_end(?p, ?b)
	""",

"SameParentOfCorrACts": """
	corresponding_end(?a, ?b), parent_of(?p, ?a)
	 -> parent_of(?p, ?b)
	""",


                ###################
                ###################
################ Смысловые правила ################
                ###################
                ###################


"CorrespondingActsMismatch_Error": """
	corresponding_end(?a, ?b), 
	executes(?a, ?s1),
	executes(?b, ?s2),
	DifferentFrom(?s1, ?s2),
	
	IRI(?a, ?a_iri),
	IRI(?b, ?b_iri),
	
	stringConcat(?cmd, "trace_error{arg=", ?a_iri, "; arg=", ?b_iri, "; message=[Corresponding Acts Mismatch Error (broken trace flow)]; }")
	 -> CREATE(INSTANCE, ?cmd)
""",


"-ActStartsAfterEnd_Error": """
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

"DuplicatesOfAct_Mistake": """
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
	
	stringConcat(?cmd, "trace_error{arg=", ?act2_iri, "; message=[Duplicate Acts Of Stmt Error]; }")
	 -> CREATE(INSTANCE, ?cmd)
""",


# Нужно вычислить настоящего, должного родительского объекта, затем всё просто.

"GenericMisplaced_Mistake": """
    act_begin(?act1),
    executes(?act1, ?st), 
    parent_of(?st2, ?st),

    parent_of(?act2, ?act1),
    executes(?act2, ?shouldbe_st2), 
	
    DifferentFrom(?shouldbe_st2, ?st2),
    
    IRI(?act1, ?act1_iri),
    IRI(?st2, ?st2_iri),
    IRI(?shouldbe_st2, ?shouldbe_st2_iri),
    
    stringConcat(?cmd, "trace_error{trace_error{arg=", ?act1_iri, "; trace_error{arg=", ?st2_iri, "; trace_error{arg=", ?shouldbe_st2_iri, "; message=[Act placed within inproper enclosing act]; }")
     -> CREATE(INSTANCE, ?cmd)
    
    
""",

# Акт находится в пределах родительского акта, но не непосредственно под ним

"-MissingAct_Mistake": """
    
""",


}
