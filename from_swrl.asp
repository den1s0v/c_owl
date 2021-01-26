
% Rule: Incr_index [correct & helper]
	t(B, index, IB):-
	t(A, next_act, B), t(A, index, IA), IB = IA + 1.

% Rule: DepthIncr_rule_s6 [correct & helper]
	t(A, parent_of, B):-
	t(A, type, act_begin), t(A, next_act, B), t(B, type, act_begin).

% Rule: student_DepthIncr_rule_s6 [helper & mistake]
	t(A, student_parent_of, B):-
	t(A, type, act_begin), t(A, student_next, B), t(B, type, act_begin).

% Rule: DepthSame_b-e_rule_s7 [correct & helper]
	t(P, parent_of, B):-
	t(A, type, act_begin), t(A, next_act, B), t(B, type, act_end), 
	t(P, parent_of, A).
	t(A, corresponding_end, B):-
	t(A, type, act_begin), t(A, next_act, B), t(B, type, act_end), 
	t(P, parent_of, A).

% Rule: student_DepthSame_b-e_rule_s7 [helper & mistake]
	t(P, student_parent_of, B):-
	t(A, type, act_begin), t(A, student_next, B), t(B, type, act_end), 
	t(P, student_parent_of, A).
	t(A, student_corresponding_end, B):-
	t(A, type, act_begin), t(A, student_next, B), t(B, type, act_end), 
	t(P, student_parent_of, A).

% Rule: DepthSame_e-b_rule_s8 [correct & helper]
	t(P, parent_of, B):-
	t(A, type, act_end), t(A, next_act, B), t(B, type, act_begin), 
	t(P, parent_of, A).

% Rule: student_DepthSame_e-b_rule_s8 [helper & mistake]
	t(P, student_parent_of, B):-
	t(A, type, act_end), t(A, student_next, B), t(B, type, act_begin), 
	t(P, student_parent_of, A).

% Rule: DepthDecr_rule_s9 [correct & helper]
	t(P, corresponding_end, B):-
	t(A, type, act_end), t(A, next_act, B), t(B, type, act_end), 
	t(P, parent_of, A).

% Rule: student_DepthDecr_rule_s9 [helper & mistake]
	t(P, student_corresponding_end, B):-
	t(A, type, act_end), t(A, student_next, B), t(B, type, act_end), 
	t(P, student_parent_of, A).

% Rule: SameParentOfCorrActs_rule_s10 [correct & helper]
	t(P, parent_of, B):-
	t(A, corresponding_end, B), t(P, parent_of, A).

% Rule: student_SameParentOfCorrActs_rule_s10 [helper & mistake]
	t(P, student_parent_of, B):-
	t(A, corresponding_end, B), t(P, student_parent_of, A).

% Rule: Earliest_after_act_is_previous_correct_sibling [correct & helper]
	t(S, after_act, A):-
	t(A, type, correct_act),             
	t(A, next_sibling, S).

% Rule: Propagate_after_act [correct & helper]
	t(S, after_act, B):-
	t(S, after_act, A),
	t(A, next_act, B),
	                        
		t(B, id, IB),
		t(S, id, IS),
		IB != IS.

% Rule: start__to__MainFunctionBegin__rule_g3 [correct & entry & function]
	t(B, type, normal_flow_correct_act):-
	t(A, type, trace),
	t(A, executes, ALG),
	t(ALG, entry_point, FUNC_),
	t(FUNC_, type, func), 
	t(B, type, act_begin),
	t(A, next_sibling, B),
	t(B, executes, FUNC_).
	t(A, next_act, B):-
	t(A, type, trace),
	t(A, executes, ALG),
	t(ALG, entry_point, FUNC_),
	t(FUNC_, type, func), 
	t(B, type, act_begin),
	t(A, next_sibling, B),
	t(B, executes, FUNC_).
	t(B, type, functionBegin):-
	t(A, type, trace),
	t(A, executes, ALG),
	t(ALG, entry_point, FUNC_),
	t(FUNC_, type, func), 
	t(B, type, act_begin),
	t(A, next_sibling, B),
	t(B, executes, FUNC_).

% Rule: start__to__GlobalCode__rule_g4 [correct & entry & sequence]
	t(B, type, normal_flow_correct_act):-
	t(A, type, trace),
	t(A, executes, ALG),
	t(ALG, entry_point, GC),
	t(GC, type, sequence), 

	t(B, type, act_begin),
	t(A, next_sibling, B),
	t(B, executes, GC).
	t(A, next_act, B):-
	t(A, type, trace),
	t(A, executes, ALG),
	t(ALG, entry_point, GC),
	t(GC, type, sequence), 

	t(B, type, act_begin),
	t(A, next_sibling, B),
	t(B, executes, GC).
	t(B, type, globalCodeBegin):-
	t(A, type, trace),
	t(A, executes, ALG),
	t(ALG, entry_point, GC),
	t(GC, type, sequence), 

	t(B, type, act_begin),
	t(A, next_sibling, B),
	t(B, executes, GC).

