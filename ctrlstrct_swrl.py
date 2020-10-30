# ctrlstrct.swrl

import re

__COMMENT_RE = re.compile(r"(?://|#).*$")
RULES = []



def strip_comments_out(text):
	# strip all the comments out ...
	# ... replacing them by spaces 
	# in order to preserve char positions reported by lexing parser
	lines = [
				__COMMENT_RE.sub(lambda m: " "*len(m.group(0)), line)
				for line in text.split("\n")
			]
	return "\n".join(lines)


class DomainRule:
	def __init__(self, swrl, name="", tags={}):
		self.name = str(name)
		self.swrl = strip_comments_out(swrl)
		self.tags = tags
	
	def valid_for_tags(self, tags={}):
		return self.tags in tags
	
	def __str__(self):
		return self.swrl
	
	
def filtered_rules(tags):
	# print(tags)
	# print("RULES:", len(RULES))
	filtered = [r for r in RULES if r.tags <= tags]
	# print("filtered:", len(filtered))
	return filtered


# помечаем минусом в начале имени отключенные правила.
# из текста удаляются комментарии в стиле Си (//) и Python (#).


				###################
				###################
################ Служебные правила ################
				###################
				###################



# entry_point       program executes        first act executes
# 
# global_code       global_code.body        global_code.body.first
# 
# func_a            func_a.body             func_a.body.first


# RULES.append(DomainRule(name=, tags={}, swrl=))
# if not dr.name.startswith("-"): RULES.append(dr)
	
RULES.append(DomainRule(name="Incr_index", 
	tags={'correct', 'helper'}, 
	swrl="""
	next_act(?a, ?b), index(?a, ?ia), add(?ib, ?ia, 1)
	 -> index(?b, ?ib)"""))
RULES.append(DomainRule(name="-hardcoded- student_Incr_index", 
	tags={'mistake', 'helper'}, 
	swrl="""
	student_next(?a, ?b), student_index(?a, ?ia), add(?ib, ?ia, 1)
	 -> student_index(?b, ?ib)"""))

# (s6)
RULES.append(DomainRule(name="DepthIncr_rule_s6", 
	tags={'correct', 'helper'}, 
	swrl="""
	act_begin(?a), next_act(?a, ?b), act_begin(?b)
	 -> parent_of(?a, ?b)
	"""))
RULES.append(DomainRule(name="student_DepthIncr_rule_s6", 
	tags={'mistake', 'helper'},
	swrl="""
	act_begin(?a), student_next(?a, ?b), act_begin(?b)
	 -> student_parent_of(?a, ?b)
	"""))

# (s7)
RULES.append(DomainRule(name="DepthSame_b-e_rule_s7", 
	tags={'correct', 'helper'},
	swrl="""
	act_begin(?a), next_act(?a, ?b), act_end(?b), 
	parent_of(?p, ?a),
	 -> parent_of(?p, ?b), corresponding_end(?a, ?b)
	"""))
RULES.append(DomainRule(name="student_DepthSame_b-e_rule_s7", 
	tags={'mistake', 'helper'},
	swrl="""
	act_begin(?a), student_next(?a, ?b), act_end(?b), 
	student_parent_of(?p, ?a),
	 -> student_parent_of(?p, ?b), student_corresponding_end(?a, ?b)
	"""))
	
# (s8)
 # проверка на Начало А - Конец Б (должен был быть Конец А) - CorrespondingActsMismatch_Error
RULES.append(DomainRule(name="DepthSame_e-b_rule_s8", 
	tags={'correct', 'helper'},
	swrl="""
	act_end(?a), next_act(?a, ?b), act_begin(?b), 
	parent_of(?p, ?a)  # depth(?a, ?da),
	 -> parent_of(?p, ?b)  # depth(?b, ?da), 
	"""))
RULES.append(DomainRule(name="student_DepthSame_e-b_rule_s8", 
	tags={'mistake', 'helper'},
	swrl="""
	act_end(?a), student_next(?a, ?b), act_begin(?b), 
	student_parent_of(?p, ?a)
	 -> student_parent_of(?p, ?b)
	"""))

