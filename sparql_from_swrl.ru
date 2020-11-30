PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX my:  <http://vstu.ru/poas/ctrl_structs_2020-05_v1#>

# 		  4 RDFS core rules			  #
# =================================== #

# (?x ?p ?y), (?p rdfs:domain ?c) -> (?x rdf:type ?c) .

# (?x ?p ?y), (?p rdfs:range ?c) -> (?y rdf:type ?c) .


# (?a ?p ?b), (?p rdfs:subPropertyOf ?q) -> (?a ?q ?b) .
INSERT
  { ?a ?q ?b }
WHERE
  {
    ?p rdfs:subPropertyOf ?q . 
    ?a ?p ?b .
  } ;


# (?x rdfs:subClassOf ?y), (?a rdf:type ?x) -> (?a rdf:type ?y) .
INSERT
  { ?a rdf:type ?y }
WHERE
  {
    ?x rdfs:subClassOf ?y. 
    ?a rdf:type ?x .
  } ;



# SPARQL queries generated from SWRL rules #
# ======================================== #


# Rule: Incr_index [helper & correct]
INSERT
  { ?b my:index ?ib . }
WHERE
  {
    ?a my:next_act ?b . ?a my:index ?ia . BIND( ?ia + 1 as ?ib ) .
  } ;

# Rule: DepthIncr_rule_s6 [helper & correct]
INSERT
  { ?a my:parent_of ?b . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:next_act ?b . ?b rdf:type my:act_begin .
  } ;

# Rule: student_DepthIncr_rule_s6 [helper & mistake]
INSERT
  { ?a my:student_parent_of ?b . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:student_next ?b . ?b rdf:type my:act_begin .
  } ;

# Rule: DepthSame_b-e_rule_s7 [helper & correct]
INSERT
  { ?p my:parent_of ?b . ?a my:corresponding_end ?b . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:next_act ?b . ?b rdf:type my:act_end . ?p my:parent_of ?a .
  } ;

# Rule: student_DepthSame_b-e_rule_s7 [helper & mistake]
INSERT
  { ?p my:student_parent_of ?b . ?a my:student_corresponding_end ?b . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:student_next ?b . ?b rdf:type my:act_end . ?p my:student_parent_of ?a .
  } ;

# Rule: DepthSame_e-b_rule_s8 [helper & correct]
INSERT
  { ?p my:parent_of ?b . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:next_act ?b . ?b rdf:type my:act_begin . ?p my:parent_of ?a .
  } ;

# Rule: student_DepthSame_e-b_rule_s8 [helper & mistake]
INSERT
  { ?p my:student_parent_of ?b . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:student_next ?b . ?b rdf:type my:act_begin . ?p my:student_parent_of ?a .
  } ;

# Rule: DepthDecr_rule_s9 [helper & correct]
INSERT
  { ?p my:corresponding_end ?b . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:next_act ?b . ?b rdf:type my:act_end . ?p my:parent_of ?a .
  } ;

# Rule: student_DepthDecr_rule_s9 [helper & mistake]
INSERT
  { ?p my:student_corresponding_end ?b . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:student_next ?b . ?b rdf:type my:act_end . ?p my:student_parent_of ?a .
  } ;

# Rule: SameParentOfCorrActs_rule_s10 [helper & correct]
INSERT
  { ?p my:parent_of ?b . }
WHERE
  {
    ?a my:corresponding_end ?b . ?p my:parent_of ?a .
  } ;

# Rule: student_SameParentOfCorrActs_rule_s10 [helper & mistake]
INSERT
  { ?p my:student_parent_of ?b . }
WHERE
  {
    ?a my:corresponding_end ?b . ?p my:student_parent_of ?a .
  } ;

# Rule: Earliest_after_act_is_previous_correct_sibling [helper & correct]
INSERT
  { ?s my:after_act ?a . }
WHERE
  {
    ?a rdf:type my:correct_act . ?a my:next_sibling ?s .
  } ;

# Rule: Propagate_after_act [helper & correct]
INSERT
  { ?s my:after_act ?b . }
WHERE
  {
    ?s my:after_act ?a . ?a my:next_act ?b . ?b my:id ?ib . ?s my:id ?is . FILTER ( ?ib != ?is ) .
  } ;