% Rule: connect_FunctionBodyBegin_rule_g5 [correct & function]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(FUNC_, type, func), 
	t(A, executes, FUNC_),
	t(FUNC_, body, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	                                                    
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(FUNC_, type, func), 
	t(A, executes, FUNC_),
	t(FUNC_, body, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	                                                    
	
	t(B, after_act, A).
	t(B, type, functionBodyBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(FUNC_, type, func), 
	t(A, executes, FUNC_),
	t(FUNC_, body, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	                                                    
	
	t(B, after_act, A).

% Rule: connect_FuncBodyEnd_rule_g5-2 [correct & function]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(FUNC_, type, func), 
	t(FUNC_, body, ST),
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, FUNC_),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(FUNC_, type, func), 
	t(FUNC_, body, ST),
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, FUNC_),
	
	t(B, after_act, A).
	t(B, type, functionEnd):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(FUNC_, type, func), 
	t(FUNC_, body, ST),
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, FUNC_),
	
	t(B, after_act, A).

% Rule: connect_SequenceBegin_rule_g2 [correct & sequence]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(BLOCK, type, sequence), 
	t(A, executes, BLOCK),
	t(BLOCK, body_item, ST),
	t(ST, type, first_item),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(BLOCK, type, sequence), 
	t(A, executes, BLOCK),
	t(BLOCK, body_item, ST),
	t(ST, type, first_item),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(B, type, sequenceBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(BLOCK, type, sequence), 
	t(A, executes, BLOCK),
	t(BLOCK, body_item, ST),
	t(ST, type, first_item),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).

% Rule: connect_SequenceNext [correct & sequence]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(P, parent_of, A),
	t(BLOCK, type, sequence), 
	t(P, executes, BLOCK),
	t(BLOCK, body_item, ST),
	t(A, executes, ST),
	
	t(ST, next, ST2),
	
	t(B, type, act_begin),
	t(B, executes, ST2),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(P, parent_of, A),
	t(BLOCK, type, sequence), 
	t(P, executes, BLOCK),
	t(BLOCK, body_item, ST),
	t(A, executes, ST),
	
	t(ST, next, ST2),
	
	t(B, type, act_begin),
	t(B, executes, ST2),
	
	t(B, after_act, A).
	t(B, type, sequenceNext):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(P, parent_of, A),
	t(BLOCK, type, sequence), 
	t(P, executes, BLOCK),
	t(BLOCK, body_item, ST),
	t(A, executes, ST),
	
	t(ST, next, ST2),
	
	t(B, type, act_begin),
	t(B, executes, ST2),
	
	t(B, after_act, A).

% Rule: connect_StmtEnd [correct & sequence]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ST, type, stmt), 
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, ST),
	
	t(B, after_act, A),
	
	t(A, exec_time, T), t(B, exec_time, Tmp_T),
	T = Tmp_T.
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ST, type, stmt), 
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, ST),
	
	t(B, after_act, A),
	
	t(A, exec_time, T), t(B, exec_time, Tmp_T),
	T = Tmp_T.
	t(B, type, stmtEnd):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ST, type, stmt), 
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, ST),
	
	t(B, after_act, A),
	
	t(A, exec_time, T), t(B, exec_time, Tmp_T),
	T = Tmp_T.

% Rule: connect_ExprEnd [correct & sequence]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ST, type, expr), 
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, ST),
	
	t(B, after_act, A),

	t(A, exec_time, T), t(B, exec_time, Tmp_T),
	T = Tmp_T.
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ST, type, expr), 
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, ST),
	
	t(B, after_act, A),

	t(A, exec_time, T), t(B, exec_time, Tmp_T),
	T = Tmp_T.
	t(B, type, exprEnd):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ST, type, expr), 
	t(A, executes, ST),
	
	t(B, type, act_end),
	t(B, executes, ST),
	
	t(B, after_act, A),

	t(A, exec_time, T), t(B, exec_time, Tmp_T),
	T = Tmp_T.

% Rule: connect_SequenceEnd [correct & sequence]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(A, executes, ST),
	t(ST, type, last_item),
	
	t(B, type, act_end),
	t(P, parent_of, A),
	t(P, executes, BLOCK),
                            
	t(B, executes, BLOCK),
	t(BLOCK, body_item, ST),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(A, executes, ST),
	t(ST, type, last_item),
	
	t(B, type, act_end),
	t(P, parent_of, A),
	t(P, executes, BLOCK),
                            
	t(B, executes, BLOCK),
	t(BLOCK, body_item, ST),
	
	t(B, after_act, A).
	t(B, type, sequenceEnd):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(A, executes, ST),
	t(ST, type, last_item),
	
	t(B, type, act_end),
	t(P, parent_of, A),
	t(P, executes, BLOCK),
                            
	t(B, executes, BLOCK),
	t(BLOCK, body_item, ST),
	
	t(B, after_act, A).