# (s9)
RULES.append(DomainRule(name="DepthDecr_rule_s9", 
	tags={'correct', 'helper'},
	swrl="""
	act_end(?a), next_act(?a, ?b), act_end(?b), 
	parent_of(?p, ?a)
	 -> corresponding_end(?p, ?b)
	"""))
RULES.append(DomainRule(name="student_DepthDecr_rule_s9", 
	tags={'mistake', 'helper'},
	swrl="""
	act_end(?a), student_next(?a, ?b), act_end(?b), 
	student_parent_of(?p, ?a)
	 -> student_corresponding_end(?p, ?b)
	"""))

# (s10)
RULES.append(DomainRule(name="SameParentOfCorrActs_rule_s10", 
	tags={'correct', 'helper'},
	swrl="""
	corresponding_end(?a, ?b), parent_of(?p, ?a)
	 -> parent_of(?p, ?b)
	"""))
RULES.append(DomainRule(name="student_SameParentOfCorrActs_rule_s10", 
	tags={'mistake', 'helper'},
	swrl="""
	corresponding_end(?a, ?b), student_parent_of(?p, ?a)
	 -> student_parent_of(?p, ?b)
	"""))


# Disambiguating siblings (1): init on previous correct sibling
RULES.append(DomainRule(name="Earliest_after_act_is_previous_correct_sibling", 
	tags={'correct', 'helper'},
	swrl="""
	correct_act(?a),
	next_sibling(?a, ?s),
	 -> after_act(?s, ?a)
"""))
# Disambiguating siblings (2): propagate till itself
RULES.append(DomainRule(name="Propagate_after_act", 
	tags={'correct', 'helper'},
	swrl="""
	after_act(?s, ?a),
	next_act(?a, ?b),
	# DifferentFrom(?b, ?s),
		id(?b, ?ib),
		id(?s, ?is),
		notEqual(?ib, ?is),
	 -> after_act(?s, ?b)
"""))



				######################
				######################
################ Производящие правила ################
				######################
				######################

# Точка входа в трассу - функция  [works with Pellet] [works with Stardog]
RULES.append(DomainRule(name="start__to__MainFunctionBegin__rule_g3", 
	tags={'correct', 'entry', 'function'},
	swrl="""
	trace(?a),
	executes(?a, ?alg),
	entry_point(?alg, ?func_),
	func(?func_), 
	# DifferentFrom(?a, ?b),  # здесь не нужно, но правило от этого ломается (хотя и не ломает остальной вывод)!
	act_begin(?b),
		# next_sibling(?pr, ?b), correct_act(?pr),
	next_sibling(?a, ?b),  # ?pr === ?a
	executes(?b, ?func_),

	 -> normal_flow_correct_act(?b), 
	 next_act(?a, ?b), 
	 FunctionBegin(?b)
"""))

# Точка входа в трассу - глобальный код  [works with Pellet]
RULES.append(DomainRule(name="start__to__GlobalCode__rule_g4", 
	tags={'correct', 'entry', 'sequence'},
	swrl="""
	trace(?a),
	executes(?a, ?alg),
	entry_point(?alg, ?gc),
	sequence(?gc), 

	act_begin(?b),
		# next_sibling(?pr, ?b), correct_act(?pr),
	next_sibling(?a, ?b),  # ?pr === ?a
	executes(?b, ?gc),

	 -> normal_flow_correct_act(?b), 
	 next_act(?a, ?b), GlobalCodeBegin(?b)
"""))


# OK !
# Начало тела функции  [works with Pellet] [works with Stardog]
RULES.append(DomainRule(name="connect_FunctionBodyBegin_rule_g5", 
	tags={'correct', 'function'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	func(?func_), 
	executes(?a, ?func_),
	body(?func_, ?st),
	
	act_begin(?b),
	executes(?b, ?st),
	# SameAs(?st, ?_st), # stardog fails with error here
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), 
	 next_act(?a, ?b), 
	 FunctionBodyBegin(?b)
"""))
# Конец тела функции
RULES.append(DomainRule(name="connect_FuncBodyEnd_rule_g5-2", 
	tags={'correct', 'function'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	func(?func_), 
	body(?func_, ?st),
	executes(?a, ?st),
	
	act_end(?b),
	executes(?b, ?func_),
	
	after_act(?b, ?a),
	
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), FunctionEnd(?b)
"""))

