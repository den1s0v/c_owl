
% Rule: Incr_index [correct & helper]
swrl_rule() :- 
	
	next_act(A, B), index(A, ^^(IA,_)), add(IB, IA, 1),
	% -> index(B, ^^(IB,_)),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%index', IB),
	fail.

% Rule: DepthIncr_rule_s6 [correct & helper]
swrl_rule() :- 
	
	act_begin(A), next_act(A, B), act_begin(B),
	% -> parent_of(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%parent_of', B),
	fail.

% Rule: student_DepthIncr_rule_s6 [mistake & helper]
swrl_rule() :- 
	
	act_begin(A), student_next(A, B), act_begin(B),
	% -> student_parent_of(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%student_parent_of', B),
	fail.

% Rule: DepthSame_b-e_rule_s7 [correct & helper]
swrl_rule() :- 
	
	act_begin(A), next_act(A, B), act_end(B), 
	parent_of(P, A),
	% -> parent_of(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%parent_of', B),
	% -> corresponding_end(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%corresponding_end', B),
	fail.

% Rule: student_DepthSame_b-e_rule_s7 [mistake & helper]
swrl_rule() :- 
	
	act_begin(A), student_next(A, B), act_end(B), 
	student_parent_of(P, A),
	% -> student_parent_of(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%student_parent_of', B),
	% -> student_corresponding_end(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%student_corresponding_end', B),
	fail.

% Rule: DepthSame_e-b_rule_s8 [correct & helper]
swrl_rule() :- 
	
	act_end(A), next_act(A, B), act_begin(B), 
	parent_of(P, A),
	% -> parent_of(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%parent_of', B),
	fail.

% Rule: student_DepthSame_e-b_rule_s8 [mistake & helper]
swrl_rule() :- 
	
	act_end(A), student_next(A, B), act_begin(B), 
	student_parent_of(P, A),
	% -> student_parent_of(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%student_parent_of', B),
	fail.

% Rule: DepthDecr_rule_s9 [correct & helper]
swrl_rule() :- 
	
	act_end(A), next_act(A, B), act_end(B), 
	parent_of(P, A),
	% -> corresponding_end(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%corresponding_end', B),
	fail.

% Rule: student_DepthDecr_rule_s9 [mistake & helper]
swrl_rule() :- 
	
	act_end(A), student_next(A, B), act_end(B), 
	student_parent_of(P, A),
	% -> student_corresponding_end(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%student_corresponding_end', B),
	fail.

% Rule: SameParentOfCorrActs_rule_s10 [correct & helper]
swrl_rule() :- 
	
	corresponding_end(A, B), parent_of(P, A),
	% -> parent_of(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%parent_of', B),
	fail.

% Rule: student_SameParentOfCorrActs_rule_s10 [mistake & helper]
swrl_rule() :- 
	
	corresponding_end(A, B), student_parent_of(P, A),
	% -> student_parent_of(P, B),
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%student_parent_of', B),
	fail.

% Rule: Earliest_after_act_is_previous_correct_sibling [correct & helper]
swrl_rule() :- 
	
	correct_act(A),
	next_sibling(A, S),
	% -> after_act(S, A),
	rdf_assert(S, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%after_act', A),
	fail.

% Rule: Propagate_after_act [correct & helper]
swrl_rule() :- 
	
	after_act(S, A),
	next_act(A, B),
	                        
		id(B, ^^(IB,_)),
		id(S, ^^(IS,_)),
		notEqual(IB, IS),
	% -> after_act(S, B),
	rdf_assert(S, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%after_act', B),
	fail.

% Rule: start__to__MainFunctionBegin__rule_g3 [correct & function & entry]
swrl_rule() :- 
	
	trace(A),
	executes(A, ALG),
	entry_point(ALG, FUNC_),
	func(FUNC_), 
	                                                                                                            
	act_begin(B),
		                                          
	next_sibling(A, B),              
	executes(B, FUNC_),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> functionBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%FunctionBegin'),
	fail.

% Rule: start__to__GlobalCode__rule_g4 [correct & sequence & entry]
swrl_rule() :- 
	
	trace(A),
	executes(A, ALG),
	entry_point(ALG, GC),
	sequence(GC), 

	act_begin(B),
		                                          
	next_sibling(A, B),              
	executes(B, GC),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> globalCodeBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%GlobalCodeBegin'),
	fail.

% Rule: connect_FunctionBodyBegin_rule_g5 [correct & function]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	func(FUNC_), 
	executes(A, FUNC_),
	body(FUNC_, ST),
	
	act_begin(B),
	executes(B, ST),
	                                                    
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> functionBodyBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%FunctionBodyBegin'),
	fail.

% Rule: connect_FuncBodyEnd_rule_g5-2 [correct & function]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	func(FUNC_), 
	body(FUNC_, ST),
	executes(A, ST),
	
	act_end(B),
	executes(B, FUNC_),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> functionEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%FunctionEnd'),
	fail.

% Rule: connect_SequenceBegin_rule_g2 [correct & sequence]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	sequence(BLOCK), 
	executes(A, BLOCK),
	body_item(BLOCK, ST),
	first_item(ST),
	
	act_begin(B),
	executes(B, ST),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> sequenceBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%SequenceBegin'),
	fail.

% Rule: connect_SequenceNext [correct & sequence]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	parent_of(P, A),
	sequence(BLOCK), 
	executes(P, BLOCK),
	body_item(BLOCK, ST),
	executes(A, ST),
	
	next(ST, ST2),
	
	act_begin(B),
	executes(B, ST2),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> sequenceNext(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%SequenceNext'),
	fail.

% Rule: connect_StmtEnd [correct & sequence]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	stmt(ST), 
	executes(A, ST),
	
	act_end(B),
	executes(B, ST),
	
	after_act(B, A),
	
	exec_time(A, ^^(T,_)), exec_time(B, ^^(tmp_T,_)),
	equal(T, tmp_T),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> stmtEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%StmtEnd'),
	fail.

% Rule: connect_ExprEnd [correct & sequence]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	expr(ST), 
	executes(A, ST),
	
	act_end(B),
	executes(B, ST),
	
	after_act(B, A),

	exec_time(A, ^^(T,_)), exec_time(B, ^^(tmp_T,_)),
	equal(T, tmp_T),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> exprEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExprEnd'),
	fail.

% Rule: connect_SequenceEnd [correct & sequence]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	executes(A, ST),
	last_item(ST),
	
	act_end(B),
	parent_of(P, A),
	executes(P, BLOCK),
                            
	executes(B, BLOCK),
	body_item(BLOCK, ST),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> sequenceEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%SequenceEnd'),
	fail.

% Rule: connect_AltBegin [correct & alternative]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	alternative(ALT), 
	executes(A, ALT),

	branches_item(ALT, BR),
	first_item(BR),	                             
	                                          
	cond(BR, CND),
	
	act_begin(B),
	executes(B, CND),        
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> altBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AltBegin'),
	fail.

% Rule: connect_AltBranchBegin_CondTrue [correct & alternative]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, true),                    

	cond(BR, CND),
	alt_branch(BR),                             
	
	act_begin(B),
	executes(B, BR),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> altBranchBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AltBranchBegin'),
	fail.

% Rule: connect_NextAltCondition [correct & alternative]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    

	cond(BR, CND),
	alt_branch(BR),                             

	next(BR, BR2),
	cond(BR2, CND2),
	
	act_begin(B),
	executes(B, CND2),        
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> nextAltCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%NextAltCondition'),
	fail.

% Rule: connect_AltElseBranch [correct & alternative]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    

	cond(BR, CND),
	alt_branch(BR),                             
	next(BR, BR2),
	else(BR2),
	
	act_begin(B),
	executes(B, BR2),        

	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> altElseBranchBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AltElseBranchBegin'),
	fail.

% Rule: connect_AltEndAllFalse [correct & alternative]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    

	cond(BR, CND),
	alt_branch(BR),                             
	branches_item(ALT, BR),
	last_item(BR),                                      
	alternative(ALT),
	
	act_end(B),
	executes(B, ALT),        

	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> altEndAllFalse(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AltEndAllFalse'),
	fail.

% Rule: connect_AltEndAfterBranch [correct & alternative]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	executes(A, BR),
	branches_item(ALT, BR),
	alternative(ALT), 

	act_end(B),
	executes(B, ALT),                          
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> altEndAfterBranch(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AltEndAfterBranch'),
	fail.

% Rule: connect_LoopBegin-cond [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	pre_conditional_loop(LOOP), 
	executes(A, LOOP),

	cond(LOOP, CND),
	
	act_begin(B),
	executes(B, CND),        
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> preCondLoopBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%PreCondLoopBegin'),
	fail.

% Rule: connect_LoopBegin-body [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	post_conditional_loop(LOOP), 
	executes(A, LOOP),

	body(LOOP, ST),
	
	act_begin(B),
	executes(B, ST),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> postCondLoopBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%PostCondLoopBegin'),
	fail.

% Rule: connect_LoopCond1-BodyBegin [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	cond_then_body(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, true),                    
	
	body(LOOP, ST),
	                        
	                  
	
	act_begin(B),
	executes(B, ST),
								                           
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> iterationBeginOnTrueCond(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%IterationBeginOnTrueCond'),
	fail.

% Rule: connect_LoopCond0-body [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	inverse_conditional_loop(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, false),                    
	
	body(LOOP, ST),
	                        
	                  
	
	act_begin(B),
	executes(B, ST),
								                           
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> iterationBeginOnFalseCond(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%IterationBeginOnFalseCond'),
	fail.

% Rule: connect_LoopCond1-update [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	pre_update_loop(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, true),                    
	
	update(LOOP, UPD),
	act_begin(B),
	executes(B, UPD),
								                           
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopUpdateOnTrueCond(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopUpdateOnTrueCond'),
	fail.

% Rule: connect_LoopUpdate-body [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	pre_update_loop(LOOP), 
	update(LOOP, UPD),
	executes(A, UPD),

	body(LOOP, ST),
	act_begin(B),
	executes(B, ST),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopBodyAfterUpdate(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopBodyAfterUpdate'),
	fail.

% Rule: connect_LoopCond0-LoopEnd [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	conditional_loop(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, false),                    
	
	act_end(B),
	executes(B, LOOP),
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> normalLoopEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%NormalLoopEnd'),
	fail.

% Rule: connect_LoopCond1-LoopEnd [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	inverse_conditional_loop(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, true),                    
	
	act_end(B),
	executes(B, LOOP),
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> normalLoopEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%NormalLoopEnd'),
	fail.

% Rule: connect_LoopBody-cond [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	body_then_cond(LOOP), 
	body(LOOP, ST),
	executes(A, ST),

	cond(LOOP, CND),
	act_begin(B),
	executes(B, CND),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopCondBeginAfterIteration(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopCondBeginAfterIteration'),
	fail.

% Rule: connect_LoopBegin-init [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_begin(A),
	executes(A, LOOP),
	loop_with_initialization(LOOP), 

	init(LOOP, ST),
	
	act_begin(B),
	executes(B, ST),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopWithInitBegin(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopWithInitBegin'),
	fail.

% Rule: connect_LoopInit-cond [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	loop_with_initialization(LOOP), 
	init(LOOP, ST),
	executes(A, ST),

	cond(LOOP, CND),
	act_begin(B),
	executes(B, CND),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopCondBeginAfterInit(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopCondBeginAfterInit'),
	fail.

% Rule: connect_LoopBody-update [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	post_update_loop(LOOP), 
	body(LOOP, ST),
	executes(A, ST),

	update(LOOP, UPD),
	act_begin(B),
	executes(B, UPD),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopUpdateAfterIteration(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopUpdateAfterIteration'),
	fail.

% Rule: connect_LoopUpdate-cond [correct & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	post_update_loop(LOOP), 
	update(LOOP, ST),
	executes(A, ST),

	cond(LOOP, CND),
	act_begin(B),
	executes(B, CND),
	
	after_act(B, A),
	% -> normal_flow_correct_act(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%normal_flow_correct_act'),
	% -> next_act(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%next_act', B),
	% -> loopCondAfterUpdate(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%LoopCondAfterUpdate'),
	fail.

% Rule: CorrespondingActsMismatch_Error [mistake]
swrl_rule() :- 
	
	student_corresponding_end(A, B), 
	executes(A, S1),
	executes(B, S2),
	                          
		id(S1, ^^(IB,_)),
		id(S2, ^^(IC,_)),
		notEqual(IB, IC),
	% -> correspondingEndMismatched(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%CorrespondingEndMismatched'),
	% -> cause(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', A),
	fail.

% Rule: GenericWrongAct_Error [mistake]
swrl_rule() :- 
	
	next_act(A, B),
	student_next(A, C),
	                        
		id(B, ^^(IB,_)),
		id(C, ^^(IC,_)),
		notEqual(IB, IC),
	% -> should_be(C, B),
	rdf_assert(C, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', B),
	% -> precursor(C, A),
	rdf_assert(C, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> erroneous(C),
	rdf_assert(C, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%Erroneous'),
	fail.

% Rule: GenericWrongParent_Error [mistake]
swrl_rule() :- 
	
	parent_of(P, A),
	student_parent_of(C, A),
	                        
		id(P, ^^(IP,_)),
		id(C, ^^(IC,_)),
		notEqual(IP, IC),
	% -> context_should_be(A, P),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%context_should_be', P),
	% -> wrongContext(A),
	rdf_assert(A, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%WrongContext'),
	fail.

% Rule: MisplacedBefore_Error [mistake]
swrl_rule() :- 
	
	wrongContext(A),
	corresponding_end(A, E),
	parent_of(P, A),
	             
		student_index(E, ^^(IE,_)),
		student_index(P, ^^(IP,_)),
		lessThan(IE, IP),
	% -> misplacedBefore(A),
	rdf_assert(A, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MisplacedBefore'),
	% -> misplacedBefore(E),
	rdf_assert(E, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MisplacedBefore'),
	fail.

% Rule: MisplacedAfter_Error [mistake]
swrl_rule() :- 
	
	wrongContext(A),
	corresponding_end(A, E),
	parent_of(P, A),
	corresponding_end(P, PE),
	                    
		student_index(A, ^^(IA,_)),
		student_index(PE, ^^(IPE,_)),
		lessThan(IPE, IA),
	% -> misplacedAfter(A),
	rdf_assert(A, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MisplacedAfter'),
	% -> misplacedAfter(E),
	rdf_assert(E, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MisplacedAfter'),
	fail.

% Rule: MisplacedDeeper_Error [mistake]
swrl_rule() :- 
	
	wrongContext(A),
	corresponding_end(A, E),
	parent_of(P, A),
	corresponding_end(P, PE),
	                  
		student_index(A, ^^(IA,_)),
		student_index(P, ^^(IP,_)),
		lessThan(IP, IA),
		student_index(E, ^^(IE,_)),
		student_index(PE, ^^(IPE,_)),
		lessThan(IE, IPE),
	% -> misplacedDeeper(A),
	rdf_assert(A, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MisplacedDeeper'),
	% -> misplacedDeeper(E),
	rdf_assert(E, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MisplacedDeeper'),
	fail.

% Rule: GenericWrongExecTime-b_Error [mistake]
swrl_rule() :- 
	
	erroneous(C),
	should_be(C, B),
	act_begin(B),
	act_begin(C),
	executes(C, ST),
	executes(B, ST),
	exec_time(C, ^^(N1,_)),
	exec_time(B, ^^(N2,_)),
	notEqual(N1, N2),
	% -> wrongExecTime(C),
	rdf_assert(C, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%WrongExecTime'),
	fail.

% Rule: GenericWrongExecTime-e_Error [mistake]
swrl_rule() :- 
	
	erroneous(C),
	should_be(C, B),
	act_end(B),
	act_end(C),
	executes(C, ST),
	executes(B, ST),
	exec_time(C, ^^(N1,_)),
	exec_time(B, ^^(N2,_)),
	notEqual(N1, N2),
	% -> wrongExecTime(C),
	rdf_assert(C, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%WrongExecTime'),
	fail.

% Rule: ActStartsAfterItsEnd_Error [mistake]
swrl_rule() :- 
	
	act_begin(A),
	act_end(B),
	executes(A, ST),
	executes(B, ST),
	exec_time(A, ^^(N,_)),
	exec_time(B, ^^(N,_)),
	student_index(A, ^^(IA,_)),
	student_index(B, ^^(IB,_)),
	lessThan(IB, IA),
	% -> cause(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', B),
	% -> cause(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', A),
	% -> actStartsAfterItsEnd(A),
	rdf_assert(A, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ActStartsAfterItsEnd'),
	% -> actEndsWithoutStart(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ActEndsWithoutStart'),
	fail.

% Rule: DuplicateOfAct-seq-b_Error [mistake & sequence]
swrl_rule() :- 
	
	extraAct(C1), 
	act_begin(C1),
	student_parent_of(P, C1),
	executes(P, BLOCK),
	sequence(BLOCK),
		body_item(BLOCK, ST),                                                                      
	executes(C1, ST),

	executes(C, ST),
	student_parent_of(P, C),
	act_begin(C),

		id(C1, ^^(IC1,_)),
		id(C, ^^(IC,_)),
		notEqual(IC1, IC),
	% -> cause(C1, C),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', C),
	% -> duplicateOfAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%DuplicateOfAct'),
	fail.

% Rule: DuplicateOfAct-seq-e_Error [mistake & sequence]
swrl_rule() :- 
	
	extraAct(C1), 
	act_end(C1),
	student_parent_of(P, C1),
	executes(P, BLOCK),
	sequence(BLOCK),
		body_item(BLOCK, ST),                                                                      
	executes(C1, ST),

	executes(C, ST),
	student_parent_of(P, C),
	act_end(C),

		id(C1, ^^(IC1,_)),
		id(C, ^^(IC,_)),
		notEqual(IC1, IC),
	% -> cause(C1, C),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', C),
	% -> duplicateOfAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%DuplicateOfAct'),
	fail.

% Rule: DisplacedAct_Error [mistake & sequence]
swrl_rule() :- 
	
	extraAct(C1), 
	missingAct(C1),
	% -> displacedAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%DisplacedAct'),
	fail.

% Rule: TooEarlyInSequence_Error [mistake & sequence]
swrl_rule() :- 
	
	tooEarly(B), 
	student_parent_of(SA, B),
	executes(SA, SEQ),
	sequence(SEQ),
	should_be_before(A, B), 
	student_parent_of(SA, A),
	% -> should_be_after(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_after', A),
	% -> tooEarlyInSequence(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarlyInSequence'),
	fail.

% Rule: NoFirstCondition-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_begin(A),
	executes(A, ALT),
	alternative(ALT), 

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> noFirstCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%NoFirstCondition'),
	fail.

% Rule: BranchOfFalseCondition-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    

	cond(BR, CND),                        
	alt_branch(BR),                             
	
	act_begin(B),
	executes(B, BR),
	
	parent_of(ALT_ACT, A),                                                                                   
	student_parent_of(ALT_ACT, B),
	
	                       
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> cause(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', A),
	% -> branchOfFalseCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%BranchOfFalseCondition'),
	fail.

% Rule: WrongBranch-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_begin(A),
	executes(A, BR),
	branches_item(ALT, BR),
	alternative(ALT), 

	act_begin(B),
	executes(B, BR2),
	branches_item(ALT, BR2),
	
	                        
		id(BR, ^^(I,_)),
		id(BR2, ^^(I2,_)),
		notEqual(I, I2),
	
	parent_of(ALT_ACT, A),
	student_parent_of(ALT_ACT, B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> wrongBranch(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%WrongBranch'),
	fail.

% Rule: ConditionAfterBranch-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_end(A),
	executes(A, BR),
	branches_item(ALT, BR),
	alternative(ALT), 

	student_next(A, B),
	extraAct(B), 	                                        
	                
	executes(B, CND),
	expr(CND),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> conditionAfterBranch(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ConditionAfterBranch'),
	fail.

% Rule: AnotherExtraBranch-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_begin(A),
	executes(A, BR),
	branches_item(ALT, BR),
	alternative(ALT), 

	act_begin(B),
	executes(B, BR2),
	branches_item(ALT, BR2),
	
	student_parent_of(ALT_ACT, A),
	student_parent_of(ALT_ACT, B),
	
	student_index(A, ^^(SIA,_)),
	student_index(B, ^^(SIB,_)),
	greaterThan(SIB, SIA),
	% -> cause(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%cause', A),
	% -> anotherExtraBranch(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AnotherExtraBranch'),
	fail.

% Rule: NoBranchWhenConditionIsTrue-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, true),                    

	cond(BR, CND),                        
	alt_branch(BR),                             

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> noBranchWhenConditionIsTrue(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%NoBranchWhenConditionIsTrue'),
	fail.

% Rule: AllFalseNoElse-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    
	cond(BR, CND),                        
	next(BR, BR2),
	else(BR2), 	                          

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> allFalseNoElse(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AllFalseNoElse'),
	fail.

% Rule: NoNextCondition-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    
	cond(BR, CND),                        
	next(BR, BR2),
	cond(BR2, CND2), 	                               

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> noNextCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%NoNextCondition'),
	fail.

% Rule: AllFalseNoEnd-alt_Error [alternative & mistake]
swrl_rule() :- 
	
	act_end(A),
	expr(CND), 
	executes(A, CND),

	expr_value(A, false),                    
	cond(BR, CND),                        
	last_item(BR),                                

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> allFalseNoEnd(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%AllFalseNoEnd'),
	fail.

% Rule: MissingIterationAfterSuccessfulCondition-1-loop_Error [mistake & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	cond_then_body(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, true),                    

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> missingIterationAfterSuccessfulCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingIterationAfterSuccessfulCondition'),
	fail.

% Rule: MissingIterationAfterSuccessfulCondition-0-loop_Error [mistake & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	inverse_conditional_loop(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, false),                    

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> missingIterationAfterSuccessfulCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingIterationAfterSuccessfulCondition'),
	fail.

% Rule: MissingLoopEndAfterFailedCondition-0-loop_Error [mistake & loop]
swrl_rule() :- 
	
	normal_flow_correct_act(A),
	act_end(A),
	cond_then_body(LOOP), 
	cond(LOOP, CND),
	executes(A, CND),

	expr_value(A, false),                    

	student_next(A, B),
	erroneous(B),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> missingLoopEndAfterFailedCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingLoopEndAfterFailedCondition'),
	fail.

% Rule: IterationAfterFailedCondition-loop_Error [mistake & loop]
swrl_rule() :- 
	
	missingLoopEndAfterFailedCondition(B),
	act_begin(B),
	executes(B, ST),
	body(L, ST),
	loop(L),
	% -> should_be(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be', A),
	% -> precursor(B, A),
	rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%precursor', A),
	% -> iterationAfterFailedCondition(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%IterationAfterFailedCondition'),
	fail.

% Rule: ExtraAct_1_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		
		student_next(C1, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_1_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		
		next_act(C1, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_2_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), 
		student_next(C2, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_2_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), 
		next_act(C2, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_3_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), 
		student_next(C3, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_3_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), 
		next_act(C3, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_4_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), 
		student_next(C4, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_4_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), 
		next_act(C4, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_5_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), 
		student_next(C5, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_5_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), 
		next_act(C5, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_6_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), 
		student_next(C6, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_6_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), 
		next_act(C6, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_7_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), student_next(C6, C7), 
		student_next(C7, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_7_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), next_act(C6, C7), 
		next_act(C7, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C7, B),
	rdf_assert(C7, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_8_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), student_next(C6, C7), student_next(C7, C8), 
		student_next(C8, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_8_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), next_act(C6, C7), next_act(C7, C8), 
		next_act(C8, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C7, B),
	rdf_assert(C7, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C8, B),
	rdf_assert(C8, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_9_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), student_next(C6, C7), student_next(C7, C8), student_next(C8, C9), 
		student_next(C9, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_9_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), next_act(C6, C7), next_act(C7, C8), next_act(C8, C9), 
		next_act(C9, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C7, B),
	rdf_assert(C7, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C8, B),
	rdf_assert(C8, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C9, B),
	rdf_assert(C9, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_10_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), student_next(C6, C7), student_next(C7, C8), student_next(C8, C9), student_next(C9, C10), 
		student_next(C10, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C10),
	rdf_assert(C10, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_10_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), next_act(C6, C7), next_act(C7, C8), next_act(C8, C9), next_act(C9, C10), 
		next_act(C10, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C7, B),
	rdf_assert(C7, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C8, B),
	rdf_assert(C8, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C9, B),
	rdf_assert(C9, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C10),
	rdf_assert(C10, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C10, B),
	rdf_assert(C10, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_11_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), student_next(C6, C7), student_next(C7, C8), student_next(C8, C9), student_next(C9, C10), student_next(C10, C11), 
		student_next(C11, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C10),
	rdf_assert(C10, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C11),
	rdf_assert(C11, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_11_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), next_act(C6, C7), next_act(C7, C8), next_act(C8, C9), next_act(C9, C10), next_act(C10, C11), 
		next_act(C11, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C7, B),
	rdf_assert(C7, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C8, B),
	rdf_assert(C8, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C9, B),
	rdf_assert(C9, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C10),
	rdf_assert(C10, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C10, B),
	rdf_assert(C10, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C11),
	rdf_assert(C11, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C11, B),
	rdf_assert(C11, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: ExtraAct_12_Error [mistake]
swrl_rule() :- 
	
		next_act(A, B),
		student_next(A, C1),
		                         
		student_next(C1, C2), student_next(C2, C3), student_next(C3, C4), student_next(C4, C5), student_next(C5, C6), student_next(C6, C7), student_next(C7, C8), student_next(C8, C9), student_next(C9, C10), student_next(C10, C11), student_next(C11, C12), 
		student_next(C12, B),
	% -> extraAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C10),
	rdf_assert(C10, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C11),
	rdf_assert(C11, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	% -> extraAct(C12),
	rdf_assert(C12, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%ExtraAct'),
	fail.

% Rule: MissingAct_12_Error [mistake]
swrl_rule() :- 
	
		student_next(A, B),
		next_act(A, C1),
		                         
		next_act(C1, C2), next_act(C2, C3), next_act(C3, C4), next_act(C4, C5), next_act(C5, C6), next_act(C6, C7), next_act(C7, C8), next_act(C8, C9), next_act(C9, C10), next_act(C10, C11), next_act(C11, C12), 
		next_act(C12, B),
	% -> missingAct(C1),
	rdf_assert(C1, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C1, B),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C2),
	rdf_assert(C2, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C2, B),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C3),
	rdf_assert(C3, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C3, B),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C4),
	rdf_assert(C4, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C4, B),
	rdf_assert(C4, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C5),
	rdf_assert(C5, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C5, B),
	rdf_assert(C5, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C6),
	rdf_assert(C6, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C6, B),
	rdf_assert(C6, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C7),
	rdf_assert(C7, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C7, B),
	rdf_assert(C7, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C8),
	rdf_assert(C8, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C8, B),
	rdf_assert(C8, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C9),
	rdf_assert(C9, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C9, B),
	rdf_assert(C9, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C10),
	rdf_assert(C10, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C10, B),
	rdf_assert(C10, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C11),
	rdf_assert(C11, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C11, B),
	rdf_assert(C11, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> missingAct(C12),
	rdf_assert(C12, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%MissingAct'),
	% -> should_be_before(C12, B),
	rdf_assert(C12, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%should_be_before', B),
	% -> tooEarly(B),
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns%type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%TooEarly'),
	fail.

% Rule: LoopIteration1_after_0 [correct & helper & loop]
swrl_rule() :- 
	
		act_begin(A),
		executes(A, L),
		loop(L),
		body(L, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		 
		executes(C0, ST), corresponding_end(C0, CE0),
	% -> iteration_n(C0, 1),
	rdf_assert(C0, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	% -> iteration_n(CE0, 1),
	rdf_assert(CE0, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	fail.

% Rule: LoopIteration1_after_1 [correct & helper & loop]
swrl_rule() :- 
	
		act_begin(A),
		executes(A, L),
		loop(L),
		body(L, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		
		executes(C0, ST0),
		id(ST0, ^^(ST0_I,_)),
		notEqual(ST0_I, BODY_I),
		corresponding_end(C0, CE0), 
		next_act(CE0, C1), 
		 
		executes(C1, ST), corresponding_end(C1, CE1),
	% -> iteration_n(C1, 1),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	% -> iteration_n(CE1, 1),
	rdf_assert(CE1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	fail.

% Rule: LoopIteration1_after_2 [correct & helper & loop]
swrl_rule() :- 
	
		act_begin(A),
		executes(A, L),
		loop(L),
		body(L, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		
		executes(C0, ST0),
		id(ST0, ^^(ST0_I,_)),
		notEqual(ST0_I, BODY_I),
		corresponding_end(C0, CE0), 
		next_act(CE0, C1), 
		
		executes(C1, ST1),
		id(ST1, ^^(ST1_I,_)),
		notEqual(ST1_I, BODY_I),
		corresponding_end(C1, CE1), 
		next_act(CE1, C2), 
		 
		executes(C2, ST), corresponding_end(C2, CE2),
	% -> iteration_n(C2, 1),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	% -> iteration_n(CE2, 1),
	rdf_assert(CE2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	fail.

% Rule: LoopIteration1_after_3 [correct & helper & loop]
swrl_rule() :- 
	
		act_begin(A),
		executes(A, L),
		loop(L),
		body(L, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		
		executes(C0, ST0),
		id(ST0, ^^(ST0_I,_)),
		notEqual(ST0_I, BODY_I),
		corresponding_end(C0, CE0), 
		next_act(CE0, C1), 
		
		executes(C1, ST1),
		id(ST1, ^^(ST1_I,_)),
		notEqual(ST1_I, BODY_I),
		corresponding_end(C1, CE1), 
		next_act(CE1, C2), 
		
		executes(C2, ST2),
		id(ST2, ^^(ST2_I,_)),
		notEqual(ST2_I, BODY_I),
		corresponding_end(C2, CE2), 
		next_act(CE2, C3), 
		 
		executes(C3, ST), corresponding_end(C3, CE3),
	% -> iteration_n(C3, 1),
	rdf_assert(C3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	% -> iteration_n(CE3, 1),
	rdf_assert(CE3, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', 1),
	fail.

% Rule: LoopIterationNext_after_0 [correct & helper & loop]
swrl_rule() :- 
	
		act_end(A),
		iteration_n(A, N),
		executes(A, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		 
		executes(C0, ST), corresponding_end(C0, CE0),                       
		add(N_NEXT, N, 1),
	% -> iteration_n(C0, N_NEXT),
	rdf_assert(C0, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', N_NEXT),
	% -> iteration_n(CE0, N_NEXT),
	rdf_assert(CE0, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', N_NEXT),
	fail.

% Rule: LoopIterationNext_after_1 [correct & helper & loop]
swrl_rule() :- 
	
		act_end(A),
		iteration_n(A, N),
		executes(A, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		
		executes(C0, ST0),
		id(ST0, ^^(ST0_I,_)),
		notEqual(ST0_I, BODY_I),
		corresponding_end(C0, CE0), 
		next_act(CE0, C1), 
		 
		executes(C1, ST), corresponding_end(C1, CE1),                       
		add(N_NEXT, N, 1),
	% -> iteration_n(C1, N_NEXT),
	rdf_assert(C1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', N_NEXT),
	% -> iteration_n(CE1, N_NEXT),
	rdf_assert(CE1, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', N_NEXT),
	fail.

% Rule: LoopIterationNext_after_2 [correct & helper & loop]
swrl_rule() :- 
	
		act_end(A),
		iteration_n(A, N),
		executes(A, ST),
		id(ST, ^^(BODY_I,_)),
		next_act(A, C0),
		
		executes(C0, ST0),
		id(ST0, ^^(ST0_I,_)),
		notEqual(ST0_I, BODY_I),
		corresponding_end(C0, CE0), 
		next_act(CE0, C1), 
		
		executes(C1, ST1),
		id(ST1, ^^(ST1_I,_)),
		notEqual(ST1_I, BODY_I),
		corresponding_end(C1, CE1), 
		next_act(CE1, C2), 
		 
		executes(C2, ST), corresponding_end(C2, CE2),                       
		add(N_NEXT, N, 1),
	% -> iteration_n(C2, N_NEXT),
	rdf_assert(C2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', N_NEXT),
	% -> iteration_n(CE2, N_NEXT),
	rdf_assert(CE2, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1%iteration_n', N_NEXT),
	fail.