# Rule: start__to__MainFunctionBegin__rule_g3 [correct & function & entry]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:FunctionBegin . }
WHERE
  {
    ?a rdf:type my:trace . ?a my:executes ?alg . ?alg my:entry_point ?func_ . ?func_ rdf:type my:func . ?b rdf:type my:act_begin . ?a my:next_sibling ?b . ?b my:executes ?func_ .
  } ;

# Rule: start__to__GlobalCode__rule_g4 [correct & entry & sequence]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:GlobalCodeBegin . }
WHERE
  {
    ?a rdf:type my:trace . ?a my:executes ?alg . ?alg my:entry_point ?gc . ?gc rdf:type my:sequence . ?b rdf:type my:act_begin . ?a my:next_sibling ?b . ?b my:executes ?gc .
  } ;

# Rule: connect_FunctionBodyBegin_rule_g5 [correct & function]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:FunctionBodyBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?func_ rdf:type my:func . ?a my:executes ?func_ . ?func_ my:body ?st . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_FuncBodyEnd_rule_g5-2 [correct & function]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:FunctionEnd . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?func_ rdf:type my:func . ?func_ my:body ?st . ?a my:executes ?st . ?b rdf:type my:act_end . ?b my:executes ?func_ . ?b my:after_act ?a .
  } ;

# Rule: connect_SequenceBegin_rule_g2 [correct & sequence]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:SequenceBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?block rdf:type my:sequence . ?a my:executes ?block . ?block my:body_item ?st . ?st rdf:type my:first_item . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_SequenceNext [correct & sequence]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:SequenceNext . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?p my:parent_of ?a . ?block rdf:type my:sequence . ?p my:executes ?block . ?block my:body_item ?st . ?a my:executes ?st . ?st my:next ?st2 . ?b rdf:type my:act_begin . ?b my:executes ?st2 . ?b my:after_act ?a .
  } ;

# Rule: connect_StmtEnd [correct & sequence]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:StmtEnd . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?st rdf:type my:stmt . ?a my:executes ?st . ?b rdf:type my:act_end . ?b my:executes ?st . ?b my:after_act ?a . ?a my:exec_time ?t . ?b my:exec_time ?_t . FILTER ( ?t = ?_t ) .
  } ;

# Rule: connect_ExprEnd [correct & sequence]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:ExprEnd . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?st rdf:type my:expr . ?a my:executes ?st . ?b rdf:type my:act_end . ?b my:executes ?st . ?b my:after_act ?a . ?a my:exec_time ?t . ?b my:exec_time ?_t . FILTER ( ?t = ?_t ) .
  } ;

# Rule: connect_SequenceEnd [correct & sequence]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:SequenceEnd . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?a my:executes ?st . ?st rdf:type my:last_item . ?b rdf:type my:act_end . ?p my:parent_of ?a . ?p my:executes ?block . ?b my:executes ?block . ?block my:body_item ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_AltBegin [alternative & correct]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:AltBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?alt rdf:type my:alternative . ?a my:executes ?alt . ?alt my:branches_item ?br . ?br rdf:type my:first_item . ?br my:cond ?cnd . ?b rdf:type my:act_begin . ?b my:executes ?cnd . ?b my:after_act ?a .
  } ;

# Rule: connect_AltBranchBegin_CondTrue [alternative & correct]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:AltBranchBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value true . ?br my:cond ?cnd . ?br rdf:type my:alt_branch . ?b rdf:type my:act_begin . ?b my:executes ?br . ?b my:after_act ?a .
  } ;

# Rule: connect_NextAltCondition [alternative & correct]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:NextAltCondition . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?br rdf:type my:alt_branch . ?br my:next ?br2 . ?br2 my:cond ?cnd2 . ?b rdf:type my:act_begin . ?b my:executes ?cnd2 . ?b my:after_act ?a .
  } ;

# Rule: connect_AltElseBranch [alternative & correct]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:AltElseBranchBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?br rdf:type my:alt_branch . ?br my:next ?br2 . ?br2 rdf:type my:else . ?b rdf:type my:act_begin . ?b my:executes ?br2 . ?b my:after_act ?a .
  } ;