# Первый акт следования [works with Pellet] [FAILS with Stardog...]
# Пустые следования (без действий) не поддерживаются!
RULES.append(DomainRule(name="connect_SequenceBegin_rule_g2", 
	tags={'correct', 'sequence'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	sequence(?block), 
	executes(?a, ?block),
	body_item(?block, ?st),
	first_item(?st),
	
	act_begin(?b),
	executes(?b, ?st),
	
	after_act(?b, ?a),
	
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), SequenceBegin(?b)
"""))

# Следующий акт следования [works with Pellet]
RULES.append(DomainRule(name="connect_SequenceNext", 
	tags={'correct', 'sequence'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	parent_of(?p, ?a),
	sequence(?block), 
	executes(?p, ?block),
	body_item(?block, ?st),
	executes(?a, ?st),
	
	next(?st, ?st2),
	
	act_begin(?b),
	executes(?b, ?st2),
	
	after_act(?b, ?a),	
	
	 -> normal_flow_correct_act(?b), 
	  next_act(?a, ?b), 
	  SequenceNext(?b)
"""))

# Начало и конец простого акта [works with Pellet]
RULES.append(DomainRule(name="connect_StmtEnd", 
	tags={'correct', 'sequence'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	stmt(?st), 
	executes(?a, ?st),
	
	act_end(?b),
	executes(?b, ?st),
	
	after_act(?b, ?a),
	
	exec_time(?a, ?t), exec_time(?b, ?_t),
	equal(?t, ?_t),
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), StmtEnd(?b)
"""))

# Начало и конец акта выражения [works with Pellet]
RULES.append(DomainRule(name="connect_ExprEnd", 
	tags={'correct', 'sequence'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	expr(?st), 
	executes(?a, ?st),
	
	act_end(?b),
	executes(?b, ?st),
	
	after_act(?b, ?a),

	exec_time(?a, ?t), exec_time(?b, ?_t),
	equal(?t, ?_t),
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), ExprEnd(?b)
"""))

#  [works with Pellet]
RULES.append(DomainRule(name="connect_SequenceEnd", 
	tags={'correct', 'sequence'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	executes(?a, ?st),
	last_item(?st),
	
	act_end(?b),
	parent_of(?p, ?a),
	executes(?p, ?block),
#	sequence(?block),    # ???
	executes(?b, ?block),
	body_item(?block, ?st),
	
	after_act(?b, ?a),
	
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), SequenceEnd(?b)
"""))


# ===== Alt ===== #


# Проверка первого условия развилки (if) [works with Pellet]
RULES.append(DomainRule(name="connect_AltBegin", 
	tags={'correct', 'alternative'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	alternative(?alt), 
	executes(?a, ?alt),

	branches_item(?alt, ?br),
	first_item(?br),	# one of that lines is enough
	# if(?br),			# one of that lines is enough
	cond(?br, ?cnd),
	
	act_begin(?b),
	executes(?b, ?cnd),  # expr
	
	after_act(?b, ?a),

	# exec_time(?a, ?t), exec_time(?b, ?_t),
	# equal(?t, ?_t),
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), AltBegin(?b)
"""))

# Начало ветки истинного условия развилки [works with Pellet]
RULES.append(DomainRule(name="connect_AltBranchBegin_CondTrue", 
	tags={'correct', 'alternative'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, true),  # condition passed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative
	
	act_begin(?b),
	executes(?b, ?br),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), AltBranchBegin(?b)
"""))

# Проверка следующего условия развилки (else-if) [works with Pellet]
RULES.append(DomainRule(name="connect_NextAltCondition", 
	tags={'correct', 'alternative'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative

	next(?br, ?br2),
	cond(?br2, ?cnd2),
	
	act_begin(?b),
	executes(?b, ?cnd2),  # expr
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), NextAltCondition(?b)
"""))

