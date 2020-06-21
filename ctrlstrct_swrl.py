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

# (s1)
"next_to__current_act": """
	current_act(?a), index(?a, ?ia), add(?ib, ?ia, 1),
	act(?b), index(?b, ?_ib),
	equal(?_ib, ?ib), 
	 -> next(?a, ?b)
 """,

"- hasNextAct_to_beforeAct": """
	next(?a, ?b) -> before(?a, ?b)  # 'before' connects correct acts and acts next to current, only.

	# a comment in rule!
	// Another one.
 """,

# (s2)
"assign_next_sibling_0-1-b": """
	trace(?a),
	act_begin(?b), exec_time(?b, ?_ib),
	equal(?_ib, 1),
	# DifferentFrom(?a, ?b),  # stardog fails the rule here!
	 -> next_sibling(?a, ?b)
 """,
# (s3)
"assign_next_sibling_0-1-e": """
	trace(?a),
	act_end(?b), exec_time(?b, ?_ib),
	equal(?_ib, 1), 
	# DifferentFrom(?a, ?b),
	 -> next_sibling(?a, ?b)
 """,
# (s4)
"assign_next_sibling-b": """
	act_begin(?a), exec_time(?a, ?ia), add(?_ib, ?ia, 1),
	act_begin(?b), exec_time(?b, ?ib),  # unification of a bound var does rebind in stardog ??!
	equal(?_ib, ?ib), 
	# DifferentFrom(?a, ?b),
	executes(?a, ?st),
	executes(?b, ?st),
	 -> next_sibling(?a, ?b)
 """,
# (s5)
"assign_next_sibling-e": """
	act_end(?a), exec_time(?a, ?ia), add(?_ib, ?ia, 1),
	act_end(?b), exec_time(?b, ?ib),
	equal(?_ib, ?ib), 
	# DifferentFrom(?a, ?b),
	executes(?a, ?st),
	executes(?b, ?st),
	 -> next_sibling(?a, ?b)
 """,


"- BeforeActTransitive": """
	before(?a, ?b), before(?b, ?c), -> before(?a, ?c)
	""",
# "- - correct_BeforeActTransitive": """
# 	correct_before(?a, ?b), correct_before(?b, ?c) -> correct_before(?a, ?c)
# 	""",
	# act(?a),
	# act(?b),
	# act(?c),
	
# ???
# "parent_of_to_contains_child": """
# 	parent_of(?a, ?b) -> contains_child(?a, ?b)
#  """ ,

"- parent_of_to_contains_act": """
	parent_of(?a, ?b), act(?a), act(?b) -> contains_act(?a, ?b)
 """ ,

"- contains_actTransitive": """
	contains_act(?a, ?b), contains_act(?b, ?c) -> contains_act(?a, ?c)
	""",


# entry_point       program executes        first act executes
# 
# global_code       global_code.body        global_code.body.first
# 
# func_a            func_a.body             func_a.body.first

# "- DepthOfProgramIs0": """
# 	algorithm(?a), entry_point(?a, ?e), 
# 	executes(?p, ?e), correct_act(p),
# 	 -> depth(?p, 0)
# 	""",

# (s6)
"DepthIncr": """
	act_begin(?a), next(?a, ?b), act_begin(?b), 
	# depth(?a, ?da), add(?db, ?da, 1)
	 -> parent_of(?a, ?b)  # depth(?b, ?db),
	""",
# "- DepthIncr_correct": """
# 	act_begin(?a), correct_next(?a, ?b), act_begin(?b), 
# 	depth(?a, ?da), add(?db, ?da, 1)
# 	 -> depth(?b, ?db), parent_of(?a, ?b)
# 	""",

# (s7)
"DepthSame_b-e": """
	act_begin(?a), next(?a, ?b), act_end(?b), 
	parent_of(?p, ?a),  # depth(?a, ?da), 
	 -> parent_of(?p, ?b), corresponding_end(?a, ?b)
	 # depth(?b, ?da)
	""",
# "- DepthSame_b-e_correct": """
# 	act_begin(?a), correct_next(?a, ?b), act_end(?b), 
# 	depth(?a, ?da), parent_of(?p, ?a)
# 	 -> depth(?b, ?da), parent_of(?p, ?b), corresponding_end(?a, ?b)
# 	""",
	
# (s8)
 # проверка на Начало А - Конец Б (должен был быть Конец А) - CorrespondingActsMismatch_Error
"DepthSame_e-b": """
	act_end(?a), next(?a, ?b), act_begin(?b), 
	parent_of(?p, ?a)  # depth(?a, ?da),
	 -> parent_of(?p, ?b)  # depth(?b, ?da), 
	""",
# "- DepthSame_e-b_correct": """
# 	act_end(?a), correct_next(?a, ?b), act_begin(?b), 
# 	parent_of(?p, ?a)  # depth(?a, ?da),
# 	 -> depth(?b, ?da), parent_of(?p, ?b)
# 	 -> parent_of(?p, ?b)  # depth(?b, ?da), 
# 	""",