# Rule: connect_AltEndAllFalse [alternative & correct]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:AltEndAllFalse . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?br rdf:type my:alt_branch . ?alt my:branches_item ?br . ?br rdf:type my:last_item . ?alt rdf:type my:alternative . ?b rdf:type my:act_end . ?b my:executes ?alt . ?b my:after_act ?a .
  } ;

# Rule: connect_AltEndAfterBranch [alternative & correct]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:AltEndAfterBranch . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?a my:executes ?br . ?alt my:branches_item ?br . ?alt rdf:type my:alternative . ?b rdf:type my:act_end . ?b my:executes ?alt . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopBegin-cond [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:PreCondLoopBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?loop rdf:type my:pre_conditional_loop . ?a my:executes ?loop . ?loop my:cond ?cnd . ?b rdf:type my:act_begin . ?b my:executes ?cnd . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopBegin-body [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:PostCondLoopBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?loop rdf:type my:post_conditional_loop . ?a my:executes ?loop . ?loop my:body ?st . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopCond1-BodyBegin [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:IterationBeginOnTrueCond . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:cond_then_body . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value true . ?loop my:body ?st . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopCond0-body [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:IterationBeginOnFalseCond . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:inverse_conditional_loop . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value false . ?loop my:body ?st . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopCond1-update [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopUpdateOnTrueCond . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:pre_update_loop . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value true . ?loop my:update ?upd . ?b rdf:type my:act_begin . ?b my:executes ?upd . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopUpdate-body [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopBodyAfterUpdate . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:pre_update_loop . ?loop my:update ?upd . ?a my:executes ?upd . ?loop my:body ?st . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopCond0-LoopEnd [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:NormalLoopEnd . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:conditional_loop . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value false . ?b rdf:type my:act_end . ?b my:executes ?loop . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopCond1-LoopEnd [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:NormalLoopEnd . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:inverse_conditional_loop . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value true . ?b rdf:type my:act_end . ?b my:executes ?loop . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopBody-cond [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopCondBeginAfterIteration . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:body_then_cond . ?loop my:body ?st . ?a my:executes ?st . ?loop my:cond ?cnd . ?b rdf:type my:act_begin . ?b my:executes ?cnd . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopBegin-init [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopWithInitBegin . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_begin . ?a my:executes ?loop . ?loop rdf:type my:loop_with_initialization . ?loop my:init ?st . ?b rdf:type my:act_begin . ?b my:executes ?st . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopInit-cond [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopCondBeginAfterInit . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:loop_with_initialization . ?loop my:init ?st . ?a my:executes ?st . ?loop my:cond ?cnd . ?b rdf:type my:act_begin . ?b my:executes ?cnd . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopBody-update [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopUpdateAfterIteration . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:post_update_loop . ?loop my:body ?st . ?a my:executes ?st . ?loop my:update ?upd . ?b rdf:type my:act_begin . ?b my:executes ?upd . ?b my:after_act ?a .
  } ;

# Rule: connect_LoopUpdate-cond [correct & loop]
INSERT
  { ?b rdf:type my:normal_flow_correct_act . ?a my:next_act ?b . ?b rdf:type my:LoopCondAfterUpdate . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:post_update_loop . ?loop my:update ?st . ?a my:executes ?st . ?loop my:cond ?cnd . ?b rdf:type my:act_begin . ?b my:executes ?cnd . ?b my:after_act ?a .
  } ;

# Rule: CorrespondingActsMismatch_Error [mistake]
INSERT
  { ?b rdf:type my:CorrespondingEndMismatched . ?b my:cause ?a . }
WHERE
  {
    ?a my:student_corresponding_end ?b . ?a my:executes ?s1 . ?b my:executes ?s2 . ?s1 my:id ?ib . ?s2 my:id ?ic . FILTER ( ?ib != ?ic ) .
  } ;

# Rule: GenericWrongAct_Error [mistake]
INSERT
  { ?c my:should_be ?b . ?c my:precursor ?a . ?c rdf:type my:Erroneous . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c . ?b my:id ?ib . ?c my:id ?ic . FILTER ( ?ib != ?ic ) .
  } ;

# Rule: GenericWrongParent_Error [mistake]
INSERT
  { ?a my:context_should_be ?p . ?a rdf:type my:WrongContext . }