# Переход к ветке ИНАЧЕ (else)  [works with Pellet]
RULES.append(DomainRule(name="connect_AltElseBranch", 
	tags={'correct', 'alternative'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative
	next(?br, ?br2),
	else(?br2),
	
	act_begin(?b),
	executes(?b, ?br2),  # expr

	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), AltElseBranchBegin(?b)
"""))

# Конец развилки, т.к. все условия ложны [works with Pellet]
RULES.append(DomainRule(name="connect_AltEndAllFalse", 
	tags={'correct', 'alternative'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed

	cond(?br, ?cnd),
	alt_branch(?br),  # belonds to an alternative
	branches_item(?alt, ?br),
	last_item(?br),   # the branch is last in alternative
	alternative(?alt),
	
	act_end(?b),
	executes(?b, ?alt),  # expr

	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), AltEndAllFalse(?b)
"""))

# Окончание развилки по завершению ветки [works with Pellet]
RULES.append(DomainRule(name="connect_AltEndAfterBranch", 
	tags={'correct', 'alternative'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	executes(?a, ?br),
	branches_item(?alt, ?br),
	alternative(?alt), 

	act_end(?b),
	executes(?b, ?alt),  # ends whole alternative
	
	after_act(?b, ?a),
	
	 -> normal_flow_correct_act(?b), next_act(?a, ?b), AltEndAfterBranch(?b)
"""))

# (6 generating rules to construct alternatives)


# ===== Loops ===== #


# Начало цикла с предусловием (while) [works with Pellet]
RULES.append(DomainRule(name="connect_LoopBegin-cond", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	pre_conditional_loop(?loop), 
	executes(?a, ?loop),

	cond(?loop, ?cnd),
	
	act_begin(?b),
	executes(?b, ?cnd),  # expr
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), PreCondLoopBegin(?b)
"""))

# Начало цикла с постусловием (do-while, do-until) [works]
RULES.append(DomainRule(name="connect_LoopBegin-body", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	post_conditional_loop(?loop), 
	executes(?a, ?loop),

	body(?loop, ?st),
	
	act_begin(?b),
	executes(?b, ?st),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), PostCondLoopBegin(?b)
"""))

# Начало тела цикла при cond=1 (while, do-while, for) [works since simplified cond_then_body class declaration]
RULES.append(DomainRule(name="connect_LoopCond1-BodyBegin", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	cond_then_body(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, true),  # condition passed
	
	body(?loop, ?st),
	# body_item(?loop, ?st),
	# first_item(?st),
	
	act_begin(?b),
	executes(?b, ?st),
								# iteration belongs to ????
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), IterationBeginOnTrueCond(?b)
"""))

# Начало тела цикла при cond=0 (do-until) [works]
RULES.append(DomainRule(name="connect_LoopCond0-body", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	inverse_conditional_loop(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition passed
	
	body(?loop, ?st),
	# body_item(?loop, ?st),
	# first_item(?st),
	
	act_begin(?b),
	executes(?b, ?st),
								# iteration belongs to ????
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), IterationBeginOnFalseCond(?b)
"""))

# Начало тела цикла при cond=1 (foreach) [works]
RULES.append(DomainRule(name="connect_LoopCond1-update", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	pre_update_loop(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, true),  # condition passed
	
	update(?loop, ?upd),
	act_begin(?b),
	executes(?b, ?upd),
								# iteration belongs to ????
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), LoopUpdateOnTrueCond(?b)
"""))

# После перехода цикла - условие (foreach) [works]
RULES.append(DomainRule(name="connect_LoopUpdate-body", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	pre_update_loop(?loop), 
	update(?loop, ?upd),
	executes(?a, ?upd),

	body(?loop, ?st),
	act_begin(?b),
	executes(?b, ?st),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b),
	 LoopBodyAfterUpdate(?b)
"""))

# Конец цикла при cond=0 (while, do-while, for, foreach) [works]
RULES.append(DomainRule(name="connect_LoopCond0-LoopEnd", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	conditional_loop(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition passed
	
	act_end(?b),
	executes(?b, ?loop),
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), NormalLoopEnd(?b)
"""))

