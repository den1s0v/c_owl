#############		 Paste rules to to Protege`s SWRL Tab 			  #############
############# (*.py extension is just used for syntax highlighting :) #############
### Rule format structure: blocks separated by blank line:
### - variables (`?x`, `?my_var`) type declaration.
### - conditions & restrictions; last line is exact rule trigger.
### - strings assignment; last line is concatenation of result message.
### > line starting with `->` is a rule body - saves message as new data property assigned to LOG (global individual).

# `differentFrom` -> `DifferentFrom` in owlready2 !!!


# BeforeActTransitive
c_schema:Act(?b) ^ c_schema:Act(?c) ^ c_schema:Act(?a) ^ c_schema:beforeAct(?a, ?b) ^ c_schema:beforeAct(?b, ?c) -> c_schema:beforeAct(?a, ?c)

# ==================================

# 0
# ActOutOfContextError
# Срабатывает, если есть акт `act`, непосредственно вложенный в акт `act_c` (контекст),
# в то время как их первоисточники в алгоритме (st и st_c) не состоят в таком же отношении вложенности (контекст st - st_c_actual - отличается от st_c, указанного в трассе):
hasDirectPart(?act_c, ?act),
hasOrigin(?act, ?st),
hasOrigin(?act_c, ?st_c),
hasDirectPart(?st_c_actual, ?st),

DifferentFrom(?st_c, ?st_c_actual)
 -> message(ERRORS, "ActOutOfContextError(No detalization yet.)")

# ==================================


# 1
# ActBeforeStartOfBlockError
# Срабатывает, если для блока есть акт `act`, стоящий ДО первого акта следования `act1`:
# act < act1
c_schema:Context(?c)
c_schema:Block(?block)
c_schema:Statement(?stmt1)
c_schema:Act(?act1)
c_schema:Act(?act)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act,  ?c)
c_schema:hasFirst(?block, ?stmt1)
c_schema:hasOrigin(?c, ?block)
c_schema:hasOrigin(?act1, ?stmt1)
c_schema:before(?act, ?act1)

c_schema:hasIndex(?c, ?index)
c_schema:hasOrigin(?act, ?stmt)
c_schema:hasSource(?stmt, ?src)
c_schema:hasLocationSuffix(?stmt, ?stlbl)
swrlb:stringConcat(?msg, "ActBeforeStartOfBlockError: act `", ?src, "` (", ?stlbl, "#", ?index, ") is placed before start of block.")
 -> c_schema:message(c_schema:ERRORS, ?msg)

# 2
# ActAfterEndOfBlockError
# Срабатывает, если для блока есть акт `act`, стоящий ПОСЛЕ последнего акта следования `end`:
# end < act
c_schema:Context(?c)
c_schema:Block(?block)
c_schema:Statement(?stmt_end)
c_schema:Act(?end)
c_schema:Act(?act)

c_schema:hasContext(?end, ?c)
c_schema:hasContext(?act,  ?c)
c_schema:hasLast(?block, ?stmt_end)
c_schema:hasOrigin(?c, ?block)
c_schema:hasOrigin(?end, ?stmt_end)
c_schema:before(?end, ?act)

c_schema:hasIndex(?c, ?index)
c_schema:hasOrigin(?act, ?stmt)
c_schema:hasSource(?stmt, ?src)
c_schema:hasLocationSuffix(?stmt, ?stlbl)
swrlb:stringConcat(?msg, "ActAfterEndOfBlockError: act `", ?src, "` (", ?stlbl, "#", ?index, ") is placed after end of block.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# 3
# Утв-4 : Ош-1
# ActsPairMisorderError
# Срабатывает, если акты `act1` и `act2` для последовательных действий блока `stmt_1` и `stmt_2` стоят в обратном порядке:
# stmt_1 << stmt_2 ,
# act2 < act1
c_schema:Context(?c)
c_schema:Statement(?stmt_1)
c_schema:Statement(?stmt_2)
c_schema:Act(?act1)
c_schema:Act(?act2)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act2, ?c)
c_schema:hasNext(?stmt_1, ?stmt_2)
c_schema:hasOrigin(?act1, ?stmt_1)
c_schema:hasOrigin(?act2, ?stmt_2)
c_schema:before(?act2, ?act1)