WHERE
  {
    ?p my:parent_of ?a . ?c my:student_parent_of ?a . ?p my:id ?ip . ?c my:id ?ic . FILTER ( ?ip != ?ic ) .
  } ;

# Rule: MisplacedBefore_Error [mistake]
INSERT
  { ?a rdf:type my:MisplacedBefore . ?e rdf:type my:MisplacedBefore . }
WHERE
  {
    ?a rdf:type my:WrongContext . ?a my:corresponding_end ?e . ?p my:parent_of ?a . ?e my:student_index ?ie . ?p my:student_index ?ip . FILTER ( ?ie < ?ip ) .
  } ;

# Rule: MisplacedAfter_Error [mistake]
INSERT
  { ?a rdf:type my:MisplacedAfter . ?e rdf:type my:MisplacedAfter . }
WHERE
  {
    ?a rdf:type my:WrongContext . ?a my:corresponding_end ?e . ?p my:parent_of ?a . ?p my:corresponding_end ?pe . ?a my:student_index ?ia . ?pe my:student_index ?ipe . FILTER ( ?ipe < ?ia ) .
  } ;

# Rule: MisplacedDeeper_Error [mistake]
INSERT
  { ?a rdf:type my:MisplacedDeeper . ?e rdf:type my:MisplacedDeeper . }
WHERE
  {
    ?a rdf:type my:WrongContext . ?a my:corresponding_end ?e . ?p my:parent_of ?a . ?p my:corresponding_end ?pe . ?a my:student_index ?ia . ?p my:student_index ?ip . FILTER ( ?ip < ?ia ) . ?e my:student_index ?ie . ?pe my:student_index ?ipe . FILTER ( ?ie < ?ipe ) .
  } ;

# Rule: GenericWrongExecTime-b_Error [mistake]
INSERT
  { ?c rdf:type my:WrongExecTime . }
WHERE
  {
    ?c rdf:type my:Erroneous . ?c my:should_be ?b . ?b rdf:type my:act_begin . ?c rdf:type my:act_begin . ?c my:executes ?st . ?b my:executes ?st . ?c my:exec_time ?n1 . ?b my:exec_time ?n2 . FILTER ( ?n1 != ?n2 ) .
  } ;

# Rule: GenericWrongExecTime-e_Error [mistake]
INSERT
  { ?c rdf:type my:WrongExecTime . }
WHERE
  {
    ?c rdf:type my:Erroneous . ?c my:should_be ?b . ?b rdf:type my:act_end . ?c rdf:type my:act_end . ?c my:executes ?st . ?b my:executes ?st . ?c my:exec_time ?n1 . ?b my:exec_time ?n2 . FILTER ( ?n1 != ?n2 ) .
  } ;

# Rule: ActStartsAfterItsEnd_Error [mistake]
INSERT
  { ?a my:cause ?b . ?b my:cause ?a . ?a rdf:type my:ActStartsAfterItsEnd . ?b rdf:type my:ActEndsWithoutStart . }
WHERE
  {
    ?a my:in_trace ?tr . ?b my:in_trace ?tr . ?a rdf:type my:act_begin . ?b rdf:type my:act_end . ?a my:executes ?st . ?b my:executes ?st . ?a my:exec_time ?n . ?b my:exec_time ?n . ?a my:student_index ?ia . ?b my:student_index ?ib . FILTER ( ?ib < ?ia ) .
  } ;

# Rule: DuplicateOfAct-seq-b_Error [mistake & sequence]
INSERT
  { ?c1 my:cause ?c . ?c1 rdf:type my:DuplicateOfAct . }
WHERE
  {
    ?c1 rdf:type my:ExtraAct . ?c1 rdf:type my:act_begin . ?p my:student_parent_of ?c1 . ?p my:executes ?block . ?block rdf:type my:sequence . ?block my:body_item ?st . ?c1 my:executes ?st . ?c my:executes ?st . ?p my:student_parent_of ?c . ?c rdf:type my:act_begin . ?c1 my:id ?ic1 . ?c my:id ?ic . FILTER ( ?ic1 != ?ic ) .
  } ;

# Rule: DuplicateOfAct-seq-e_Error [mistake & sequence]
INSERT
  { ?c1 my:cause ?c . ?c1 rdf:type my:DuplicateOfAct . }