# Конец цикла при cond=1 (do-until) [works]
RULES.append(DomainRule(name="connect_LoopCond1-LoopEnd", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	inverse_conditional_loop(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, true),  # condition failed
	
	act_end(?b),
	executes(?b, ?loop),
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), NormalLoopEnd(?b)
"""))

# После тела цикла - условие (while, do-while, do-until, foreach) [works]
RULES.append(DomainRule(name="connect_LoopBody-cond", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	body_then_cond(?loop), 
	body(?loop, ?st),
	executes(?a, ?st),

	cond(?loop, ?cnd),
	act_begin(?b),
	executes(?b, ?cnd),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b),
	 LoopCondBeginAfterIteration(?b)
"""))


# Начало цикла с инициализацией (for, foreach) [works]
RULES.append(DomainRule(name="connect_LoopBegin-init", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_begin(?a),
	executes(?a, ?loop),
	loop_with_initialization(?loop), 

	init(?loop, ?st),
	
	act_begin(?b),
	executes(?b, ?st),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b), LoopWithInitBegin(?b)
"""))

# После инициализации цикла - условие (for, foreach) [works]
RULES.append(DomainRule(name="connect_LoopInit-cond", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	loop_with_initialization(?loop), 
	init(?loop, ?st),
	executes(?a, ?st),

	cond(?loop, ?cnd),
	act_begin(?b),
	executes(?b, ?cnd),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b),
	 LoopCondBeginAfterInit(?b)
"""))

# После тела цикла - переход (update) (for) [works]
RULES.append(DomainRule(name="connect_LoopBody-update", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	post_update_loop(?loop), 
	body(?loop, ?st),
	executes(?a, ?st),

	update(?loop, ?upd),
	act_begin(?b),
	executes(?b, ?upd),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b),
	 LoopUpdateAfterIteration(?b)
"""))

# После перехода цикла - условие (for) [works]
RULES.append(DomainRule(name="connect_LoopUpdate-cond", 
	tags={'correct', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	post_update_loop(?loop), 
	update(?loop, ?st),
	executes(?a, ?st),

	cond(?loop, ?cnd),
	act_begin(?b),
	executes(?b, ?cnd),
	
	after_act(?b, ?a),

	 -> normal_flow_correct_act(?b), next_act(?a, ?b),
	 LoopCondAfterUpdate(?b)
"""))




		 # dont forget to add suffix '_rule_#' if continue testing the rules.


				###################
				###################
################ Правила на ошибки ################
				###################
				###################


RULES.append(DomainRule(name="CorrespondingActsMismatch_Error", 
	tags={'mistake'},
	swrl="""
	student_corresponding_end(?a, ?b), 
	executes(?a, ?s1),
	executes(?b, ?s2),
	# DifferentFrom(?s1, ?s2),
		id(?s1, ?ib),
		id(?s2, ?ic),
		notEqual(?ib, ?ic),
	 -> CorrespondingEndMismatched(?b), cause(?b, ?a)
"""))

RULES.append(DomainRule(name="-ErrOff- CorrespondingActsHaveDifferentExecTime_Error", 
	tags={'mistake'},
	swrl="""
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
"""))


RULES.append(DomainRule(name="GenericWrongAct_Error", 
	tags={'mistake'},
	swrl="""
	next_act(?a, ?b),
	student_next(?a, ?c),
	# DifferentFrom(?b, ?c),
		id(?b, ?ib),
		id(?c, ?ic),
		notEqual(?ib, ?ic),
	 -> should_be(?c, ?b), 
	 precursor(?c, ?a), 
	 Erroneous(?c)
"""))

RULES.append(DomainRule(name="GenericWrongParent_Error", 
	tags={'mistake'},
	swrl="""
	parent_of(?p, ?a),
	student_parent_of(?c, ?a),
	# DifferentFrom(?p, ?c),
		id(?p, ?ip),
		id(?c, ?ic),
		notEqual(?ip, ?ic),
	 -> context_should_be(?a, ?p), 
	 # cause(?a, ?c), 
	 WrongContext(?a)
"""))

RULES.append(DomainRule(name="GenericWrongExecTime-b_Error", 
	tags={'mistake'},
	swrl="""
	Erroneous(?c),
	should_be(?c, ?b),
	act_begin(?b),
	act_begin(?c),
	executes(?c, ?st),
	executes(?b, ?st),
	exec_time(?c, ?n1),
	exec_time(?b, ?n2),
	notEqual(?n1, ?n2),
	 -> WrongExecTime(?c)
"""))