% Rule: connect_AltBegin [alternative & correct]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ALT, type, alternative), 
	t(A, executes, ALT),

	t(ALT, branches_item, BR),
	t(BR, type, first_item),	                             
	                                          
	t(BR, cond, CND),
	
	t(B, type, act_begin),
	t(B, executes, CND),        
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ALT, type, alternative), 
	t(A, executes, ALT),

	t(ALT, branches_item, BR),
	t(BR, type, first_item),	                             
	                                          
	t(BR, cond, CND),
	
	t(B, type, act_begin),
	t(B, executes, CND),        
	
	t(B, after_act, A).
	t(B, type, altBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(ALT, type, alternative), 
	t(A, executes, ALT),

	t(ALT, branches_item, BR),
	t(BR, type, first_item),	                             
	                                          
	t(BR, cond, CND),
	
	t(B, type, act_begin),
	t(B, executes, CND),        
	
	t(B, after_act, A).

% Rule: connect_AltBranchBegin_CondTrue [alternative & correct]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(B, after_act, A).
	t(B, type, altBranchBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(B, after_act, A).

% Rule: connect_NextAltCondition [alternative & correct]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             

	t(BR, next, BR2),
	t(BR2, cond, CND2),
	
	t(B, type, act_begin),
	t(B, executes, CND2),        
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             

	t(BR, next, BR2),
	t(BR2, cond, CND2),
	
	t(B, type, act_begin),
	t(B, executes, CND2),        
	
	t(B, after_act, A).
	t(B, type, nextAltCondition):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             

	t(BR, next, BR2),
	t(BR2, cond, CND2),
	
	t(B, type, act_begin),
	t(B, executes, CND2),        
	
	t(B, after_act, A).

% Rule: connect_AltElseBranch [alternative & correct]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	t(BR, next, BR2),
	t(BR2, type, else),
	
	t(B, type, act_begin),
	t(B, executes, BR2),        

	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	t(BR, next, BR2),
	t(BR2, type, else),
	
	t(B, type, act_begin),
	t(B, executes, BR2),        

	t(B, after_act, A).
	t(B, type, altElseBranchBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	t(BR, next, BR2),
	t(BR2, type, else),
	
	t(B, type, act_begin),
	t(B, executes, BR2),        

	t(B, after_act, A).

% Rule: connect_AltEndAllFalse [alternative & correct]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	t(ALT, branches_item, BR),
	t(BR, type, last_item),                                      
	t(ALT, type, alternative),
	
	t(B, type, act_end),
	t(B, executes, ALT),        

	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	t(ALT, branches_item, BR),
	t(BR, type, last_item),                                      
	t(ALT, type, alternative),
	
	t(B, type, act_end),
	t(B, executes, ALT),        

	t(B, after_act, A).
	t(B, type, altEndAllFalse):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),
	t(BR, type, alt_branch),                             
	t(ALT, branches_item, BR),
	t(BR, type, last_item),                                      
	t(ALT, type, alternative),
	
	t(B, type, act_end),
	t(B, executes, ALT),        

	t(B, after_act, A).

% Rule: connect_AltEndAfterBranch [alternative & correct]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_end),
	t(B, executes, ALT),                          
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_end),
	t(B, executes, ALT),                          
	
	t(B, after_act, A).
	t(B, type, altEndAfterBranch):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_end),
	t(B, executes, ALT),                          
	
	t(B, after_act, A).

