# ctrlstrct.swrl

import re

RULES_DICT = {

# помечаем минусом в начале имени отключенные правила.
# из текста удаляются комментарии в стиле Си (//) и Python (#).


				###################
				###################
################ Служебные правила ################
				###################
				###################

# # (s1)
# "---- next_to__current_act_rule_s1": """
# 	correct_act(?a), index(?a, ?ia), add(?ib, ?ia, 1),
# 	act(?b), index(?b, ?_ib),
# 	equal(?_ib, ?ib), 
# 	 -> next_act(?a, ?b)
#  """,

"- hasNextAct_to_beforeAct": """
	next_act(?a, ?b) -> before(?a, ?b)  # 'before' connects correct acts and acts next_act to current, only.

	# a comment in rule!
	// Another one.
 """,

# (s2)
"---- assign_next_sibling_0-1-b_rule_s2": """
	trace(?a),
	act_begin(?b), exec_time(?b, ?_ib),
	equal(?_ib, 1),
	# DifferentFrom(?a, ?b),  # stardog fails the rule here!
	 -> next_sibling(?a, ?b)
 """,
# (s3)
"---- assign_next_sibling_0-1-e_rule_s3": """
	trace(?a),
	act_end(?b), exec_time(?b, ?_ib),
	equal(?_ib, 1), 
	# DifferentFrom(?a, ?b),
	 -> next_sibling(?a, ?b)
 """,
# (s4)
"---- assign_next_sibling-b_rule_s4": """
	act_begin(?a), exec_time(?a, ?ia), add(?_ib, ?ia, 1),
	act_begin(?b), exec_time(?b, ?ib),  # unification of a bound var does rebind in stardog ??!
	equal(?_ib, ?ib), 
	# DifferentFrom(?a, ?b),
	executes(?a, ?st),
	executes(?b, ?st),
	 -> next_sibling(?a, ?b)
 """,
# (s5)
"---- assign_next_sibling-e_rule_s5": """
	act_end(?a), exec_time(?a, ?ia), add(?_ib, ?ia, 1),
	act_end(?b), exec_time(?b, ?ib),
	equal(?_ib, ?ib), 
	# DifferentFrom(?a, ?b),
	executes(?a, ?st),
	executes(?b, ?st),
	 -> next_sibling(?a, ?b)
 """,

	
# ???
# "parent_of_to_contains_child": """
# 	parent_of(?a, ?b) -> contains_child(?a, ?b)
#  """ ,

# "- parent_of_to_contains_act": """
# 	parent_of(?a, ?b), act(?a), act(?b) -> contains_act(?a, ?b)
#  """ ,




# entry_point       program executes        first act executes
# 
# global_code       global_code.body        global_code.body.first
# 
# func_a            func_a.body             func_a.body.first


"Incr_index": """
	next_act(?a, ?b), index(?a, ?ia), add(?ib, ?ia, 1)
	 -> index(?b, ?ib)""",
"-hardcoded- student_Incr_index": """
	student_next(?a, ?b), student_index(?a, ?ia), add(?ib, ?ia, 1)
	 -> student_index(?b, ?ib)""",

# (s6)
"DepthIncr_rule_s6": """
	act_begin(?a), next_act(?a, ?b), act_begin(?b)
	 -> parent_of(?a, ?b)
	""",
"student_DepthIncr_rule_s6": """
	act_begin(?a), student_next(?a, ?b), act_begin(?b)
	 -> student_parent_of(?a, ?b)
	""",

# (s7)
"DepthSame_b-e_rule_s7": """
	act_begin(?a), next_act(?a, ?b), act_end(?b), 
	parent_of(?p, ?a),
	 -> parent_of(?p, ?b), corresponding_end(?a, ?b)
	""",
"student_DepthSame_b-e_rule_s7": """
	act_begin(?a), student_next(?a, ?b), act_end(?b), 
	student_parent_of(?p, ?a),
	 -> student_parent_of(?p, ?b), student_corresponding_end(?a, ?b)
	""",
	
# (s8)
 # проверка на Начало А - Конец Б (должен был быть Конец А) - CorrespondingActsMismatch_Error
"DepthSame_e-b_rule_s8": """
	act_end(?a), next_act(?a, ?b), act_begin(?b), 
	parent_of(?p, ?a)  # depth(?a, ?da),
	 -> parent_of(?p, ?b)  # depth(?b, ?da), 
	""",
"student_DepthSame_e-b_rule_s8": """
	act_end(?a), student_next(?a, ?b), act_begin(?b), 
	student_parent_of(?p, ?a)
	 -> student_parent_of(?p, ?b)
	""",

# (s9)
"DepthDecr_rule_s9": """
	act_end(?a), next_act(?a, ?b), act_end(?b), 
	parent_of(?p, ?a)
	 -> corresponding_end(?p, ?b)
	""",
"student_DepthDecr_rule_s9": """
	act_end(?a), student_next(?a, ?b), act_end(?b), 
	student_parent_of(?p, ?a)
	 -> student_corresponding_end(?p, ?b)
	""",

# (s10)
"SameParentOfCorrActs_rule_s10": """
	corresponding_end(?a, ?b), parent_of(?p, ?a)
	 -> parent_of(?p, ?b)
	""",
"student_SameParentOfCorrActs_rule_s10": """
	corresponding_end(?a, ?b), student_parent_of(?p, ?a)
	 -> student_parent_of(?p, ?b)
	""",


				######################
				######################
################ Производящие правила ################
				######################
				######################

# Точка входа в трассу - функция  [works with Pellet] [works with Stardog]
"start__to__MainFunctionBegin__rule_g3": """
	trace(?a),
	executes(?a, ?alg),
	entry_point(?alg, ?func_),
	func(?func_), 
	# DifferentFrom(?a, ?b),  # здесь не нужно, но правило от этого ломается (хотя и не ломает остальной вывод)!
	act_begin(?b),
		# next_sibling(?pr, ?b), correct_act(?pr),
	next_sibling(?a, ?b),  # ?pr === ?a
	executes(?b, ?func_),

	 -> correct_act(?b), 
	 next_act(?a, ?b), 
	 FunctionBegin(?b)
""",

# Точка входа в трассу - глобальный код  [works with Pellet]
"start__to__GlobalCode__rule_g4": """
	trace(?a),
	executes(?a, ?alg),
	entry_point(?alg, ?gc),
	sequence(?gc), 

	act_begin(?b),
		# next_sibling(?pr, ?b), correct_act(?pr),
	next_sibling(?a, ?b),  # ?pr === ?a
	executes(?b, ?gc),

	 -> correct_act(?b), 
	 next_act(?a, ?b), GlobalCodeBegin(?b)
""",


# OK !
# Начало тела функции  [works with Pellet] [works with Stardog]
"connect_FunctionBodyBegin_rule_g5": """
	correct_act(?a),
	act_begin(?a),
	func(?func_), 
	executes(?a, ?func_),
	body(?func_, ?st),
	
	act_begin(?b),
	next_sibling(?pr, ?b), correct_act(?pr),  # check that previous execution of st was in correct sub-trace
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),

	executes(?b, ?st),
	# SameAs(?st, ?_st), # stardog fails with error here
	
	 -> correct_act(?b), 
	 next_act(?a, ?b), 
	 FunctionBodyBegin(?b)
""",
# Конец тела функции
"connect_FuncBodyEnd_rule_g5-2": """
	correct_act(?a),
	act_end(?a),
	func(?func_), 
	body(?func_, ?st),
	executes(?a, ?st),
	
	act_end(?b),
	executes(?b, ?func_),
	next_sibling(?pr, ?b), correct_act(?pr),  # check that previous execution of st was in correct sub-trace
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),
	
	 -> next_act(?a, ?b), FunctionEnd(?b)  # correct_act(?b),
""",

# Первый акт следования [works with Pellet] [FAILS with Stardog...]
# Пустые следования (без действий) не поддерживаются!
"connect_SequenceBegin_rule_g2": """
	correct_act(?a),
	act_begin(?a),
	sequence(?block), 
	executes(?a, ?block),
	body_item(?block, ?st),
	first_item(?st),
	
	act_begin(?b),
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),
	executes(?b, ?st),
	
	 -> correct_act(?b), next_act(?a, ?b), SequenceBegin(?b)
""",

# Следующий акт следования [works with Pellet]
"connect_SequenceNext": """
	correct_act(?a),
	act_end(?a),
	parent_of(?p, ?a),
	sequence(?block), 
	executes(?p, ?block),
	body_item(?block, ?st),
	executes(?a, ?st),
	
	next(?st, ?st2),
	
	act_begin(?b),
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),
	executes(?b, ?st2),
	
	 -> correct_act(?b), 
	  next_act(?a, ?b), 
	  SequenceNext(?b)
""",

# Начало и конец простого акта [works with Pellet]
"connect_StmtEnd": """
	correct_act(?a),
	act_begin(?a),
	stmt(?st), 
	executes(?a, ?st),
	
	act_end(?b),
	# next_sibling(?pr, ?b), correct_act(?pr),
	# 	index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),
	executes(?b, ?st),
	
	exec_time(?a, ?t), exec_time(?b, ?_t),
	equal(?t, ?_t),
	 -> correct_act(?b), next_act(?a, ?b), StmtEnd(?b)
""",

# Начало и конец акта выражения [works with Pellet]
"connect_ExprEnd": """
	correct_act(?a),
	act_begin(?a),
	expr(?st), 
	executes(?a, ?st),
	
	act_end(?b),
	executes(?b, ?st),
	
	exec_time(?a, ?t), exec_time(?b, ?_t),
	equal(?t, ?_t),
	 -> correct_act(?b), next_act(?a, ?b), ExprEnd(?b)
""",

#  [works with Pellet]
"connect_SequenceEnd": """
	correct_act(?a),
	act_end(?a),
	executes(?a, ?st),
	last_item(?st),
	
	act_end(?b),
	parent_of(?p, ?a),
	executes(?p, ?block),
#	sequence(?block),    # ???
	executes(?b, ?block),
	body_item(?block, ?st),
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),
	 -> correct_act(?b), next_act(?a, ?b), SequenceEnd(?b)
""",


# ===== Alt ===== #


# Проверка первого условия развилки (if) [works with Pellet]
"connect_AltBegin": """
	correct_act(?a),
	act_begin(?a),
	alternative(?alt), 
	executes(?a, ?alt),

	branches_item(?alt, ?br),
	first_item(?br),	# one of that lines is enough
	# if(?br),			# one of that lines is enough
	cond(?br, ?cnd),
	
	act_begin(?b),
	executes(?b, ?cnd),  # expr
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),

	# exec_time(?a, ?t), exec_time(?b, ?_t),
	# equal(?t, ?_t),
	 -> correct_act(?b), next_act(?a, ?b), AltBegin(?b)
""",

# Начало ветки истинного условия развилки [works with Pellet]
"connect_AltBranchBegin_CondTrue": """
	correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, true),  # condition passed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative
	
	act_begin(?b),
	executes(?b, ?br),
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),

	 -> correct_act(?b), next_act(?a, ?b), AltBranchBegin(?b)
""",

# Проверка следующего условия развилки (else-if) [works with Pellet]
"connect_NextAltCondition": """
	correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, false),  # condition failed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative

	next(?br, ?br2),
	cond(?br2, ?cnd2),
	
	act_begin(?b),
	executes(?b, ?cnd2),  # expr
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),

	 -> correct_act(?b), next_act(?a, ?b), NextAltCondition(?b)
""",

# Переход к ветке ИНАЧЕ (else)  [works with Pellet]
"connect_AltElseBranch": """
	correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, false),  # condition failed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative
	next(?br, ?br2),
	else(?br2),
	
	act_begin(?b),
	executes(?b, ?br2),  # expr

	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),

	 -> correct_act(?b), next_act(?a, ?b), AltElseBranchBegin(?b)
""",

# Конец развилки, т.к. все условия ложны [works with Pellet]
"connect_AltEndAllFalse": """
	correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, false),  # condition failed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative
	branches_item(?alt, ?br),
	last_item(?br),   # the branch is last in alternative
	alternative(?alt),
	
	act_end(?b),
	executes(?b, ?alt),  # expr

	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),

	 -> correct_act(?b), next_act(?a, ?b), AltEndAllFalse(?b)
""",

# Окончание развилки по завершению ветки [works with Pellet]
"connect_AltEndAfterBranch": """
	correct_act(?a),
	act_end(?a),
	executes(?a, ?br),
	branches_item(?alt, ?br),
	alternative(?alt), 

	act_end(?b),
	executes(?b, ?alt),  # ends whole alternative
	next_sibling(?pr, ?b), correct_act(?pr),
		index(?a, ?ia), index(?pr, ?ipr), lessThan(?ipr, ?ia),
	 -> correct_act(?b), next_act(?a, ?b), AltEndAfterBranch(?b)
""",

# (6 generating rules to construct alternatives)



	 	 # dont forget to add suffix '_rule_#' if continue testing the rules.


				###################
				###################
################ Смысловые правила ################
				###################
				###################


"CorrespondingActsMismatch_Error": """
	student_corresponding_end(?a, ?b), 
	executes(?a, ?s1),
	executes(?b, ?s2),
	# DifferentFrom(?s1, ?s2),
		id(?s1, ?ib),
		id(?s2, ?ic),
		notEqual(?ib, ?ic),
	 -> CorrespondingEndMismatched(?b), cause(?b, ?a)
""",

"-ErrOff- CorrespondingActsHaveDifferentExecTime_Error": """
	student_corresponding_end(?a, ?b), 
	executes(?a, ?st),
	executes(?b, ?st),
		# executes(?a, ?s1),
		# executes(?b, ?s2),
		# SameAs(?s1, ?s2),
	exec_time(?a, ?n1),
	exec_time(?b, ?n2),
	notEqual(?n1, ?n2),
	 -> CorrespondingEndPerformedDifferentTime(?b), cause(?b, ?a)
""",


"GenericWrongAct_Error": """
	next_act(?a, ?b),
	student_next(?a, ?c),
	# DifferentFrom(?b, ?c),
		id(?b, ?ib),
		id(?c, ?ic),
		notEqual(?ib, ?ic),
	 -> should_be(?c, ?b), 
	 cause(?c, ?a), 
	 Erroneous(?c)
""",

"GenericWrongParent_Error": """
	parent_of(?p, ?a),
	student_parent_of(?c, ?a),
	# DifferentFrom(?p, ?c),
		id(?p, ?ip),
		id(?c, ?ic),
		notEqual(?ip, ?ic),
	 -> context_should_be(?a, ?p), 
	 # cause(?a, ?c), 
	 WrongContext(?a)
""",


"- EndAfterTraceEnd_Error": """
	act_end(?a),
	parent_of(?p, ?a), index(?p, 0),  # top-level act representing trace only has index of 0.
	next_act(?a, ?b), ## act(?b), 
	 -> AfterTraceEnd(?b), cause(?b, ?a)
	""",




# ! OFF
"- - ActStartsAfterEnd_Error": """
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

"---------- DuplicatesOfAct_Mistake": """
	sequence(?block), 
	act_begin(?block_act_b),
	executes(?block_act_b, ?block), 

	body_item(?block, ?st), 
	executes(?a, ?st), 
	executes(?b, ?st), 
	
	parent_of(?block_act_b, ?a),
	parent_of(?block_act_b, ?b),
	act_begin(?a),
	act_begin(?b),
	DifferentFrom(?a, ?b),

	before(?a, ?b), 
	 -> DuplicateActInSequence >>> DuplicateOfAct? (?b), cause(?b, ?a)
""",


"- GenericDisplaced_Mistake": """
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


"- -MissingAct_Mistake": """
	
""",


"- ActsPairMisorder_Mistake": """

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
	next(?st1, ?st2),         # st1 -> st2
	executes(?act1, ?st1), 
	executes(?act2, ?st2), 
	
	# но сами стоят в другом порядке.
	before(?act2, ?act1), 
	
	IRI(?act2, ?act2_iri),
	IRI(?act1, ?act1_iri),
	
	stringConcat(?cmd, "trace_error{cause=", ?act2_iri, "; arg=", ?act1_iri, "; message=[TooEarly: Act should not occure before the act it must follow]; }")
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

# ============ Sequence mistakes ============ #

# Дубликат акта в следовании [works with Pellet]
# Базируется на ExtraAct
"DuplicateOfAct-seq-b_Error": """
	ExtraAct(?c1), 
	act_begin(?c1),
	student_parent_of(?p, ?c1),
	executes(?p, ?block),
	sequence(?block),
		body_item(?block, ?st),  # just to ensure the sequence is real (and thus has "body_item"s)
	executes(?c1, ?st),

	executes(?c, ?st),
	parent_of(?p, ?c),
	act_begin(?c),

		id(?p, ?ip),
		id(?c, ?ic),
		notEqual(?ip, ?ic),
	 -> cause(?c1, ?c), 
	 DuplicateOfAct(?c1)
""",
# Дубликат акта в следовании [works with Pellet]
# Базируется на ExtraAct
"DuplicateOfAct-seq-e_Error": """
	ExtraAct(?c1), 
	act_end(?c1),
	student_parent_of(?p, ?c1),
	executes(?p, ?block),
	sequence(?block),
		body_item(?block, ?st),  # just to ensure the sequence is real (and thus has "body_item"s)
	executes(?c1, ?st),

	executes(?c, ?st),
	parent_of(?p, ?c),
	act_end(?c),

		id(?p, ?ip),
		id(?c, ?ic),
		notEqual(?ip, ?ic),
	 -> cause(?c1, ?c), 
	 DuplicateOfAct(?c1)
""",

# Перемещённый акт [works with Pellet]
# Базируется одновременно на ExtraAct и MissingAct
"DisplacedAct_Error": """
	ExtraAct(?c1), 
	MissingAct(?c1), 
	 -> DisplacedAct(?c1)
""",

# ============ Alternatives mistakes ============ #

# Развилка не начинается с условия [works with Pellet]
"NoFirstCondition-alt_Error": """
	act_begin(?a),
	executes(?a, ?alt),
	alternative(?alt), 

	student_next(?a, ?b),
	Erroneous(?b), 
	 -> NoFirstCondition(?b)
""",

# Ветка при ложном условии [works with Pellet]
"BranchOfFalseCondition-alt_Error": """
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, false),  # condition failed

	cond(?br, ?cnd),  # corresponding branch
	alt_branch(?br),  # belonds to an alternative

	student_next(?a, ?b),
	Erroneous(?b), 	  # как страховка, сработает и без этого
	
	act_begin(?b),
	executes(?b, ?br),
	 -> BranchOfFalseCondition(?b)