RULES.append(DomainRule(name="GenericWrongExecTime-e_Error", 
	tags={'mistake'},
	swrl="""
	Erroneous(?c),
	should_be(?c, ?b),
	act_end(?b),
	act_end(?c),
	executes(?c, ?st),
	executes(?b, ?st),
	exec_time(?c, ?n1),
	exec_time(?b, ?n2),
	notEqual(?n1, ?n2),
	 -> WrongExecTime(?c)
"""))


RULES.append(DomainRule(name="ActStartsAfterItsEnd_Error", 
	tags={'mistake'},
	swrl="""
	act_begin(?a),
	act_end(?b),
	executes(?a, ?st),
	executes(?b, ?st),
	exec_time(?a, ?n),
	exec_time(?b, ?n),
	student_index(?a, ?ia),
	student_index(?b, ?ib),
	lessThan(?ib, ?ia),  # b < a
	 -> cause(?a, ?b), cause(?b, ?a), 
	  ActStartsAfterItsEnd(?a),
	  ActEndsWithoutStart(?b)
"""))



# ============ Sequence mistakes ============ #

# Дубликат акта в следовании [works with Pellet]
# Базируется на ExtraAct
RULES.append(DomainRule(name="DuplicateOfAct-seq-b_Error", 
	tags={'mistake', 'sequence'},
	swrl="""
	ExtraAct(?c1), 
	act_begin(?c1),
	student_parent_of(?p, ?c1),
	executes(?p, ?block),
	sequence(?block),
		body_item(?block, ?st),  # // just to ensure the sequence is real (and thus has "body_item"s)
	executes(?c1, ?st),

	executes(?c, ?st),
	parent_of(?p, ?c),
	act_begin(?c),

		id(?c1, ?ic1),
		id(?c, ?ic),
		notEqual(?ic1, ?ic),
	 -> cause(?c1, ?c), 
	 DuplicateOfAct(?c1)
"""))
# Дубликат акта в следовании [works with Pellet]
# Базируется на ExtraAct
RULES.append(DomainRule(name="DuplicateOfAct-seq-e_Error", 
	tags={'mistake', 'sequence'},
	swrl="""
	ExtraAct(?c1), 
	act_end(?c1),
	student_parent_of(?p, ?c1),
	executes(?p, ?block),
	sequence(?block),
		body_item(?block, ?st),  # // just to ensure the sequence is real (and thus has "body_item"s)
	executes(?c1, ?st),

	executes(?c, ?st),
	parent_of(?p, ?c),
	act_end(?c),

		id(?c1, ?ic1),
		id(?c, ?ic),
		notEqual(?ic1, ?ic),
	 -> cause(?c1, ?c), 
	 DuplicateOfAct(?c1)
"""))

# Перемещённый акт [works with Pellet]
# Базируется одновременно на ExtraAct и MissingAct
RULES.append(DomainRule(name="DisplacedAct_Error", 
	tags={'mistake', 'sequence'},
	swrl="""
	ExtraAct(?c1), 
	MissingAct(?c1), 
	 -> DisplacedAct(?c1)
"""))

# # Перемещённый акт [works with Pellet]
# # Базируется одновременно на ExtraAct и MissingAct
# RULES.append(DomainRule(name="DisplacedAct_Error", 
# 	tags={'mistake', 'sequence'},
# 	swrl="""
# 	ExtraAct(?c1), 
# 	MissingAct(?c1), 
# 	 -> DisplacedAct(?c1)
# """))

# ============ Alternatives mistakes ============ #

