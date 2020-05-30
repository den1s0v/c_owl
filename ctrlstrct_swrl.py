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

"correct_hasNextAct_to_correct_beforeAct": """
    correct_next(?a, ?b) -> correct_before(?a, ?b)
 """ ,

"BeforeActTransitive": """
	before(?a, ?b), before(?b, ?c) -> before(?a, ?c)
	""",
"correct_BeforeActTransitive": """
    correct_before(?a, ?b), correct_before(?b, ?c) -> correct_before(?a, ?c)
    """,
	# act(?a),
	# act(?b),
	# act(?c),
	
# ???
# "parent_of_to_contains_child": """
# 	parent_of(?a, ?b) -> contains_child(?a, ?b)
#  """ ,

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
"DepthIncr_correct": """
    act_begin(?a), correct_next(?a, ?b), act_begin(?b), 
    depth(?a, ?da), add(?db, ?da, 1)
     -> depth(?b, ?db), parent_of(?a, ?b)
    """,

"DepthSame_b-e": """
	act_begin(?a), next(?a, ?b), act_end(?b), 
	depth(?a, ?da), parent_of(?p, ?a)
	 -> depth(?b, ?da), parent_of(?p, ?b), corresponding_end(?a, ?b)
	""",
"DepthSame_b-e_correct": """
    act_begin(?a), correct_next(?a, ?b), act_end(?b), 
    depth(?a, ?da), parent_of(?p, ?a)
     -> depth(?b, ?da), parent_of(?p, ?b), corresponding_end(?a, ?b)
    """,
    
 # проверка на Начало А - Конец Б (должен был быть Конец А) - CorrespondingActsMismatch_Error
"DepthSame_e-b": """
	act_end(?a), next(?a, ?b), act_begin(?b), 
	depth(?a, ?da), parent_of(?p, ?a)
	 -> depth(?b, ?da), parent_of(?p, ?b)
	""",
"DepthSame_e-b_correct": """
    act_end(?a), correct_next(?a, ?b), act_begin(?b), 
    depth(?a, ?da), parent_of(?p, ?a)
     -> depth(?b, ?da), parent_of(?p, ?b)
    """,

"DepthDecr": """
	act_end(?a), next(?a, ?b), act_end(?b), 
	depth(?a, ?da), subtract(?db, ?da, 1), 
	parent_of(?p, ?a)
	 -> depth(?b, ?db), corresponding_end(?p, ?b)
	""",
"DepthDecr_correct": """
    act_end(?a), correct_next(?a, ?b), act_end(?b), 
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
	
	stringConcat(?cmd, "trace_error{arg=", ?a_iri, "; cause=", ?b_iri, "; message=[CorrespondingActsMismatchError (broken trace flow)]; }")
	 -> CREATE(INSTANCE, ?cmd)
""",

# ! OFF
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
	
	# before(?block_act_b, ?act1), 
	# before(?block_act_b, ?act2), 
	# before(?act1, ?block_act_e), 
	# before(?act2, ?block_act_e), 
    parent_of(?block_act_b, ?act1), 
    parent_of(?block_act_b, ?act2), 
    

	DifferentFrom(?act1, ?act2),
	
	IRI(?act2, ?act2_iri),
	
	stringConcat(?cmd, "trace_error{cause=", ?act2_iri, "; message=[DuplicateActs Of Stmt Error]; }")
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
    IRI(?act2, ?act2_iri),
    IRI(?st, ?st_iri),
    IRI(?st2, ?st2_iri),
    IRI(?shouldbe_st2, ?shouldbe_st2_iri),
    
    stringConcat(?cmd, "trace_error{cause=", ?act1_iri, "; arg=", ?act2_iri, "; arg=", ?st2_iri, "; arg=", ?st_iri, "; arg=", ?shouldbe_st2_iri, "; message=[WrongContext: Act placed within inproper enclosing act]; }")
     -> CREATE(INSTANCE, ?cmd)
""",

    # act1 = 85b_otvet_negativnyj_n1
    # act2 = 83b_po_otvetu_n1
    # shouldbe_st2 = 4_po_otvetu
    # st2 = 9_elseif-otvet_negativnyj
    # st = 10_otvet_negativnyj
    

# Акт находится в пределах родительского акта, но не непосредственно под ним
# ...


# Здесь, думаю, надо добавить в upd_onto счётчик связей
"-MissingAct_Mistake": """
    
""",


"ActsPairMisorder_Mistake": """

    # начало и конец акта блока
    sequence(?block), 
    executes(?block_act_b, ?block), 
    corresponding_end(?block_act_b, ?block_act_e), 

    act_begin(?act1),
    act_begin(?act2),

    # акты в пределах акта блока
    # before(?block_act_b, ?act1), 
    # before(?block_act_b, ?act2), 
    # before(?act1, ?block_act_e), 
    # before(?act2, ?block_act_e), 
    parent_of(?block_act_b, ?act1), 
    parent_of(?block_act_b, ?act2), 

    # акты выполняют пару последовательных действий
    body_item(?block, ?st1), 
    body_item(?block, ?st2), 
    next(?st1, ?st2),         # st1 --> st2
    executes(?act1, ?st1), 
    executes(?act2, ?st2), 
    
    # но сами стоят в другом порядке.
    before(?act2, ?act1), 
    
    IRI(?act2, ?act2_iri),
    IRI(?act1, ?act1_iri),
    
    stringConcat(?cmd, "trace_error{cause=", ?act2_iri, "; arg=", ?act1_iri, "; message=[TooEarly: Act should not occure before the act it must follow]; }")
     -> CREATE(INSTANCE, ?cmd)