% Rule: connect_LoopBegin-cond [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(LOOP, type, pre_conditional_loop), 
	t(A, executes, LOOP),

	t(LOOP, cond, CND),
	
	t(B, type, act_begin),
	t(B, executes, CND),        
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(LOOP, type, pre_conditional_loop), 
	t(A, executes, LOOP),

	t(LOOP, cond, CND),
	
	t(B, type, act_begin),
	t(B, executes, CND),        
	
	t(B, after_act, A).
	t(B, type, preCondLoopBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(LOOP, type, pre_conditional_loop), 
	t(A, executes, LOOP),

	t(LOOP, cond, CND),
	
	t(B, type, act_begin),
	t(B, executes, CND),        
	
	t(B, after_act, A).

% Rule: connect_LoopBegin-body [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(LOOP, type, post_conditional_loop), 
	t(A, executes, LOOP),

	t(LOOP, body, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(LOOP, type, post_conditional_loop), 
	t(A, executes, LOOP),

	t(LOOP, body, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(B, type, postCondLoopBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(LOOP, type, post_conditional_loop), 
	t(A, executes, LOOP),

	t(LOOP, body, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).

% Rule: connect_LoopCond1-BodyBegin [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(LOOP, body, ST),
	                        
	                  
	
	t(B, type, act_begin),
	t(B, executes, ST),
								                           
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(LOOP, body, ST),
	                        
	                  
	
	t(B, type, act_begin),
	t(B, executes, ST),
								                           
	t(B, after_act, A).
	t(B, type, iterationBeginOnTrueCond):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(LOOP, body, ST),
	                        
	                  
	
	t(B, type, act_begin),
	t(B, executes, ST),
								                           
	t(B, after_act, A).

% Rule: connect_LoopCond0-body [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    
	
	t(LOOP, body, ST),
	                        
	                  
	
	t(B, type, act_begin),
	t(B, executes, ST),
								                           
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    
	
	t(LOOP, body, ST),
	                        
	                  
	
	t(B, type, act_begin),
	t(B, executes, ST),
								                           
	t(B, after_act, A).
	t(B, type, iterationBeginOnFalseCond):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    
	
	t(LOOP, body, ST),
	                        
	                  
	
	t(B, type, act_begin),
	t(B, executes, ST),
								                           
	t(B, after_act, A).

% Rule: connect_LoopCond1-update [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, pre_update_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(LOOP, update, UPD),
	t(B, type, act_begin),
	t(B, executes, UPD),
								                           
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, pre_update_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(LOOP, update, UPD),
	t(B, type, act_begin),
	t(B, executes, UPD),
								                           
	t(B, after_act, A).
	t(B, type, loopUpdateOnTrueCond):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, pre_update_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(LOOP, update, UPD),
	t(B, type, act_begin),
	t(B, executes, UPD),
								                           
	t(B, after_act, A).

% Rule: connect_LoopUpdate-body [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, pre_update_loop), 
	t(LOOP, update, UPD),
	t(A, executes, UPD),

	t(LOOP, body, ST),
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, pre_update_loop), 
	t(LOOP, update, UPD),
	t(A, executes, UPD),

	t(LOOP, body, ST),
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(B, type, loopBodyAfterUpdate):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, pre_update_loop), 
	t(LOOP, update, UPD),
	t(A, executes, UPD),

	t(LOOP, body, ST),
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).

% Rule: connect_LoopCond0-LoopEnd [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    
	
	t(B, type, act_end),
	t(B, executes, LOOP),
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    
	
	t(B, type, act_end),
	t(B, executes, LOOP),
	t(B, after_act, A).
	t(B, type, normalLoopEnd):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    
	
	t(B, type, act_end),
	t(B, executes, LOOP),
	t(B, after_act, A).

% Rule: connect_LoopCond1-LoopEnd [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(B, type, act_end),
	t(B, executes, LOOP),
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(B, type, act_end),
	t(B, executes, LOOP),
	t(B, after_act, A).
	t(B, type, normalLoopEnd):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    
	
	t(B, type, act_end),
	t(B, executes, LOOP),
	t(B, after_act, A).

% Rule: connect_LoopBody-cond [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, body_then_cond), 
	t(LOOP, body, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, body_then_cond), 
	t(LOOP, body, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).
	t(B, type, loopCondBeginAfterIteration):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, body_then_cond), 
	t(LOOP, body, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).

% Rule: connect_LoopBegin-init [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(A, executes, LOOP),
	t(LOOP, type, loop_with_initialization), 

	t(LOOP, init, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(A, executes, LOOP),
	t(LOOP, type, loop_with_initialization), 

	t(LOOP, init, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).
	t(B, type, loopWithInitBegin):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_begin),
	t(A, executes, LOOP),
	t(LOOP, type, loop_with_initialization), 

	t(LOOP, init, ST),
	
	t(B, type, act_begin),
	t(B, executes, ST),
	
	t(B, after_act, A).

% Rule: connect_LoopInit-cond [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, loop_with_initialization), 
	t(LOOP, init, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, loop_with_initialization), 
	t(LOOP, init, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).
	t(B, type, loopCondBeginAfterInit):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, loop_with_initialization), 
	t(LOOP, init, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).

% Rule: connect_LoopBody-update [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, post_update_loop), 
	t(LOOP, body, ST),
	t(A, executes, ST),

	t(LOOP, update, UPD),
	t(B, type, act_begin),
	t(B, executes, UPD),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, post_update_loop), 
	t(LOOP, body, ST),
	t(A, executes, ST),

	t(LOOP, update, UPD),
	t(B, type, act_begin),
	t(B, executes, UPD),
	
	t(B, after_act, A).
	t(B, type, loopUpdateAfterIteration):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, post_update_loop), 
	t(LOOP, body, ST),
	t(A, executes, ST),

	t(LOOP, update, UPD),
	t(B, type, act_begin),
	t(B, executes, UPD),
	
	t(B, after_act, A).

% Rule: connect_LoopUpdate-cond [correct & loop]
	t(B, type, normal_flow_correct_act):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, post_update_loop), 
	t(LOOP, update, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).
	t(A, next_act, B):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, post_update_loop), 
	t(LOOP, update, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).
	t(B, type, loopCondAfterUpdate):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, post_update_loop), 
	t(LOOP, update, ST),
	t(A, executes, ST),

	t(LOOP, cond, CND),
	t(B, type, act_begin),
	t(B, executes, CND),
	
	t(B, after_act, A).

% Rule: CorrespondingActsMismatch_Error [mistake]
	t(B, type, correspondingEndMismatched):-
	t(A, student_corresponding_end, B), 
	t(A, executes, S1),
	t(B, executes, S2),
	                          
		t(S1, id, IB),
		t(S2, id, IC),
		IB != IC.
	t(B, cause, A):-
	t(A, student_corresponding_end, B), 
	t(A, executes, S1),
	t(B, executes, S2),
	                          
		t(S1, id, IB),
		t(S2, id, IC),
		IB != IC.

% Rule: GenericWrongAct_Error [mistake]
	t(C, should_be, B):-
	t(A, next_act, B),
	t(A, student_next, C),
	                        
		t(B, id, IB),
		t(C, id, IC),
		IB != IC.
	t(C, precursor, A):-
	t(A, next_act, B),
	t(A, student_next, C),
	                        
		t(B, id, IB),
		t(C, id, IC),
		IB != IC.
	t(C, type, erroneous):-
	t(A, next_act, B),
	t(A, student_next, C),
	                        
		t(B, id, IB),
		t(C, id, IC),
		IB != IC.

% Rule: GenericWrongParent_Error [mistake]
	t(A, context_should_be, P):-
	t(P, parent_of, A),
	t(C, student_parent_of, A),
	                        
		t(P, id, IP),
		t(C, id, IC),
		IP != IC.
	t(A, type, wrongContext):-
	t(P, parent_of, A),
	t(C, student_parent_of, A),
	                        
		t(P, id, IP),
		t(C, id, IC),
		IP != IC.

% Rule: MisplacedBefore_Error [mistake]
	t(A, type, misplacedBefore):-
	t(A, type, wrongContext),
	t(A, corresponding_end, E),
	t(P, parent_of, A),
	             
		t(E, student_index, IE),
		t(P, student_index, IP),
		IE < IP.
	t(E, type, misplacedBefore):-
	t(A, type, wrongContext),
	t(A, corresponding_end, E),
	t(P, parent_of, A),
	             
		t(E, student_index, IE),
		t(P, student_index, IP),
		IE < IP.

% Rule: MisplacedAfter_Error [mistake]
	t(A, type, misplacedAfter):-
	t(A, type, wrongContext),
	t(A, corresponding_end, E),
	t(P, parent_of, A),
	t(P, corresponding_end, PE),
	                    
		t(A, student_index, IA),
		t(PE, student_index, IPE),
		IPE < IA.
	t(E, type, misplacedAfter):-
	t(A, type, wrongContext),
	t(A, corresponding_end, E),
	t(P, parent_of, A),
	t(P, corresponding_end, PE),
	                    
		t(A, student_index, IA),
		t(PE, student_index, IPE),
		IPE < IA.

% Rule: MisplacedDeeper_Error [mistake]
	t(A, type, misplacedDeeper):-
	t(A, type, wrongContext),
	t(A, corresponding_end, E),
	t(P, parent_of, A),
	t(P, corresponding_end, PE),
	                  
		t(A, student_index, IA),
		t(P, student_index, IP),
		IP < IA,
		t(E, student_index, IE),
		t(PE, student_index, IPE),
		IE < IPE.
	t(E, type, misplacedDeeper):-
	t(A, type, wrongContext),
	t(A, corresponding_end, E),
	t(P, parent_of, A),
	t(P, corresponding_end, PE),
	                  
		t(A, student_index, IA),
		t(P, student_index, IP),
		IP < IA,
		t(E, student_index, IE),
		t(PE, student_index, IPE),
		IE < IPE.

% Rule: GenericWrongExecTime-b_Error [mistake]
	t(C, type, wrongExecTime):-
	t(C, type, erroneous),
	t(C, should_be, B),
	t(B, type, act_begin),
	t(C, type, act_begin),
	t(C, executes, ST),
	t(B, executes, ST),
	t(C, exec_time, N1),
	t(B, exec_time, N2),
	N1 != N2.

% Rule: GenericWrongExecTime-e_Error [mistake]
	t(C, type, wrongExecTime):-
	t(C, type, erroneous),
	t(C, should_be, B),
	t(B, type, act_end),
	t(C, type, act_end),
	t(C, executes, ST),
	t(B, executes, ST),
	t(C, exec_time, N1),
	t(B, exec_time, N2),
	N1 != N2.

% Rule: ActStartsAfterItsEnd_Error [mistake]
	t(A, cause, B):-
	t(A, in_trace, TR),
	t(B, in_trace, TR),
	t(A, type, act_begin),
	t(B, type, act_end),
	t(A, executes, ST),
	t(B, executes, ST),
	t(A, exec_time, N),
	t(B, exec_time, N),
	t(A, student_index, IA),
	t(B, student_index, IB),
	IB < IA.
	t(B, cause, A):-
	t(A, in_trace, TR),
	t(B, in_trace, TR),
	t(A, type, act_begin),
	t(B, type, act_end),
	t(A, executes, ST),
	t(B, executes, ST),
	t(A, exec_time, N),
	t(B, exec_time, N),
	t(A, student_index, IA),
	t(B, student_index, IB),
	IB < IA.
	t(A, type, actStartsAfterItsEnd):-
	t(A, in_trace, TR),
	t(B, in_trace, TR),
	t(A, type, act_begin),
	t(B, type, act_end),
	t(A, executes, ST),
	t(B, executes, ST),
	t(A, exec_time, N),
	t(B, exec_time, N),
	t(A, student_index, IA),
	t(B, student_index, IB),
	IB < IA.
	t(B, type, actEndsWithoutStart):-
	t(A, in_trace, TR),
	t(B, in_trace, TR),
	t(A, type, act_begin),
	t(B, type, act_end),
	t(A, executes, ST),
	t(B, executes, ST),
	t(A, exec_time, N),
	t(B, exec_time, N),
	t(A, student_index, IA),
	t(B, student_index, IB),
	IB < IA.

% Rule: DuplicateOfAct-seq-b_Error [mistake & sequence]
	t(C1, cause, C):-
	t(C1, type, extraAct), 
	t(C1, type, act_begin),
	t(P, student_parent_of, C1),
	t(P, executes, BLOCK),
	t(BLOCK, type, sequence),
	t(BLOCK, body_item, ST),
	t(C1, executes, ST),

	t(C, executes, ST),
	t(P, student_parent_of, C),
	t(C, type, act_begin),
		t(C1, id, IC1),
		t(C, id, IC),
		IC1 != IC.
	t(C1, type, duplicateOfAct):-
	t(C1, type, extraAct), 
	t(C1, type, act_begin),
	t(P, student_parent_of, C1),
	t(P, executes, BLOCK),
	t(BLOCK, type, sequence),
	t(BLOCK, body_item, ST),
	t(C1, executes, ST),

	t(C, executes, ST),
	t(P, student_parent_of, C),
	t(C, type, act_begin),
		t(C1, id, IC1),
		t(C, id, IC),
		IC1 != IC.

% Rule: DuplicateOfAct-seq-e_Error [mistake & sequence]
	t(C1, cause, C):-
	t(C1, type, extraAct), 
	t(C1, type, act_end),
	t(P, student_parent_of, C1),
	t(P, executes, BLOCK),
	t(BLOCK, type, sequence),
		t(BLOCK, body_item, ST),                                                                      
	t(C1, executes, ST),

	t(C, executes, ST),
	t(P, student_parent_of, C),
	t(C, type, act_end),

		t(C1, id, IC1),
		t(C, id, IC),
		IC1 != IC.
	t(C1, type, duplicateOfAct):-
	t(C1, type, extraAct), 
	t(C1, type, act_end),
	t(P, student_parent_of, C1),
	t(P, executes, BLOCK),
	t(BLOCK, type, sequence),
		t(BLOCK, body_item, ST),                                                                      
	t(C1, executes, ST),

	t(C, executes, ST),
	t(P, student_parent_of, C),
	t(C, type, act_end),

		t(C1, id, IC1),
		t(C, id, IC),
		IC1 != IC.

% Rule: DisplacedAct_Error [mistake & sequence]
	t(C1, type, displacedAct):-
	t(C1, type, extraAct), 
	t(C1, type, missingAct).

% Rule: TooEarlyInSequence_Error [mistake & sequence]
	t(B, should_be_after, A):-
	t(B, type, tooEarly), 
	t(SA, student_parent_of, B),
	t(SA, executes, SEQ),
	t(SEQ, type, sequence),
	t(A, should_be_before, B), 
	t(SA, student_parent_of, A).
	t(B, type, tooEarlyInSequence):-
	t(B, type, tooEarly), 
	t(SA, student_parent_of, B),
	t(SA, executes, SEQ),
	t(SEQ, type, sequence),
	t(A, should_be_before, B), 
	t(SA, student_parent_of, A).

% Rule: NoFirstCondition-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_begin),
	t(A, executes, ALT),
	t(ALT, type, alternative), 

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, act_begin),
	t(A, executes, ALT),
	t(ALT, type, alternative), 

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, noFirstCondition):-
	t(A, type, act_begin),
	t(A, executes, ALT),
	t(ALT, type, alternative), 

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: BranchOfFalseCondition-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(ALT_ACT, parent_of, A),                                                                                   
	t(ALT_ACT, student_parent_of, B),
	
	                       
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(ALT_ACT, parent_of, A),                                                                                   
	t(ALT_ACT, student_parent_of, B),
	
	                       
	t(B, type, erroneous).
	t(B, cause, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(ALT_ACT, parent_of, A),                                                                                   
	t(ALT_ACT, student_parent_of, B),
	
	                       
	t(B, type, erroneous).
	t(B, type, branchOfFalseCondition):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             
	
	t(B, type, act_begin),
	t(B, executes, BR),
	
	t(ALT_ACT, parent_of, A),                                                                                   
	t(ALT_ACT, student_parent_of, B),
	
	                       
	t(B, type, erroneous).

% Rule: WrongBranch-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_begin),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_begin),
	t(B, executes, BR2),
	t(ALT, branches_item, BR2),
	
	                        
		t(BR, id, I),
		t(BR2, id, I2),
		I != I2,
	
	t(ALT_ACT, parent_of, A),
	t(ALT_ACT, student_parent_of, B).
	t(B, precursor, A):-
	t(A, type, act_begin),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_begin),
	t(B, executes, BR2),
	t(ALT, branches_item, BR2),
	
	                        
		t(BR, id, I),
		t(BR2, id, I2),
		I != I2,
	
	t(ALT_ACT, parent_of, A),
	t(ALT_ACT, student_parent_of, B).
	t(B, type, wrongBranch):-
	t(A, type, act_begin),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_begin),
	t(B, executes, BR2),
	t(ALT, branches_item, BR2),
	
	                        
		t(BR, id, I),
		t(BR2, id, I2),
		I != I2,
	
	t(ALT_ACT, parent_of, A),
	t(ALT_ACT, student_parent_of, B).