# Развилка не начинается с условия [works with Pellet]
RULES.append(DomainRule(name="NoFirstCondition-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_begin(?a),
	executes(?a, ?alt),
	alternative(?alt), 

	student_next(?a, ?b),
	Erroneous(?b), 
	 -> NoFirstCondition(?b)
"""))

# Ветка при ложном условии [works with Pellet]
RULES.append(DomainRule(name="BranchOfFalseCondition-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed

	cond(?br, ?cnd),  # corresponding branch
	alt_branch(?br),  # belonds to an alternative
	
	act_begin(?b),
	executes(?b, ?br),
	
	student_parent_of(?alt_act, ?a),
	student_parent_of(?alt_act, ?b),
	
	# student_next(?a, ?b),
	Erroneous(?b), 	  # как страховка, сработает и без этого
	 -> cause(?b, ?a),
	 BranchOfFalseCondition(?b)
"""))

# Условие после ветки  [works with Pellet]
RULES.append(DomainRule(name="ConditionAfterBranch-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
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
"""))

# Вторая ветка в альтернативе [works with Pellet]
RULES.append(DomainRule(name="AnotherExtraBranch-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_end(?a),
	executes(?a, ?br),
	branches_item(?alt, ?br),
	alternative(?alt), 

	act_begin(?b),
	executes(?b, ?br2),
	branches_item(?alt, ?br2),
	
	student_parent_of(?alt_act, ?a),
	student_parent_of(?alt_act, ?b),
	
	student_index(?a, ?sia),
	student_index(?b, ?sib),
	greaterThan(?sib, ?sia),
	 -> AnotherExtraBranch(?b)
"""))

# После истинного условия нет его ветки [works with Pellet]
RULES.append(DomainRule(name="NoBranchWhenConditionIsTrue-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, true),  # condition passed

	cond(?br, ?cnd),  # corresponding branch
	alt_branch(?br),  # belonds to an alternative

	student_next(?a, ?b),
	Erroneous(?b), 	  # как страховка, сработает и без этого
	
	 -> NoBranchWhenConditionIsTrue(?b)
"""))

RULES.append(DomainRule(name="AllFalseNoElse-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed
	cond(?br, ?cnd),  # corresponding branch
	next(?br, ?br2),
	else(?br2), 	  # "else" branch expected

	student_next(?a, ?b),
	Erroneous(?b),
	
	 -> AllFalseNoElse(?b)
"""))

RULES.append(DomainRule(name="NoNextCondition-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed
	cond(?br, ?cnd),  # corresponding branch
	next(?br, ?br2),
	cond(?br2, ?cnd2), 	  # one more condition expected

	student_next(?a, ?b),
	Erroneous(?b),
	
	 -> NoNextCondition(?b)
"""))

RULES.append(DomainRule(name="AllFalseNoEnd-alt_Error", 
	tags={'mistake', 'alternative'},
	swrl="""
	act_end(?a),
	expr(?cnd), 
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed
	cond(?br, ?cnd),  # corresponding branch
	last_item(?br),   # no more conditions expected

	student_next(?a, ?b),
	Erroneous(?b),
	
	 -> AllFalseNoEnd(?b)
"""))


# ============ Loops mistakes ============ #

# Нет итерации после успешного условия при cond=1 (while, do-while, for) [works]
RULES.append(DomainRule(name="MissingIterationAfterSuccessfulCondition-1-loop_Error", 
	tags={'mistake', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	cond_then_body(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, true),  # condition passed

	student_next(?a, ?b),
	Erroneous(?b), 
	 -> MissingIterationAfterSuccessfulCondition(?b)
"""))