# (s9)
"DepthDecr": """
	act_end(?a), next(?a, ?b), act_end(?b), 
	# depth(?a, ?da), subtract(?db, ?da, 1), 
	parent_of(?p, ?a)
	 -> corresponding_end(?p, ?b)  # depth(?b, ?db),
	""",
# "- DepthDecr_correct": """
# 	act_end(?a), correct_next(?a, ?b), act_end(?b), 
# 	depth(?a, ?da), subtract(?db, ?da, 1), 
# 	parent_of(?p, ?a)
# 	 -> depth(?b, ?db), corresponding_end(?p, ?b)
# 	""",

# (s10)
"SameParentOfCorrActs": """
	corresponding_end(?a, ?b), parent_of(?p, ?a)
	 -> parent_of(?p, ?b)
	""",


				######################
				######################
################ Производящие правила ################
				######################
				######################
"-# DBG_connect_FunctionBegin": """
	current_act(?a),
	act_begin(?a),
	func(?func_), 
	executes(?a, ?func_),
	body(?func_, ?st),
	
	next(?a, ?b),
	act_begin(?b),
	executes(?b, ?st),
	
	 -> DebugObj(?a), DebugObj(?b)
""",

# OK (g1) !
"connect_FunctionBegin": """
	current_act(?a),
	act_begin(?a),
	func(?func_), 
	executes(?a, ?func_),
	body(?func_, ?st),
	
	next(?a, ?b),
	act_begin(?b),
	executes(?b, ?st),
	# SameAs(?st, ?_st), # stardog fails with error here
	
	# check that previous execution of st was in correct sub-trace
	next_sibling(?pr, ?b), correct_act(?pr),
	 -> correct_act(?b), current_act(?b), FunctionBegin(?b)
""",

# (g2) - Infers nothing in Stardog
"--- connect_SequenceBegin": """
	current_act(?a),
	act_begin(?a),
	sequence(?block), 
	executes(?a, ?block),
	body_item(?block, ?st),
	first_item(?st),
	
	next(?a, ?b),
	act_begin(?b),
	executes(?b, ?st),
	
	next_sibling(?pr, ?b), correct_act(?pr),
	 -> correct_act(?b), current_act(?b), SequenceBegin(?b)
""",

"--- connect_SequenceNext": """
	current_act(?a),
	act_end(?a),
	parent_of(?p, ?a),
	sequence(?block), 
	executes(?p, ?block),
	body_item(?block, ?st),
	executes(?a, ?st),
	
	next(?a, ?b),
	next(?st, ?st2),
	
	act_begin(?b),
	executes(?b, ?st2),
	
	next_sibling(?pr, ?b), correct_act(?pr),
	 -> correct_act(?b), current_act(?b), SequenceNext(?b)
""",

"--- connect_StmtEnd": """
	current_act(?a),
	act_begin(?a),
	stmt(?st), 
	executes(?a, ?st),
	
	act_end(?b),
	next(?a, ?b),
	executes(?b, ?st),
	
	exec_time(?a, ?t), exec_time(?b, ?_t),
	equal(?t, ?_t),
	 -> current_act(?b), StmtEnd(?b)
""",

"- ??! connect_SequenceEnd": """
	current_act(?a),
	act_end(?a),
	executes(?a, ?st),
	last_item(?st),
	
	next(?a, ?b),
	act_end(?b),
	
	parent_of(?p, ?a),
	executes(?p, ?block),
	sequence(?block), 
	executes(?b, ?block),
	body_item(?block, ?st),
	
	next_sibling(?pr, ?b), correct_act(?pr),
	 -> correct_act(?b), current_act(?b), SequenceEnd(?b)
""",



				###################
				###################
################ Смысловые правила ################
				###################
				###################


"--- CorrespondingActsMismatch_Error": """
	corresponding_end(?a, ?b), 
	executes(?a, ?s1),
	executes(?b, ?s2),
	DifferentFrom(?s1, ?s2),
	 -> CorrespondingEndMismatched(?b), cause(?b, ?a)
""",

"--- CorrespondingActsHaveDifferentExecTime_Error": """
	corresponding_end(?a, ?b), 
	executes(?a, ?s1),
	executes(?b, ?s2),
	SameAs(?s1, ?s2),
	exec_time(?a, ?n1),
	exec_time(?b, ?n2),
	notEqual(?n1, ?n2),
	 -> CorrespondingEndPerformedDifferentTime(?b), cause(?b, ?a)
""",
"- EndAfterTraceEnd_Error": """
	act_end(?a),
	parent_of(?p, ?a), index(?p, 0),  # top-level act representing trace only has index of 0.
	next(?a, ?b), ## act(?b), 
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
	 -> DuplicateActInSequence(?b), cause(?b, ?a)
""",


"- GenericMisplaced_Mistake": """
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

"- Init_Count_std_and_corr_acts": """
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
"- Count_std_acts": """
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
"- Count_corr_acts": """
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