% Rule: ConditionAfterBranch-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_end),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(A, student_next, B),
	t(B, type, extraAct), 	                                        
	                
	t(B, executes, CND),
	t(CND, type, expr).
	t(B, precursor, A):-
	t(A, type, act_end),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(A, student_next, B),
	t(B, type, extraAct), 	                                        
	                
	t(B, executes, CND),
	t(CND, type, expr).
	t(B, type, conditionAfterBranch):-
	t(A, type, act_end),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(A, student_next, B),
	t(B, type, extraAct), 	                                        
	                
	t(B, executes, CND),
	t(CND, type, expr).

% Rule: AnotherExtraBranch-alt_Error [alternative & mistake]
	t(B, cause, A):-
	t(A, type, act_begin),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_begin),
	t(B, executes, BR2),
	t(ALT, branches_item, BR2),
	
	t(ALT_ACT, student_parent_of, A),
	t(ALT_ACT, student_parent_of, B),
	
	t(A, student_index, SIA),
	t(B, student_index, SIB),
	SIB > SIA.
	t(B, type, anotherExtraBranch):-
	t(A, type, act_begin),
	t(A, executes, BR),
	t(ALT, branches_item, BR),
	t(ALT, type, alternative), 

	t(B, type, act_begin),
	t(B, executes, BR2),
	t(ALT, branches_item, BR2),
	
	t(ALT_ACT, student_parent_of, A),
	t(ALT_ACT, student_parent_of, B),
	
	t(A, student_index, SIA),
	t(B, student_index, SIB),
	SIB > SIA.