c_schema:hasIndex(?c, ?index)
c_schema:hasSource(?stmt_1, ?src1)
c_schema:hasSource(?stmt_2, ?src2)
swrlb:stringConcat(?msg, "ActsPairMisorderError: acts `", ?src2, "` and `", ?src1, "` are placed in reversed order.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# 4
# ActCannotFollowActError
# Срабатывает, если действия `stmt_act1` и `stmt_act2` последовательных актов `act1` и `act2` не последовательны, и вместо `stmt_act2` должно стоять `stmt_2`:
# stmt_act1 << stmt_2 ,
# act1 << act2 ,
# stmt_act2 != stmt_2
c_schema:Context(?c)
c_schema:Statement(?stmt_act1)
c_schema:Statement(?stmt_act2)
c_schema:Act(?act1)
c_schema:Act(?act2)
c_schema:Statement(?stmt_2)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act2, ?c)
c_schema:hasNext(?act1, ?act2)
c_schema:hasNext(?stmt_act1, ?stmt_2)
c_schema:hasOrigin(?act1, ?stmt_act1)
c_schema:hasOrigin(?act2, ?stmt_act2)

differentFrom(?stmt_act2, ?stmt_2)

c_schema:hasSource(?stmt_act1, ?src_a1)
c_schema:hasSource(?stmt_act2, ?src_a2)
c_schema:hasSource(?stmt_2, ?src2)
swrlb:stringConcat(?msg, "ActCannotFollowActError: `", ?src_a1, "` must be followed by `", ?src2, "` , not `", ?src_a2, "`.")
 -> c_schema:message(c_schema:ERRORS, ?msg)


# 5
# ActCannotPrecedeActError
# Срабатывает, если действия `stmt_act1` и `stmt_act2` последовательных актов `act1` и `act2` не последовательны, и вместо `stmt_act1` должно стоять `stmt_1`:
# stmt_1 << stmt_act2 ,
# act1 << act2 ,
# stmt_act1 != stmt_1
c_schema:Context(?c)
c_schema:Statement(?stmt_act1)
c_schema:Statement(?stmt_act2)
c_schema:Act(?act1)
c_schema:Act(?act2)
c_schema:Statement(?stmt_1)

c_schema:hasContext(?act1, ?c)
c_schema:hasContext(?act2, ?c)
c_schema:hasNext(?act1, ?act2)
c_schema:hasNext(?stmt_1, ?stmt_act2)
c_schema:hasOrigin(?act1, ?stmt_act1)
c_schema:hasOrigin(?act2, ?stmt_act2)

differentFrom(?stmt_act1, ?stmt_1)

c_schema:hasSource(?stmt_act1, ?src_a1)
c_schema:hasSource(?stmt_act2, ?src_a2)
c_schema:hasSource(?stmt_1, ?src1)
swrlb:stringConcat(?msg, "ActCannotPrecedeActError: `", ?src_a2, "` must be preceeded by `", ?src1, "` , not `", ?src_a1, "`.")
 -> c_schema:message(c_schema:ERRORS, ?msg)



#		 ====================
#		 ====================
#		 ====================

# Утверждения (Приложение 1) из ТЗ Носкина

# Утв-1 : Ош-3
# Оператор Б (st) входит в следование А (block), при этом между  началом акта А и концом акта А содержится БОЛЬШЕ ОДНОГО (два) акта Б (act1,act2)
# DuplicateActsOfStmtError
Block(?block) ^
hasOrigin(?block_act, ?block) ^

hasOrigin(?act1, ?st) ^
hasOrigin(?act2, ?st) ^
hasDirectPart(?block_act, ?act1) ^
hasDirectPart(?block_act, ?act2) ^

differentFrom(?act1, ?act2)
 -> message(ERRORS, "DuplicateActsOfStmtError")


# Утв-2 : Ош-1
# Акт А существует и начало акта А > конец акта А
# (ДОЛЖНО ПРОВЕРЯТЬСЯ ПРИ ПАРСИНГЕ СИНТАКСИСА...)
# ActStartsAfterEndError
Act(?a)
hasFirstAct(?a, ?begin)
hasLastAct(?a, ?end)
DifferentFrom(?begin, ?end)
before(?end, ?begin)
 -> message(ERRORS, "ActStartsAfterEndError")