""",

# Условие после ветки  [works with Pellet]
"ConditionAfterBranch-alt_Error": """
	act_end(?a),
	executes(?a, ?br),
	branches_item(?alt, ?br),
	alternative(?alt), 

	student_next(?a, ?b),
	ExtraAct(?b), 	  # как страховка, сработает и без этого
	# act_begin(?b),
	executes(?b, ?cnd),
	expr(?cnd), 	# a condition
	
	 -> ConditionAfterBranch(?b)
""",

# Вторая ветка в альтернативе [works with Pellet]
"AnotherExtraBranch-alt_Error": """
	act_end(?a),
	executes(?a, ?br),
	branches_item(?alt, ?br),
	alternative(?alt), 

	student_next(?a, ?b),
	ExtraAct(?b), 	  # как страховка, сработает и без этого
	# act_begin(?b),
	executes(?b, ?br2),
	branches_item(?alt2, ?br2),
	
	 -> AnotherExtraBranch(?b)
""",

# После истинного условия нет его ветки [works with Pellet]
"NoBranchWhenConditionIsTrue-alt_Error": """
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, true),  # condition passed

	cond(?br, ?cnd),  # corresponding branch
	alt_branch(?br),  # belonds to an alternative

	student_next(?a, ?b),
	Erroneous(?b), 	  # как страховка, сработает и без этого
	
	 -> NoBranchWhenConditionIsTrue(?b)