% Rule: NoBranchWhenConditionIsTrue-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, noBranchWhenConditionIsTrue):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(BR, cond, CND),                        
	t(BR, type, alt_branch),                             

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: AllFalseNoElse-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(BR, next, BR2),
	t(BR2, type, else), 	                          

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(BR, next, BR2),
	t(BR2, type, else), 	                          

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, allFalseNoElse):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(BR, next, BR2),
	t(BR2, type, else), 	                          

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: NoNextCondition-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(BR, next, BR2),
	t(BR2, cond, CND2), 	                               

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(BR, next, BR2),
	t(BR2, cond, CND2), 	                               

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, noNextCondition):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(BR, next, BR2),
	t(BR2, cond, CND2), 	                               

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: AllFalseNoEnd-alt_Error [alternative & mistake]
	t(B, should_be, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(ALT, branches_item, BR),
	t(ALT, type, alternative),
	t(BR, type, last_item),                                

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(ALT, branches_item, BR),
	t(ALT, type, alternative),
	t(BR, type, last_item),                                

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, allFalseNoEnd):-
	t(A, type, act_end),
	t(CND, type, expr), 
	t(A, executes, CND),

	t(A, expr_value, false),                    
	t(BR, cond, CND),                        
	t(ALT, branches_item, BR),
	t(ALT, type, alternative),
	t(BR, type, last_item),                                

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: MissingIterationAfterSuccessfulCondition-1-loop_Error [loop & mistake]
	t(B, should_be, A):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, missingIterationAfterSuccessfulCondition):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, true),                    

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: MissingIterationAfterSuccessfulCondition-0-loop_Error [loop & mistake]
	t(B, should_be, A):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, precursor, A):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, missingIterationAfterSuccessfulCondition):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, inverse_conditional_loop), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: MissingLoopEndAfterFailedCondition-0-loop_Error [loop & mistake]
	t(B, precursor, A):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(A, student_next, B),
	t(B, type, erroneous).
	t(B, type, missingLoopEndAfterFailedCondition):-
	t(A, type, normal_flow_correct_act),
	t(A, type, act_end),
	t(LOOP, type, cond_then_body), 
	t(LOOP, cond, CND),
	t(A, executes, CND),

	t(A, expr_value, false),                    

	t(A, student_next, B),
	t(B, type, erroneous).

