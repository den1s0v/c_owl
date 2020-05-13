# ctrlstrct.swrl

import re

RULES_DICT = {

# помечаем минусом в начале имени отключенные правила.
# из текста удаляются комментарии в стиле Си и Python.


                ###################
                ###################
################ Служебные правила ################
                ###################
                ###################


"hasNextAct_to_beforeAct": """
	next(?a, ?b) -> before(?a, ?b)

    # an comment !!!
    // Another one.
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


# entry_point       program executes        first act executes
# 
# global_code       global_code.body        global_code.body.first
# 
# func_a            func_a.body             func_a.body.first

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


# Нужно вычислить настоящий, должный родительский объект, затем всё просто.

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
# ...


# Здесь, думаю, надо добавить в upd_onto счётчик связей
"-MissingAct_Mistake": """
    
""",


"ActsPairMisorder_Mistake": """

    # начало и конец акта блока
    sequence(?block), 
    executes(?block_act_b, ?block), 
    executes(?block_act_e, ?block), 

    act_begin(?act1),
    act_begin(?act2),

    # акты в пределах акта блока
    before(?block_act_b, ?act1), 
    before(?block_act_b, ?act2), 
    before(?act1, ?block_act_e), 
    before(?act2, ?block_act_e), 

    # акты выполняют пару последовательных действий
    body_item(?block, ?st1), 
    body_item(?block, ?st2), 
    next(?st1, ?st2),
    executes(?act1, ?st1), 
    executes(?act2, ?st2), 
    
    # но сами стоят в другом порядке.
    before(?act2, ?act1), 
    
    IRI(?act2, ?act2_iri),
    IRI(?act1, ?act1_iri),
    
    stringConcat(?cmd, "trace_error{arg=", ?act2_iri, "; arg=", ?act1_iri, "; message=[Act occurs before its precedent]; }")
     -> CREATE(INSTANCE, ?cmd)
""",

# Подготовка к подсчёту числа связей
"PrepareCountingSequenceActs": """

    # начало и конец акта блока
    sequence(?block), 
    executes(?block_act_b, ?block), 
    corresponding_end(?block_act_b, ?block_act_e), # построение актов следования завершено
    body_item(?block, ?st),

        # act_begin(?act1),
        # # акт в пределах акта блока
        # parent_of(?block_act_b, ?act1)

    IRI(?block_act_b, ?block_act_b_iri),
    IRI(?st, ?st_iri),
    
    stringConcat(?cmd, "Counter{arg=", ?block_act_b_iri, "; arg=", ?st_iri, "; COUNT_target=-1;}")
     -> CREATE(INSTANCE, ?cmd)
""",
# Подсчёт числа связей
"CountSequenceActs": """

    # # начало и конец акта блока
    # sequence(?block), 
    # executes(?block_act_b, ?block), 
    # corresponding_end(?block_act_b, ?block_act_e), # построение актов следования завершено
    # body_item(?block, ?st),

    # акт существует, получим счётчик
    Counter(?counter),
    arg(?counter, ?block_act_b),
    arg(?counter, ?st),

    executes(?act1, ?st),  # акт нужного действия
    act_begin(?act1),
    parent_of(?block_act_b, ?act1) # акт в пределах акта блока

    # привязываем найденный акт, чтобы посчитать его
     -> target(?counter, ?act1)
""",

# помечаем конец следования как ошибочный, если акт отсутствует
# Надо указать на акт, следующий за пропущенным ...
"MissingActInSequence_Mistake": """
    Counter(?counter),
    COUNT_target(?counter, ?n),
    equal(?n, 0),  # lessThan(?n, 1) - может сработать на начальном -1
    arg(?counter, ?block_act_b),
    arg(?counter, ?st),

    corresponding_end(?block_act_b, ?block_act_e), # конец следования
    
    IRI(?block_act_e, ?block_act_e_iri),
    IRI(?st, ?st_iri),
    
    stringConcat(?cmd, "trace_error{arg=", ?block_act_e_iri, "; arg=", ?st_iri, "; message=[MissingActInSequence]; }")
     -> CREATE(INSTANCE, ?cmd)
""",

"-Aaa_Mistake": """
    
""",


}

# strip all the comments out ...
# ... replacing them by spaces in order to preserve char positions reported by lexing parser
comment_re = re.compile(r"(?://|#).*$")

for k in tuple(RULES_DICT.keys()):
    if k.startswith("-"):
        print("skipping SWRL rule due to minus: \t", k)
        del RULES_DICT[k]
        continue
    txt = RULES_DICT[k]
    lines = [
                comment_re.sub(lambda m:" "*len(m.group(0)), line)
                for line in 
                txt.split("\n")
            ]
    RULES_DICT[k] = "\n".join(lines)
    
# print(RULES_DICT)