WHERE
  {
    ?c1 rdf:type my:ExtraAct . ?c1 rdf:type my:act_end . ?p my:student_parent_of ?c1 . ?p my:executes ?block . ?block rdf:type my:sequence . ?block my:body_item ?st . ?c1 my:executes ?st . ?c my:executes ?st . ?p my:student_parent_of ?c . ?c rdf:type my:act_end . ?c1 my:id ?ic1 . ?c my:id ?ic . FILTER ( ?ic1 != ?ic ) .
  } ;

# Rule: DisplacedAct_Error [mistake & sequence]
INSERT
  { ?c1 rdf:type my:DisplacedAct . }
WHERE
  {
    ?c1 rdf:type my:ExtraAct . ?c1 rdf:type my:MissingAct .
  } ;

# Rule: TooEarlyInSequence_Error [mistake & sequence]
INSERT
  { ?b my:should_be_after ?a . ?b rdf:type my:TooEarlyInSequence . }
WHERE
  {
    ?b rdf:type my:TooEarly . ?sa my:student_parent_of ?b . ?sa my:executes ?seq . ?seq rdf:type my:sequence . ?a my:should_be_before ?b . ?sa my:student_parent_of ?a .
  } ;

# Rule: NoFirstCondition-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:NoFirstCondition . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?alt . ?alt rdf:type my:alternative . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: BranchOfFalseCondition-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b my:cause ?a . ?b rdf:type my:BranchOfFalseCondition . }
WHERE
  {
    ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?br rdf:type my:alt_branch . ?b rdf:type my:act_begin . ?b my:executes ?br . ?alt_act my:parent_of ?a . ?alt_act my:student_parent_of ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: WrongBranch-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:WrongBranch . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?br . ?alt my:branches_item ?br . ?alt rdf:type my:alternative . ?b rdf:type my:act_begin . ?b my:executes ?br2 . ?alt my:branches_item ?br2 . ?br my:id ?i . ?br2 my:id ?i2 . FILTER ( ?i != ?i2 ) . ?alt_act my:parent_of ?a . ?alt_act my:student_parent_of ?b .
  } ;

# Rule: ConditionAfterBranch-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:ConditionAfterBranch . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:executes ?br . ?alt my:branches_item ?br . ?alt rdf:type my:alternative . ?a my:student_next ?b . ?b rdf:type my:ExtraAct . ?b my:executes ?cnd . ?cnd rdf:type my:expr .
  } ;

# Rule: AnotherExtraBranch-alt_Error [alternative & mistake]
INSERT
  { ?b my:cause ?a . ?b rdf:type my:AnotherExtraBranch . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?br . ?alt my:branches_item ?br . ?alt rdf:type my:alternative . ?b rdf:type my:act_begin . ?b my:executes ?br2 . ?alt my:branches_item ?br2 . ?alt_act my:student_parent_of ?a . ?alt_act my:student_parent_of ?b . ?a my:student_index ?sia . ?b my:student_index ?sib . FILTER ( ?sib > ?sia ) .
  } ;

# Rule: NoBranchWhenConditionIsTrue-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:NoBranchWhenConditionIsTrue . }
WHERE
  {
    ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value true . ?br my:cond ?cnd . ?br rdf:type my:alt_branch . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: AllFalseNoElse-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:AllFalseNoElse . }
WHERE
  {
    ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?br my:next ?br2 . ?br2 rdf:type my:else . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: NoNextCondition-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:NoNextCondition . }