""",

"AllFalseNoElse-alt_Error": """
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, false),  # condition failed
	cond(?br, ?cnd),  # corresponding branch
	next(?br, ?br2),
	else(?br2), 	  # "else" branch expected

	student_next(?a, ?b),
	Erroneous(?b),
	
	 -> AllFalseNoElse(?b)
""",

"NoNextCondition-alt_Error": """
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	corresponding_end(?a1, ?a),  # refer to act begin that holds expr_value
	expr_value(?a1, false),  # condition failed
	cond(?br, ?cnd),  # corresponding branch
	next(?br, ?br2),
	cond(?br2, ?cnd2), 	  # one more condition expected

	student_next(?a, ?b),
	Erroneous(?b),
	
	 -> NoNextCondition(?b)
""",


}

_more_rules = {}
for i in range(1, 6+1):

	pattern1 = ''.join([f"student_next(?c{j}, ?c{j+1}), " for j in range(1,i)])
	pattern2 = f"student_next(?c{i}, ?b),"
	action = ', '.join([f"ExtraAct(?c{j})" for j in range(1,i+1)])
	_more_rules.update({
		f"ExtraAct_{i}_Error": f"""
			next_act(?a, ?b),
			student_next(?a, ?c1),
			# DifferentFrom(?b, ?c1),
			{pattern1}
			{pattern2}
			 -> {action} ## ExtraAct(?c1)
		""",

		})

	pattern1 = ''.join([f"next_act(?c{j}, ?c{j+1}), "
						for j in range(1,i)])
	pattern2 = f"next_act(?c{i}, ?b),"
	action = ',  '.join([f"MissingAct(?c{j}), should_be_before(?c{j}, ?b)"
						for j in range(1,i+1)])
	_more_rules.update({
		f"MissingAct_{i}_Error": f"""
			student_next(?a, ?b),
			next_act(?a, ?c1),
			# DifferentFrom(?b, ?c1),
			{pattern1}
			{pattern2}
			 -> {action}, ## MissingAct(?c1)]
			 TooEarly(?b)
		""",

		})

RULES_DICT.update(_more_rules)

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

if 1:  # check correctness of modified rules text
	with open("swrl_dbg.txt", "w") as f:
	# 	# f.write(repr(RULES_DICT))
		for k, v in RULES_DICT.items():
			print(f'"{k}": ', end="", file=f)
			print(v, file=f)

		# print(RULES_DICT)
	
# debug! # RULES_DICT = {}