# Нет итерации после успешного условия при cond=0 (do-until) [works?]
RULES.append(DomainRule(name="MissingIterationAfterSuccessfulCondition-0-loop_Error", 
	tags={'mistake', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	inverse_conditional_loop(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition passed

	student_next(?a, ?b),
	Erroneous(?b), 
	 -> MissingIterationAfterSuccessfulCondition(?b)
"""))

# Нет конца цикла после неуспешного условия - при cond=0 (while, do-while, for, ?) [works?]
RULES.append(DomainRule(name="MissingLoopEndAfterFailedCondition-0-loop_Error", 
	tags={'mistake', 'loop'},
	swrl="""
	normal_flow_correct_act(?a),
	act_end(?a),
	cond_then_body(?loop), 
	cond(?loop, ?cnd),
	executes(?a, ?cnd),

	expr_value(?a, false),  # condition failed

	student_next(?a, ?b),
	Erroneous(?b), 
	 -> MissingLoopEndAfterFailedCondition(?b)
"""))



_more_rules = {}

# Поиск лишних и пропущенных актов (ограниченная дальность просмотра)
for i in range(1, 12+1):

	pattern1 = ''.join([f"student_next(?c{j}, ?c{j+1}), " for j in range(1,i)])
	pattern2 = f"student_next(?c{i}, ?b),"
	action = ', '.join([f"ExtraAct(?c{j})" for j in range(1,i+1)])
	RULES.append(DomainRule(name=f"ExtraAct_{i}_Error", 
		tags={'mistake'},
		swrl=f"""
		next_act(?a, ?b),
		student_next(?a, ?c1),
		# DifferentFrom(?b, ?c1),
		{pattern1}
		{pattern2}
		 -> {action} ## ExtraAct(?c1)
	"""))

	pattern1 = ''.join([f"next_act(?c{j}, ?c{j+1}), "
						for j in range(1,i)])
	pattern2 = f"next_act(?c{i}, ?b),"
	action = ',  '.join([f"MissingAct(?c{j}), should_be_before(?c{j}, ?b)"
						for j in range(1,i+1)])
	RULES.append(DomainRule(name=f"MissingAct_{i}_Error", 
		tags={'mistake'},
		swrl=f"""
		student_next(?a, ?b),
		next_act(?a, ?c1),
		# DifferentFrom(?b, ?c1),
		{pattern1}
		{pattern2}
		 -> {action}, ## MissingAct(?c1)]
		 TooEarly(?b)
	"""))


# Расчёт номеров итераций для всех циклов
for i in range(0, 3+1):

	pattern1 = ''.join([f"""
		executes(?c{j}, ?st{j}),
		id(?st{j}, ?st{j}_i),
		notEqual(?st{j}_i, ?body_i),
		corresponding_end(?c{j}, ?ce{j}), 
		next_act(?ce{j}, ?c{j+1}), 
		""" 
		for j in range(i)])
	pattern2 = f"executes(?c{i}, ?st), corresponding_end(?c{i}, ?ce{i}), "
	action = f"""iteration_n(?c{i}, 1),
		iteration_n(?ce{i}, 1)
		"""
						
	RULES.append(DomainRule(name=f"LoopIteration1_after_{i}", 
		tags={'correct', 'helper', 'loop'},
		swrl=f"""
		act_begin(?a),
		executes(?a, ?L),
		loop(?L),
		body(?L, ?st),
		id(?st, ?body_i),
		next_act(?a, ?c0),
		{pattern1} 
		{pattern2}  # executes(?ci, ?st),
		 -> {action}
	"""))


for i in range(0, 2+1):

	pattern1 = ''.join([f"""
		executes(?c{j}, ?st{j}),
		id(?st{j}, ?st{j}_i),
		notEqual(?st{j}_i, ?body_i),
		corresponding_end(?c{j}, ?ce{j}), 
		next_act(?ce{j}, ?c{j+1}), 
		""" 
		for j in range(i)])
	pattern2 = f"executes(?c{i}, ?st), corresponding_end(?c{i}, ?ce{i}),"
	action = f"""iteration_n(?c{i}, ?n_next),
		iteration_n(?ce{i}, ?n_next)
		"""
						
	RULES.append(DomainRule(name=f"LoopIterationNext_after_{i}", 
		tags={'correct', 'helper', 'loop'},
		swrl=f"""
		act_end(?a),
		iteration_n(?a, ?n),
		executes(?a, ?st),
		id(?st, ?body_i),
		next_act(?a, ?c0),
		{pattern1} 
		{pattern2}  # executes(?ci, ?st),
		add(?n_next, ?n, 1),
		 -> {action}
	"""))




for r in RULES[:]:
	if r.name.startswith("-"):
		# print("skipping SWRL rule due to minus: \t", r)
		RULES.remove(r)

if 1:  # check correctness of modified rules text
	with open("swrl_dbg.txt", "w") as f:
	# 	# f.write(repr(RULES))
		for r in RULES:
			print(f'"{r.name}": ', end="", file=f)
			print(r.swrl, file=f)

# debug! # RULES = {}