% Rule: IterationAfterFailedCondition-loop_Error [loop & mistake]
	t(B, type, iterationAfterFailedCondition):-
	t(B, type, missingLoopEndAfterFailedCondition),
	t(B, type, act_begin),
	t(B, executes, ST),
	t(L, body, ST),
	t(L, type, loop).

% Rule: ExtraAct_1_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		
		t(C1, student_next, B).

% Rule: MissingAct_1_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		
		t(C1, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		
		t(C1, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		
		t(C1, next_act, B).

% Rule: ExtraAct_2_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), 
		t(C2, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), 
		t(C2, student_next, B).

% Rule: MissingAct_2_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), 
		t(C2, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), 
		t(C2, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), 
		t(C2, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), 
		t(C2, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), 
		t(C2, next_act, B).

% Rule: ExtraAct_3_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), 
		t(C3, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), 
		t(C3, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), 
		t(C3, student_next, B).

% Rule: MissingAct_3_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), 
		t(C3, next_act, B).

% Rule: ExtraAct_4_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), 
		t(C4, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), 
		t(C4, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), 
		t(C4, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), 
		t(C4, student_next, B).

% Rule: MissingAct_4_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), 
		t(C4, next_act, B).

% Rule: ExtraAct_5_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), 
		t(C5, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), 
		t(C5, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), 
		t(C5, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), 
		t(C5, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), 
		t(C5, student_next, B).

% Rule: MissingAct_5_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), 
		t(C5, next_act, B).

% Rule: ExtraAct_6_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), 
		t(C6, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), 
		t(C6, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), 
		t(C6, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), 
		t(C6, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), 
		t(C6, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), 
		t(C6, student_next, B).

% Rule: MissingAct_6_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), 
		t(C6, next_act, B).

% Rule: ExtraAct_7_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).
	t(C7, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), 
		t(C7, student_next, B).

% Rule: MissingAct_7_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C7, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(C7, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), 
		t(C7, next_act, B).

% Rule: ExtraAct_8_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C7, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).
	t(C8, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), 
		t(C8, student_next, B).

% Rule: MissingAct_8_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C7, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C7, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C8, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(C8, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), 
		t(C8, next_act, B).

% Rule: ExtraAct_9_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C7, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C8, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).
	t(C9, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), 
		t(C9, student_next, B).

% Rule: MissingAct_9_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C7, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C7, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C8, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C8, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C9, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(C9, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), 
		t(C9, next_act, B).

% Rule: ExtraAct_10_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C7, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C8, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C9, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).
	t(C10, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), 
		t(C10, student_next, B).

% Rule: MissingAct_10_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C7, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C7, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C8, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C8, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C9, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C9, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C10, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(C10, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), 
		t(C10, next_act, B).

% Rule: ExtraAct_11_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C7, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C8, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C9, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C10, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).
	t(C11, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), 
		t(C11, student_next, B).

% Rule: MissingAct_11_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C7, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C7, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C8, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C8, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C9, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C9, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C10, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C10, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C11, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(C11, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), 
		t(C11, next_act, B).

% Rule: ExtraAct_12_Error [mistake]
	t(C1, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C2, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C3, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C4, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C5, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C6, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C7, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C8, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C9, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C10, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C11, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).
	t(C12, type, extraAct):-
		t(A, next_act, B),
		t(A, student_next, C1),
		                         
		t(C1, student_next, C2), t(C2, student_next, C3), t(C3, student_next, C4), t(C4, student_next, C5), t(C5, student_next, C6), t(C6, student_next, C7), t(C7, student_next, C8), t(C8, student_next, C9), t(C9, student_next, C10), t(C10, student_next, C11), t(C11, student_next, C12), 
		t(C12, student_next, B).