WHERE
  {
    ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?br my:next ?br2 . ?br2 my:cond ?cnd2 . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: AllFalseNoEnd-alt_Error [alternative & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:AllFalseNoEnd . }
WHERE
  {
    ?a rdf:type my:act_end . ?cnd rdf:type my:expr . ?a my:executes ?cnd . ?a my:expr_value false . ?br my:cond ?cnd . ?alt my:branches_item ?br . ?alt rdf:type my:alternative . ?br rdf:type my:last_item . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: MissingIterationAfterSuccessfulCondition-1-loop_Error [loop & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:MissingIterationAfterSuccessfulCondition . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:cond_then_body . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value true . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: MissingIterationAfterSuccessfulCondition-0-loop_Error [loop & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:MissingIterationAfterSuccessfulCondition . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:inverse_conditional_loop . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value false . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: MissingLoopEndAfterFailedCondition-0-loop_Error [loop & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:MissingLoopEndAfterFailedCondition . }
WHERE
  {
    ?a rdf:type my:normal_flow_correct_act . ?a rdf:type my:act_end . ?loop rdf:type my:cond_then_body . ?loop my:cond ?cnd . ?a my:executes ?cnd . ?a my:expr_value false . ?a my:student_next ?b . ?b rdf:type my:Erroneous .
  } ;

# Rule: IterationAfterFailedCondition-loop_Error [loop & mistake]
INSERT
  { ?b my:should_be ?a . ?b my:precursor ?a . ?b rdf:type my:IterationAfterFailedCondition . }
WHERE
  {
    ?b rdf:type my:MissingLoopEndAfterFailedCondition . ?b rdf:type my:act_begin . ?b my:executes ?st . ?L my:body ?st . ?L rdf:type my:loop .
  } ;

# Rule: ExtraAct_1_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?b .
  } ;

# Rule: MissingAct_1_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?b .
  } ;

# Rule: ExtraAct_2_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?b .
  } ;

# Rule: MissingAct_2_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?b .
  } ;

# Rule: ExtraAct_3_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?b .
  } ;

# Rule: MissingAct_3_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?b .
  } ;

# Rule: ExtraAct_4_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?b .
  } ;

# Rule: MissingAct_4_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?b .
  } ;

# Rule: ExtraAct_5_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?b .
  } ;

# Rule: MissingAct_5_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?b .
  } ;

# Rule: ExtraAct_6_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?b .
  } ;

# Rule: MissingAct_6_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?b .
  } ;

# Rule: ExtraAct_7_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . ?c7 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?c7 . ?c7 my:student_next ?b .
  } ;

# Rule: MissingAct_7_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?c7 rdf:type my:MissingAct . ?c7 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?c7 . ?c7 my:next_act ?b .
  } ;

# Rule: ExtraAct_8_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . ?c7 rdf:type my:ExtraAct . ?c8 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?c7 . ?c7 my:student_next ?c8 . ?c8 my:student_next ?b .
  } ;

# Rule: MissingAct_8_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?c7 rdf:type my:MissingAct . ?c7 my:should_be_before ?b . ?c8 rdf:type my:MissingAct . ?c8 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?c7 . ?c7 my:next_act ?c8 . ?c8 my:next_act ?b .
  } ;

# Rule: ExtraAct_9_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . ?c7 rdf:type my:ExtraAct . ?c8 rdf:type my:ExtraAct . ?c9 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?c7 . ?c7 my:student_next ?c8 . ?c8 my:student_next ?c9 . ?c9 my:student_next ?b .
  } ;

# Rule: MissingAct_9_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?c7 rdf:type my:MissingAct . ?c7 my:should_be_before ?b . ?c8 rdf:type my:MissingAct . ?c8 my:should_be_before ?b . ?c9 rdf:type my:MissingAct . ?c9 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?c7 . ?c7 my:next_act ?c8 . ?c8 my:next_act ?c9 . ?c9 my:next_act ?b .
  } ;

# Rule: ExtraAct_10_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . ?c7 rdf:type my:ExtraAct . ?c8 rdf:type my:ExtraAct . ?c9 rdf:type my:ExtraAct . ?c10 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?c7 . ?c7 my:student_next ?c8 . ?c8 my:student_next ?c9 . ?c9 my:student_next ?c10 . ?c10 my:student_next ?b .
  } ;

# Rule: MissingAct_10_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?c7 rdf:type my:MissingAct . ?c7 my:should_be_before ?b . ?c8 rdf:type my:MissingAct . ?c8 my:should_be_before ?b . ?c9 rdf:type my:MissingAct . ?c9 my:should_be_before ?b . ?c10 rdf:type my:MissingAct . ?c10 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?c7 . ?c7 my:next_act ?c8 . ?c8 my:next_act ?c9 . ?c9 my:next_act ?c10 . ?c10 my:next_act ?b .
  } ;