""",

"Init_Count_std_and_corr_acts": """
    # executes(?std_act, ?st),
    # student_act(?std_act),
    # act_begin(?std_act),
    # executes(?corr_act, ?st),
    correct_act(?corr_act),
    act_begin(?corr_act),
    # DifferentFrom(?std_act, ?corr_act)
     -> COUNT_has_student_act(?corr_act, true), COUNT_has_correct_act(?corr_act, true)
     # -> LINK_COUNT_has_student_act(?corr_act, true), LINK_COUNT_has_correct_act(?corr_act, true)

""",
"Count_std_acts": """
    executes(?std_act, ?st),
    student_act(?std_act),
    act_begin(?std_act),
    
    executes(?corr_act2, ?st),
    correct_act(?corr_act2),
    act_begin(?corr_act2),
    
    parent_of(?par_act, ?std_act),  # в пределах одного объемлющего акта
    parent_of(?par_act, ?corr_act2),
    
    # DifferentFrom(?std_act, ?corr_act2)
     -> has_student_act(?corr_act2, ?std_act)
""",
"Count_corr_acts": """
    executes(?corr_act1, ?st),
    correct_act(?corr_act1),
    act_begin(?corr_act1),
    executes(?corr_act2, ?st),
    correct_act(?corr_act2),
    act_begin(?corr_act2),
    parent_of(?par_act, ?corr_act1),  # в пределах одного объемлющего акта
    parent_of(?par_act, ?corr_act2),
     -> has_correct_act(?corr_act1, ?corr_act2)
""",

# Подготовка к сопоставлению корректных актов студенческим
"-AlignSequenceActs_student-correct": """

    # sequence(?block), 
    # parent_of(?block, ?st),
    
    executes(?std_act, ?st),
    student_act(?std_act),
    executes(?corr_act, ?st),
    student_act(?corr_act),
    
    # DifferentFrom(?std_act, ?corr_act),
    
    COUNT_has_student_act()
    
    IRI(?act2, ?act2_iri),
    IRI(?act1, ?act1_iri),
    
    stringConcat(?cmd, "trace_error{cause=", ?act2_iri, "; arg=", ?act1_iri, "; message=[TooEarly: Act should not occure before the act it must follow]; }")
     -> CREATE(INSTANCE, ?cmd)
""",


# Подготовка к подсчёту числа связей
"-PrepareCountingSequence_student-correct": """

    # # начало и конец акта блока
    # sequence(?block), 
    # executes(?block_act_b, ?block), 
    # corresponding_end(?block_act_b, ?block_act_e), # построение актов следования завершено
    # body_item(?block, ?st),

    #     # act_begin(?act1),
    #     # # акт в пределах акта блока
    #     # parent_of(?block_act_b, ?act1)

    # IRI(?block_act_b, ?block_act_b_iri),
    # IRI(?st, ?st_iri),
    
    # stringConcat(?cmd, "Counter{arg=", ?block_act_b_iri, "; arg=", ?st_iri, "; COUNT_target=true;}")
    #  -> CREATE(INSTANCE, ?cmd)
""",

# Подготовка к подсчёту числа связей
"-PrepareCountingSequenceActs": """

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
    
    stringConcat(?cmd, "Counter{arg=", ?block_act_b_iri, "; arg=", ?st_iri, "; COUNT_target=true;}")
     -> CREATE(INSTANCE, ?cmd)
""",

# Подсчёт числа связей
"-CountSequenceActs": """

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
    correct_act(?corr_act2),
    # act_begin(?corr_act2),
    
    N_has_student_act(?corr_act2, ?std_n),
    N_has_correct_act(?corr_act2, ?corr_n),
    
    lessThan(?std_n, ?corr_n),  # не хватает актов в трассе студента
    
    # stringConcat(?cmd, "std_n=", ?std_n, "; corr_n=", ?corr_n)
    # -> expr_value(?corr_act2, ?cmd)
    # -> expr_value(?corr_act2, ?std_n)
    
    # correct_next(?corr_act2, ?next_corr_act), # следующий за пропущенным
    # correct_act(?next_corr_act),
    # student_act(?next_corr_act),
    
    IRI(?corr_act2, ?corr_act_iri),
    # IRI(?next_corr_act, ?next_corr_act_iri),
    
    stringConcat(?cmd, "trace_error{cause=", ?corr_act_iri, "; arg=", ?corr_act_iri, "; message=[MissingActAnywhere, not only In Sequence]; }")
     -> CREATE(INSTANCE, ?cmd)
""",

"-Test_lessThan": """
    lessThan(0, 1)
     -> expr_value(INSTANCE, "debug: lessThan works!")  # OK!
 """,

"-Test_int_prop2": """
    Counter(?counter),
    COUNT_target(?counter, 0)

     ->  arg(?counter, ?counter)  # DEBUG
""",


}

# strip all the comments out ...
# ... replacing them by spaces in order to preserve char positions reported by lexing parser
comment_re = re.compile(r"(?://|#).*$")

for k in tuple(RULES_DICT.keys()):
    if k.startswith("-"):
        # print("skipping SWRL rule due to minus: \t", k)
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