% Rule: MissingAct_12_Error [mistake]
	t(C1, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C1, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C2, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C2, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C3, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C3, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C4, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C4, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C5, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C5, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C6, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C6, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C7, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C7, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C8, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C8, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C9, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C9, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C10, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C10, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C11, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C11, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C12, type, missingAct):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(C12, should_be_before, B):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).
	t(B, type, tooEarly):-
		t(A, student_next, B),
		t(A, next_act, C1),
		                         
		t(C1, next_act, C2), t(C2, next_act, C3), t(C3, next_act, C4), t(C4, next_act, C5), t(C5, next_act, C6), t(C6, next_act, C7), t(C7, next_act, C8), t(C8, next_act, C9), t(C9, next_act, C10), t(C10, next_act, C11), t(C11, next_act, C12), 
		t(C12, next_act, B).

% Rule: LoopIteration1_after_0 [correct & helper & loop]
	t(C0, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		 
		t(C0, executes, ST), t(C0, corresponding_end, CE0).
	t(CE0, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		 
		t(C0, executes, ST), t(C0, corresponding_end, CE0).

% Rule: LoopIteration1_after_1 [correct & helper & loop]
	t(C1, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		 
		t(C1, executes, ST), t(C1, corresponding_end, CE1).
	t(CE1, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		 
		t(C1, executes, ST), t(C1, corresponding_end, CE1).

% Rule: LoopIteration1_after_2 [correct & helper & loop]
	t(C2, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		
		t(C1, executes, ST1),
		t(ST1, id, ST1_I),
		ST1_I != BODY_I,
		t(C1, corresponding_end, CE1), 
		t(CE1, next_act, C2), 
		 
		t(C2, executes, ST), t(C2, corresponding_end, CE2).
	t(CE2, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		
		t(C1, executes, ST1),
		t(ST1, id, ST1_I),
		ST1_I != BODY_I,
		t(C1, corresponding_end, CE1), 
		t(CE1, next_act, C2), 
		 
		t(C2, executes, ST), t(C2, corresponding_end, CE2).

% Rule: LoopIteration1_after_3 [correct & helper & loop]
	t(C3, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		
		t(C1, executes, ST1),
		t(ST1, id, ST1_I),
		ST1_I != BODY_I,
		t(C1, corresponding_end, CE1), 
		t(CE1, next_act, C2), 
		
		t(C2, executes, ST2),
		t(ST2, id, ST2_I),
		ST2_I != BODY_I,
		t(C2, corresponding_end, CE2), 
		t(CE2, next_act, C3), 
		 
		t(C3, executes, ST), t(C3, corresponding_end, CE3).
	t(CE3, iteration_n, 1):-
		t(A, type, act_begin),
		t(A, executes, L),
		t(L, type, loop),
		t(L, body, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		
		t(C1, executes, ST1),
		t(ST1, id, ST1_I),
		ST1_I != BODY_I,
		t(C1, corresponding_end, CE1), 
		t(CE1, next_act, C2), 
		
		t(C2, executes, ST2),
		t(ST2, id, ST2_I),
		ST2_I != BODY_I,
		t(C2, corresponding_end, CE2), 
		t(CE2, next_act, C3), 
		 
		t(C3, executes, ST), t(C3, corresponding_end, CE3).

% Rule: LoopIterationNext_after_0 [correct & helper & loop]
	t(C0, iteration_n, N_NEXT):-
		t(A, type, act_end),
		t(A, iteration_n, N),
		t(A, executes, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		 
		t(C0, executes, ST), t(C0, corresponding_end, CE0),                       
		N_NEXT = N + 1.
	t(CE0, iteration_n, N_NEXT):-
		t(A, type, act_end),
		t(A, iteration_n, N),
		t(A, executes, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		 
		t(C0, executes, ST), t(C0, corresponding_end, CE0),                       
		N_NEXT = N + 1.

% Rule: LoopIterationNext_after_1 [correct & helper & loop]
	t(C1, iteration_n, N_NEXT):-
		t(A, type, act_end),
		t(A, iteration_n, N),
		t(A, executes, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		 
		t(C1, executes, ST), t(C1, corresponding_end, CE1),                       
		N_NEXT = N + 1.
	t(CE1, iteration_n, N_NEXT):-
		t(A, type, act_end),
		t(A, iteration_n, N),
		t(A, executes, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		 
		t(C1, executes, ST), t(C1, corresponding_end, CE1),                       
		N_NEXT = N + 1.

% Rule: LoopIterationNext_after_2 [correct & helper & loop]
	t(C2, iteration_n, N_NEXT):-
		t(A, type, act_end),
		t(A, iteration_n, N),
		t(A, executes, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		
		t(C1, executes, ST1),
		t(ST1, id, ST1_I),
		ST1_I != BODY_I,
		t(C1, corresponding_end, CE1), 
		t(CE1, next_act, C2), 
		 
		t(C2, executes, ST), t(C2, corresponding_end, CE2),                       
		N_NEXT = N + 1.
	t(CE2, iteration_n, N_NEXT):-
		t(A, type, act_end),
		t(A, iteration_n, N),
		t(A, executes, ST),
		t(ST, id, BODY_I),
		t(A, next_act, C0),
		
		t(C0, executes, ST0),
		t(ST0, id, ST0_I),
		ST0_I != BODY_I,
		t(C0, corresponding_end, CE0), 
		t(CE0, next_act, C1), 
		
		t(C1, executes, ST1),
		t(ST1, id, ST1_I),
		ST1_I != BODY_I,
		t(C1, corresponding_end, CE1), 
		t(CE1, next_act, C2), 
		 
		t(C2, executes, ST), t(C2, corresponding_end, CE2),                       
		N_NEXT = N + 1.