# Rule: ExtraAct_11_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . ?c7 rdf:type my:ExtraAct . ?c8 rdf:type my:ExtraAct . ?c9 rdf:type my:ExtraAct . ?c10 rdf:type my:ExtraAct . ?c11 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?c7 . ?c7 my:student_next ?c8 . ?c8 my:student_next ?c9 . ?c9 my:student_next ?c10 . ?c10 my:student_next ?c11 . ?c11 my:student_next ?b .
  } ;

# Rule: MissingAct_11_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?c7 rdf:type my:MissingAct . ?c7 my:should_be_before ?b . ?c8 rdf:type my:MissingAct . ?c8 my:should_be_before ?b . ?c9 rdf:type my:MissingAct . ?c9 my:should_be_before ?b . ?c10 rdf:type my:MissingAct . ?c10 my:should_be_before ?b . ?c11 rdf:type my:MissingAct . ?c11 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?c7 . ?c7 my:next_act ?c8 . ?c8 my:next_act ?c9 . ?c9 my:next_act ?c10 . ?c10 my:next_act ?c11 . ?c11 my:next_act ?b .
  } ;

# Rule: ExtraAct_12_Error [mistake]
INSERT
  { ?c1 rdf:type my:ExtraAct . ?c2 rdf:type my:ExtraAct . ?c3 rdf:type my:ExtraAct . ?c4 rdf:type my:ExtraAct . ?c5 rdf:type my:ExtraAct . ?c6 rdf:type my:ExtraAct . ?c7 rdf:type my:ExtraAct . ?c8 rdf:type my:ExtraAct . ?c9 rdf:type my:ExtraAct . ?c10 rdf:type my:ExtraAct . ?c11 rdf:type my:ExtraAct . ?c12 rdf:type my:ExtraAct . }
WHERE
  {
    ?a my:next_act ?b . ?a my:student_next ?c1 . ?c1 my:student_next ?c2 . ?c2 my:student_next ?c3 . ?c3 my:student_next ?c4 . ?c4 my:student_next ?c5 . ?c5 my:student_next ?c6 . ?c6 my:student_next ?c7 . ?c7 my:student_next ?c8 . ?c8 my:student_next ?c9 . ?c9 my:student_next ?c10 . ?c10 my:student_next ?c11 . ?c11 my:student_next ?c12 . ?c12 my:student_next ?b .
  } ;

# Rule: MissingAct_12_Error [mistake]
INSERT
  { ?c1 rdf:type my:MissingAct . ?c1 my:should_be_before ?b . ?c2 rdf:type my:MissingAct . ?c2 my:should_be_before ?b . ?c3 rdf:type my:MissingAct . ?c3 my:should_be_before ?b . ?c4 rdf:type my:MissingAct . ?c4 my:should_be_before ?b . ?c5 rdf:type my:MissingAct . ?c5 my:should_be_before ?b . ?c6 rdf:type my:MissingAct . ?c6 my:should_be_before ?b . ?c7 rdf:type my:MissingAct . ?c7 my:should_be_before ?b . ?c8 rdf:type my:MissingAct . ?c8 my:should_be_before ?b . ?c9 rdf:type my:MissingAct . ?c9 my:should_be_before ?b . ?c10 rdf:type my:MissingAct . ?c10 my:should_be_before ?b . ?c11 rdf:type my:MissingAct . ?c11 my:should_be_before ?b . ?c12 rdf:type my:MissingAct . ?c12 my:should_be_before ?b . ?b rdf:type my:TooEarly . }
WHERE
  {
    ?a my:student_next ?b . ?a my:next_act ?c1 . ?c1 my:next_act ?c2 . ?c2 my:next_act ?c3 . ?c3 my:next_act ?c4 . ?c4 my:next_act ?c5 . ?c5 my:next_act ?c6 . ?c6 my:next_act ?c7 . ?c7 my:next_act ?c8 . ?c8 my:next_act ?c9 . ?c9 my:next_act ?c10 . ?c10 my:next_act ?c11 . ?c11 my:next_act ?c12 . ?c12 my:next_act ?b .
  } ;

# Rule: LoopIteration1_after_0 [helper & correct & loop]
INSERT
  { ?c0 my:iteration_n 1 . ?ce0 my:iteration_n 1 . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?L . ?L rdf:type my:loop . ?L my:body ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st . ?c0 my:corresponding_end ?ce0 .
  } ;