# Утв-3 : Синтаксис и "Акт вне своего Контекста"
hasDirectPart(?act_c, ?act),
hasOrigin(?act, ?st),
hasOrigin(?act_c, ?st_c),
hasDirectPart(?st_c_actual, ?st),

DifferentFrom(?st_c, ?st_c_actual)
 -> message(ERRORS, "ActOutOfContextError(No detalization yet.)")

# Утв-5 : Ош-1
# А является альтернативой, Б её условие, В - первая ветка, а Г - вторая, но для акта А, при истинном Б не существует акта В
# !!! 'OWL_TRUE' - заменить на нужное !!!
# NoThenBranchIfTrueError
IF_st(?alt)
hasOrigin(?alt_act, ?alt)
hasFirstAct(?alt_act, ?cond_act)
evalsTo(?cond_act, OWL_TRUE)
hasNextAct(?cond_act, ?branch_act)
# hasCondition(?alt, ?x..)
hasThenBranch(?alt, ?branch)
hasOrigin(?branch_act, ?actual_branch)
DifferentFrom(?branch, ?actual_branch)
 -> message(ERRORS, "NoThenBranchIfTrueError")

# Утв-5 : Ош-2
# А является альтернативой, Б её условие, В - первая ветка, а Г - вторая, но для акта А, при истинном Б существует акт Г
# ExtraElseBranchIfTrueError
IF_st(?alt)
hasOrigin(?alt_act, ?alt)
hasFirstAct(?alt_act, ?cond_act)
evalsTo(?cond_act, OWL_TRUE)
hasNextAct(?cond_act, ?branch_act)
hasElseBranch(?alt, ?branch)
hasOrigin(?branch_act, ?actual_branch)
SameAs(?branch, ?actual_branch)
 -> message(ERRORS, "ExtraElseBranchIfTrueError")

# Утв-5 : Ош-3
# А является альтернативой, Б её условие, В - первая ветка, а Г - вторая, но для акта А, при ложном Б не существует акта Г
# NoElseBranchIfFalseError
IF_st(?alt)
hasOrigin(?alt_act, ?alt)
hasFirstAct(?alt_act, ?cond_act)
evalsTo(?cond_act, OWL_FALSE)
hasNextAct(?cond_act, ?branch_act)
hasElseBranch(?alt, ?branch)
hasOrigin(?branch_act, ?actual_branch)
DifferentFrom(?branch, ?actual_branch)
 -> message(ERRORS, "NoElseBranchIfFalseError")

# Утв-5 : Ош-4
# А является альтернативой, Б её условие, В - первая ветка, а Г - вторая, но для акта А, при ложном Б существует акт В
# ExtraThenBranchIfFalseError
IF_st(?alt)
hasOrigin(?alt_act, ?alt)
hasFirstAct(?alt_act, ?cond_act)
evalsTo(?cond_act, OWL_FALSE)
hasNextAct(?cond_act, ?branch_act)
hasThenBranch(?alt, ?branch)
hasOrigin(?branch_act, ?actual_branch)
SameAs(?branch, ?actual_branch)
 -> message(ERRORS, "NoThenBranchIfTrueError")


# Утв-6 : Ош-1 , изменённая
# А является циклом пока, Б его условием, В его телом,  но для акта А существует такой акт Г, что конец акта В(i) < Г < начало акта В(i+1)
# ->
# А является циклом WHILE, Б его условием, В его телом,  но для акта А существует такой акт Г, что конец некоторого акта В < Г < начало акта Б.
# (проверим, что после тела ЕСТЬ след. условие, т.е. выход из тела произошёл не по break. Проверим. что следующий после тела акт - не условие)
# ExtraActBetweenLoopBodyAndConditionError
WHILE_st(?loop)
hasCondition(?loop, ?cond)
hasBody(?loop, ?body)
hasOrigin(?loop_act, ?loop)

hasContext(?cond_act, ?loop_act)
hasOrigin(?cond_act, ?cond)
hasContext(?body_act, ?loop_act)
hasOrigin(?body_act, ?body)

before(?body_act, ?cond_act)
hasNextAct(?body_act, ?next_act)

DifferentFrom(?next_act, ?cond_act)
 -> message(ERRORS, "ExtraActBetweenLoopBodyAndConditionError")