# Rule: LoopIteration1_after_1 [helper & correct & loop]
INSERT
  { ?c1 my:iteration_n 1 . ?ce1 my:iteration_n 1 . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?L . ?L rdf:type my:loop . ?L my:body ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st0 . ?st0 my:id ?st0_i . FILTER ( ?st0_i != ?body_i ) . ?c0 my:corresponding_end ?ce0 . ?ce0 my:next_act ?c1 . ?c1 my:executes ?st . ?c1 my:corresponding_end ?ce1 .
  } ;

# Rule: LoopIteration1_after_2 [helper & correct & loop]
INSERT
  { ?c2 my:iteration_n 1 . ?ce2 my:iteration_n 1 . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?L . ?L rdf:type my:loop . ?L my:body ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st0 . ?st0 my:id ?st0_i . FILTER ( ?st0_i != ?body_i ) . ?c0 my:corresponding_end ?ce0 . ?ce0 my:next_act ?c1 . ?c1 my:executes ?st1 . ?st1 my:id ?st1_i . FILTER ( ?st1_i != ?body_i ) . ?c1 my:corresponding_end ?ce1 . ?ce1 my:next_act ?c2 . ?c2 my:executes ?st . ?c2 my:corresponding_end ?ce2 .
  } ;

# Rule: LoopIteration1_after_3 [helper & correct & loop]
INSERT
  { ?c3 my:iteration_n 1 . ?ce3 my:iteration_n 1 . }
WHERE
  {
    ?a rdf:type my:act_begin . ?a my:executes ?L . ?L rdf:type my:loop . ?L my:body ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st0 . ?st0 my:id ?st0_i . FILTER ( ?st0_i != ?body_i ) . ?c0 my:corresponding_end ?ce0 . ?ce0 my:next_act ?c1 . ?c1 my:executes ?st1 . ?st1 my:id ?st1_i . FILTER ( ?st1_i != ?body_i ) . ?c1 my:corresponding_end ?ce1 . ?ce1 my:next_act ?c2 . ?c2 my:executes ?st2 . ?st2 my:id ?st2_i . FILTER ( ?st2_i != ?body_i ) . ?c2 my:corresponding_end ?ce2 . ?ce2 my:next_act ?c3 . ?c3 my:executes ?st . ?c3 my:corresponding_end ?ce3 .
  } ;

# Rule: LoopIterationNext_after_0 [helper & correct & loop]
INSERT
  { ?c0 my:iteration_n ?n_next . ?ce0 my:iteration_n ?n_next . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:iteration_n ?n . ?a my:executes ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st . ?c0 my:corresponding_end ?ce0 . BIND( ?n + 1 as ?n_next ) .
  } ;

# Rule: LoopIterationNext_after_1 [helper & correct & loop]
INSERT
  { ?c1 my:iteration_n ?n_next . ?ce1 my:iteration_n ?n_next . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:iteration_n ?n . ?a my:executes ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st0 . ?st0 my:id ?st0_i . FILTER ( ?st0_i != ?body_i ) . ?c0 my:corresponding_end ?ce0 . ?ce0 my:next_act ?c1 . ?c1 my:executes ?st . ?c1 my:corresponding_end ?ce1 . BIND( ?n + 1 as ?n_next ) .
  } ;

# Rule: LoopIterationNext_after_2 [helper & correct & loop]
INSERT
  { ?c2 my:iteration_n ?n_next . ?ce2 my:iteration_n ?n_next . }
WHERE
  {
    ?a rdf:type my:act_end . ?a my:iteration_n ?n . ?a my:executes ?st . ?st my:id ?body_i . ?a my:next_act ?c0 . ?c0 my:executes ?st0 . ?st0 my:id ?st0_i . FILTER ( ?st0_i != ?body_i ) . ?c0 my:corresponding_end ?ce0 . ?ce0 my:next_act ?c1 . ?c1 my:executes ?st1 . ?st1 my:id ?st1_i . FILTER ( ?st1_i != ?body_i ) . ?c1 my:corresponding_end ?ce1 . ?ce1 my:next_act ?c2 . ?c2 my:executes ?st . ?c2 my:corresponding_end ?ce2 . BIND( ?n + 1 as ?n_next ) .
  } ;

