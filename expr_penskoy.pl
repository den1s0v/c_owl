
% Rule: in_complex_begin []
swrl_rule() :- 
	next_index(A, ^^(B,_)), complex_beginning(A, true), complex_ending(B, false), step(A, ^^(0,_)),
	rdf_assert(B, 'http://penskoy.n/expressions#in_complex', A),
	fail.

% Rule: prev_operand_unary_postfix []
swrl_rule() :- 
	prev_index(A, ^^(B,_)), arity(B, "unary"), prefix_postfix(B, "postfix"), step(B, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#prev_operand', B),
	fail.

% Rule: copy_without_marks_associativity []
swrl_rule() :- 
	associativity(A, A_ASSOCIATIVITY), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#associativity', A_ASSOCIATIVITY),
	fail.

% Rule: prev_operation_beggining []
swrl_rule() :- 
	step(A, ^^(1,_)), index(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#prev_operation', A),
	fail.

% Rule: copy_without_marks_complex_beginning []
swrl_rule() :- 
	complex_beginning(A, B), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#complex_beginning', B),
	fail.

% Rule: copy_without_marks_complex_boundaries []
swrl_rule() :- 
	same_step(C, TO), copy_without_marks(A, TO), complex_boundaries(A, B), zero_step(C, B0), zero_step(B, B0),
	rdf_assert(TO, 'http://penskoy.n/expressions#complex_boundaries', C),
	fail.

% Rule: prev_operation []
swrl_rule() :- 
	prev_index(A, ^^(B,_)), arity(B, B_ARITY), notEqual(B_ARITY, "unary"), step(B, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#prev_operation', B),
	fail.

% Rule: copy_without_marks_complex_ending []
swrl_rule() :- 
	complex_ending(A, B), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#complex_ending', B),
	fail.

% Rule: prev_operation_unary_prefix []
swrl_rule() :- 
	prev_index(A, ^^(B,_)), arity(B, "unary"), prefix_postfix(B, "prefix"), step(B, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#prev_operation', B),
	fail.

% Rule: copy_without_marks_in_complex []
swrl_rule() :- 
	same_step(C, TO), copy_without_marks(A, TO), in_complex(A, B), zero_step(C, B0), zero_step(B, B0),
	rdf_assert(TO, 'http://penskoy.n/expressions#in_complex', C),
	fail.

% Rule: copy_without_marks_is_function_call []
swrl_rule() :- 
	is_function_call(A, A_FC), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#is_function_call', A_FC),
	fail.

% Rule: same_step []
swrl_rule() :- 
	step(A, ^^(A_STEP,_)), step(B, ^^(A_STEP,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#same_step', B),
	fail.

% Rule: copy_without_marks_is_operand []
swrl_rule() :- 
	copy_without_marks(A, TO), is_operand(A, IS_OP),
	rdf_assert(TO, 'http://penskoy.n/expressions#is_operand', IS_OP),
	fail.

% Rule: copy_without_marks_is_operator_with_strict_operands_order []
swrl_rule() :- 
	copy_without_marks(A, TO), is_operator_with_strict_operands_order(A, IS_OP),
	rdf_assert(TO, 'http://penskoy.n/expressions#is_operator_with_strict_operands_order', IS_OP),
	fail.

% Rule: copy_without_marks_last []
swrl_rule() :- 
	last(A, A_LAST), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#last', A_LAST),
	fail.

% Rule: copy_without_marks_prefix_postfix []
swrl_rule() :- 
	prefix_postfix(A, A_PR), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#prefix_postfix', A_PR),
	fail.

% Rule: copy_without_marks_priority []
swrl_rule() :- 
	precedence(A, ^^(A_PRIORITY,_)), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#precedence', A_PRIORITY),
	fail.

% Rule: copy_without_marks_real_pos []
swrl_rule() :- 
	real_pos(A, A_RP), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#real_pos', A_RP),
	fail.

% Rule: all_app_to_left []
swrl_rule() :- 
	all_app_to_left(A, B), prev_index(B, ^^(C,_)), app(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_app_to_left', C),
	fail.

% Rule: copy_without_marks_student_pos []
swrl_rule() :- 
	copy_without_marks(A, TO), student_pos(A, A_SP),
	rdf_assert(TO, 'http://penskoy.n/expressions#student_pos', A_SP),
	fail.

% Rule: copy_without_marks_text []
swrl_rule() :- 
	copy_without_marks(A, TO), text(A, ^^(A_TEXT,_)),
	rdf_assert(TO, 'http://penskoy.n/expressions#text', A_TEXT),
	fail.

% Rule: equal_priority_L_assoc []
swrl_rule() :- 
	equal(A_PRIOR, B_PRIOR), equal(A_ASSOC, B_ASSOC), index(B, ^^(B_INDEX,_)), precedence(A, ^^(A_PRIOR,_)), associativity(B, B_ASSOC), precedence(B, ^^(B_PRIOR,_)), associativity(A, A_ASSOC), equal(A_ASSOC, "L"), index(A, ^^(A_INDEX,_)), lessThan(A_INDEX, B_INDEX), same_step(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#high_priority_left_assoc', B),
	rdf_assert(A, 'http://penskoy.n/expressions#high_priority', B),
	fail.

% Rule: equal_priority_R_assoc []
swrl_rule() :- 
	equal(A_PRIOR, B_PRIOR), equal(A_ASSOC, B_ASSOC), index(B, ^^(B_INDEX,_)), precedence(A, ^^(A_PRIOR,_)), associativity(B, B_ASSOC), precedence(B, ^^(B_PRIOR,_)), associativity(A, A_ASSOC), equal(A_ASSOC, "R"), index(A, ^^(A_INDEX,_)), same_step(A, B), greaterThan(A_INDEX, B_INDEX),
	rdf_assert(A, 'http://penskoy.n/expressions#high_priority', B),
	rdf_assert(A, 'http://penskoy.n/expressions#high_priority_right_assoc', B),
	fail.

% Rule: eval_,_in_function_call []
swrl_rule() :- 
	text(A, ^^(",",_)), init(A, true), in_complex(A, B), is_function_call(B, true),
	rdf_assert(A, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	fail.

% Rule: eval_binary_operation []
swrl_rule() :- 
	next_step(B, B_NEXT), next_step(C, C_NEXT), has_highest_priority_to_right(A, true), find_left_operand(A, B), step(A, ^^(A_STEP,_)), arity(A, "binary"), init(A, true), has_highest_priority_to_left(A, true), find_right_operand(A, C), next_step(A, A_NEXT), same_step(A, C), same_step(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', C),
	rdf_assert(A, 'http://penskoy.n/expressions#copy_without_marks', A_NEXT),
	rdf_assert(C, 'http://penskoy.n/expressions#copy_without_marks', C_NEXT),
	rdf_assert(B_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#eval_step', A_STEP),
	rdf_assert(C_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A_NEXT, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	rdf_assert(B, 'http://penskoy.n/expressions#copy_without_marks', B_NEXT),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', B),
	fail.

% Rule: eval_binary_operation_copy_other []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), arity(A, "binary"), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), find_right_operand(A, C), find_left_operand(A, B), init(A, true), not_index(B, ^^(OTHER,_)), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), not_index(C, ^^(OTHER,_)), same_step(A, C), same_step(A, B),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: eval_complex_operation []
swrl_rule() :- 
	next_step(C, C_NEXT), next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), all_eval_to_right(A, B), step(A, ^^(A_STEP,_)), arity(A, "complex"), init(A, true), has_highest_priority_to_left(A, true), next_step(A, A_NEXT), same_step(A, C), complex_boundaries(A, C),
	rdf_assert(A, 'http://penskoy.n/expressions#copy_without_marks', A_NEXT),
	rdf_assert(C, 'http://penskoy.n/expressions#copy_without_marks', C_NEXT),
	rdf_assert(A, 'http://penskoy.n/expressions#eval_step', A_STEP),
	rdf_assert(A, 'http://penskoy.n/expressions#has_complex_operator_part', C),
	rdf_assert(C_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A_NEXT, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	fail.

% Rule: eval_complex_operation_copy_inner_app []
swrl_rule() :- 
	next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), complex_boundaries(A, C), index(C, ^^(C_INDEX,_)), all_eval_to_right(A, B), arity(A, "complex"), app(OTHER, true), init(A, true), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), not_index(C, ^^(OTHER,_)), index(OTHER, ^^(OTHER_INDEX,_)), lessThan(OTHER_INDEX, C_INDEX), same_step(A, C), index(A, ^^(A_INDEX,_)), lessThan(A_INDEX, OTHER_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy_without_marks', OTHER_NEXT),
	rdf_assert(OTHER_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	fail.

% Rule: eval_complex_operation_copy_inner_eval []
swrl_rule() :- 
	next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), complex_boundaries(A, C), index(C, ^^(C_INDEX,_)), all_eval_to_right(A, B), arity(A, "complex"), init(A, true), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), not_index(C, ^^(OTHER,_)), index(OTHER, ^^(OTHER_INDEX,_)), lessThan(OTHER_INDEX, C_INDEX), same_step(A, C), index(A, ^^(A_INDEX,_)), lessThan(A_INDEX, OTHER_INDEX), eval(OTHER, true),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy_without_marks', OTHER_NEXT),
	rdf_assert(OTHER_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', OTHER),
	fail.

% Rule: all_app_to_right_begin []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), init(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_app_to_right', A),
	fail.

% Rule: eval_complex_operation_copy_other_left []
swrl_rule() :- 
	next_step(C, C_NEXT), next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), complex_boundaries(A, C), index(C, ^^(C_INDEX,_)), all_eval_to_right(A, B), arity(A, "complex"), init(A, true), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), next_step(A, A_NEXT), not_index(C, ^^(OTHER,_)), is_function_call(A, false), same_step(A, C), index(OTHER, ^^(OTHER_INDEX,_)), index(A, ^^(A_INDEX,_)), lessThan(OTHER_INDEX, A_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: eval_complex_operation_copy_other_right []
swrl_rule() :- 
	next_step(C, C_NEXT), next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), complex_boundaries(A, C), index(C, ^^(C_INDEX,_)), all_eval_to_right(A, B), arity(A, "complex"), init(A, true), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), next_step(A, A_NEXT), not_index(C, ^^(OTHER,_)), same_step(A, C), index(OTHER, ^^(OTHER_INDEX,_)), index(A, ^^(A_INDEX,_)), greaterThan(OTHER_INDEX, C_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: eval_complex_operation_copy_others_left_no_function_name []
swrl_rule() :- 
	next_step(C, C_NEXT), next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), complex_boundaries(A, C), index(C, ^^(C_INDEX,_)), find_left_operand(A, D), all_eval_to_right(A, B), arity(A, "complex"), init(A, true), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), next_step(A, A_NEXT), is_function_call(A, true), not_index(D, ^^(OTHER,_)), not_index(C, ^^(OTHER,_)), same_step(A, C), index(OTHER, ^^(OTHER_INDEX,_)), index(A, ^^(A_INDEX,_)), lessThan(OTHER_INDEX, A_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: student_error_in_complex []
swrl_rule() :- 
	before_by_third_operator(A, B), before_third_operator(A, C), text(C, ^^("(",_)), describe_error(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#student_error_in_complex', A),
	fail.

% Rule: eval_function_name []
swrl_rule() :- 
	next_step(FUNCTION_NAME, FUNCTION_NAME_NEXT), next_index(B, ^^(C,_)), has_highest_priority_to_right(A, true), all_eval_to_right(A, B), find_left_operand(A, FUNCTION_NAME), same_step(A, FUNCTION_NAME), arity(A, "complex"), init(A, true), has_highest_priority_to_left(A, true), is_function_call(A, true), same_step(A, C), complex_boundaries(A, C),
	rdf_assert(FUNCTION_NAME, 'http://penskoy.n/expressions#copy_without_marks', FUNCTION_NAME_NEXT),
	rdf_assert(FUNCTION_NAME_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#has_complex_operator_part', FUNCTION_NAME),
	fail.

% Rule: describe_error []
swrl_rule() :- 
	student_pos_less(B, A), before_direct(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#describe_error', B),
	fail.

% Rule: eval_operand_in_complex []
swrl_rule() :- 
	init(A, true), in_complex(A, B), is_operand(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	fail.

% Rule: eval_postfix_operation []
swrl_rule() :- 
	next_step(B, B_NEXT), has_highest_priority_to_right(A, true), find_left_operand(A, B), step(A, ^^(A_STEP,_)), arity(A, "unary"), init(A, true), has_highest_priority_to_left(A, true), prefix_postfix(A, "postfix"), next_step(A, A_NEXT), same_step(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#copy_without_marks', A_NEXT),
	rdf_assert(B_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#eval_step', A_STEP),
	rdf_assert(A_NEXT, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	rdf_assert(B, 'http://penskoy.n/expressions#copy_without_marks', B_NEXT),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', B),
	fail.

% Rule: student_error_in_complex_bound []
swrl_rule() :- 
	before_as_operand(A, B), complex_beginning(B, true), describe_error(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#student_error_in_complex', A),
	fail.

% Rule: eval_postfix_operation_copy_others []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), find_left_operand(A, B), arity(A, "unary"), init(A, true), not_index(B, ^^(OTHER,_)), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), prefix_postfix(A, "postfix"), same_step(A, B),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: student_error_left_assoc []
swrl_rule() :- 
	before_as_operand(A, B), describe_error(A, B), high_priority_left_assoc(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#student_error_left_assoc', A),
	fail.

% Rule: eval_prefix_operation []
swrl_rule() :- 
	next_step(B, B_NEXT), has_highest_priority_to_right(A, true), step(A, ^^(A_STEP,_)), arity(A, "unary"), init(A, true), not_index(B, ^^(OTHER,_)), prefix_postfix(A, "prefix"), has_highest_priority_to_left(A, true), next_step(A, A_NEXT), find_right_operand(A, B), same_step(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#copy_without_marks', A_NEXT),
	rdf_assert(B_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#eval_step', A_STEP),
	rdf_assert(A_NEXT, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	rdf_assert(B, 'http://penskoy.n/expressions#copy_without_marks', B_NEXT),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', B),
	fail.

% Rule: student_error_more_priority []
swrl_rule() :- 
	before_as_operand(A, B), describe_error(A, B), high_priority_diff_priority(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#student_error_more_priority', A),
	fail.

% Rule: eval_prefix_operation_copy_others []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), arity(A, "unary"), init(A, true), not_index(B, ^^(OTHER,_)), next_step(OTHER, OTHER_NEXT), prefix_postfix(A, "prefix"), same_step(A, OTHER), has_highest_priority_to_left(A, true), not_index(A, ^^(OTHER,_)), find_right_operand(A, B), same_step(A, B),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: student_error_right_assoc []
swrl_rule() :- 
	before_as_operand(A, B), describe_error(A, B), high_priority_right_assoc(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#student_error_right_assoc', A),
	fail.

% Rule: eval_ternary_operation []
swrl_rule() :- 
	arity(A, "ternary"), next_step(C, C_NEXT), next_index(B, ^^(C,_)), step(A, ^^(A_STEP,_)), has_highest_priority_to_right(C, true), find_right_operand(C, E), complex_boundaries(A, C), find_left_operand(A, D), all_eval_to_right(A, B), next_step(E, E_NEXT), init(A, true), next_step(D, D_NEXT), next_step(A, A_NEXT), has_highest_priority_to_left(C, true), same_step(A, C),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', E),
	rdf_assert(D, 'http://penskoy.n/expressions#copy_without_marks', D_NEXT),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', D),
	rdf_assert(A, 'http://penskoy.n/expressions#copy_without_marks', A_NEXT),
	rdf_assert(C, 'http://penskoy.n/expressions#copy_without_marks', C_NEXT),
	rdf_assert(E, 'http://penskoy.n/expressions#copy_without_marks', E_NEXT),
	rdf_assert(A, 'http://penskoy.n/expressions#eval_step', A_STEP),
	rdf_assert(A, 'http://penskoy.n/expressions#has_complex_operator_part', C),
	rdf_assert(C_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(D_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(E_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A_NEXT, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	fail.

% Rule: student_error_strict_operands_order []
swrl_rule() :- 
	before_by_third_operator(A, B), before_third_operator(A, C), is_operator_with_strict_operands_order(C, true), describe_error(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#student_error_strict_operands_order', A),
	fail.

% Rule: eval_ternary_operation_copy_inner_app []
swrl_rule() :- 
	index(C, ^^(C_INDEX,_)), arity(A, "ternary"), step(A, ^^(A_STEP,_)), step(OTHER, ^^(A_STEP,_)), eval_step(A, A_STEP), app(OTHER, true), next_step(OTHER, OTHER_NEXT), index(OTHER, ^^(OTHER_INDEX,_)), lessThan(OTHER_INDEX, C_INDEX), complex_boundaries(A, C), index(A, ^^(A_INDEX,_)), lessThan(A_INDEX, OTHER_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy_without_marks', OTHER_NEXT),
	rdf_assert(OTHER_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	fail.

% Rule: eval_ternary_operation_copy_inner_eval []
swrl_rule() :- 
	index(C, ^^(C_INDEX,_)), arity(A, "ternary"), step(A, ^^(A_STEP,_)), step(OTHER, ^^(A_STEP,_)), eval_step(A, A_STEP), next_step(OTHER, OTHER_NEXT), index(OTHER, ^^(OTHER_INDEX,_)), lessThan(OTHER_INDEX, C_INDEX), complex_boundaries(A, C), index(A, ^^(A_INDEX,_)), lessThan(A_INDEX, OTHER_INDEX), eval(OTHER, true),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy_without_marks', OTHER_NEXT),
	rdf_assert(OTHER_NEXT, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#has_operand', OTHER),
	fail.

% Rule: eval_ternary_operation_copy_other_left []
swrl_rule() :- 
	arity(A, "ternary"), eval_step(A, A_STEP), step(A, ^^(A_STEP,_)), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), find_left_operand(A, D), not_index(D, ^^(OTHER,_)), index(OTHER, ^^(OTHER_INDEX,_)), index(A, ^^(A_INDEX,_)), lessThan(OTHER_INDEX, A_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: eval_ternary_operation_copy_other_right []
swrl_rule() :- 
	arity(A, "ternary"), eval_step(A, A_STEP), step(A, ^^(A_STEP,_)), next_step(OTHER, OTHER_NEXT), same_step(A, OTHER), complex_boundaries(A, C), find_right_operand(C, D), not_index(D, ^^(OTHER,_)), index(OTHER, ^^(OTHER_INDEX,_)), index(C, ^^(C_INDEX,_)), lessThan(C_INDEX, OTHER_INDEX),
	rdf_assert(OTHER, 'http://penskoy.n/expressions#copy', OTHER_NEXT),
	fail.

% Rule: before_strict_order_operands []
swrl_rule() :- 
	is_operator_with_strict_operands_order(A, true), text(A, ^^(A_TEXT,_)), notEqual(A_TEXT, "?"), has_operand(A, B), has_operand(A, C), index(B, ^^(B_INDEX,_)), index(C, ^^(C_INDEX,_)), lessThan(B_INDEX, C_INDEX),
	rdf_assert(B, 'http://penskoy.n/expressions#before_direct', C),
	rdf_assert(B, 'http://penskoy.n/expressions#before_all_operands', C),
	rdf_assert(B, 'http://penskoy.n/expressions#before_by_third_operator', C),
	rdf_assert(B, 'http://penskoy.n/expressions#before_third_operator', A),
	fail.

% Rule: find_left_operand_eval []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), prev_index(B, ^^(C,_)), eval(C, true), has_highest_priority_to_left(A, true), all_app_to_left(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#find_left_operand', C),
	fail.

% Rule: find_left_operand_init []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), prev_index(B, ^^(C,_)), has_highest_priority_to_left(A, true), init(C, true), all_app_to_left(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#find_left_operand', C),
	fail.

% Rule: find_right_operand_eval []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), next_index(B, ^^(C,_)), all_app_to_right(A, B), eval(C, true), has_highest_priority_to_left(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#find_right_operand', C),
	fail.

% Rule: find_right_operand_init []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), next_index(B, ^^(C,_)), all_app_to_right(A, B), has_highest_priority_to_left(A, true), init(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#find_right_operand', C),
	fail.

% Rule: has_highest_priority_to_left []
swrl_rule() :- 
	more_priority_left_by_step(A, B), index(B, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#has_highest_priority_to_left', "true"^^xsd:boolean),
	fail.

% Rule: has_highest_priority_to_left_in_complex_, []
swrl_rule() :- 
	prev_index(B, ^^(C,_)), in_complex(A, C), text(A, ^^(",",_)), is_function_call(C, false), more_priority_left_by_step(A, B), has_highest_priority_to_left(C, true), complex_boundaries(C, D),
	rdf_assert(A, 'http://penskoy.n/expressions#has_highest_priority_to_left', "true"^^xsd:boolean),
	fail.

% Rule: has_highest_priority_to_left_in_complex_not_, []
swrl_rule() :- 
	text(A, ^^(A_TEXT,_)), notEqual(A_TEXT, ","), prev_index(B, ^^(C,_)), in_complex(A, C), more_priority_left_by_step(A, B), has_highest_priority_to_left(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#has_highest_priority_to_left', "true"^^xsd:boolean),
	fail.

% Rule: has_highest_priority_to_left_ternary []
swrl_rule() :- 
	has_highest_priority_to_left(C, true), complex_boundaries(C, D),
	rdf_assert(D, 'http://penskoy.n/expressions#has_highest_priority_to_left', "true"^^xsd:boolean),
	fail.

% Rule: has_highest_priority_to_right []
swrl_rule() :- 
	more_priority_right_by_step(A, B), last(B, true),
	rdf_assert(A, 'http://penskoy.n/expressions#has_highest_priority_to_right', "true"^^xsd:boolean),
	fail.

% Rule: has_highest_priority_to_right_in_complex []
swrl_rule() :- 
	next_index(B, ^^(D,_)), has_highest_priority_to_right(C, true), in_complex(A, C), more_priority_right_by_step(A, B), complex_boundaries(C, D),
	rdf_assert(A, 'http://penskoy.n/expressions#has_highest_priority_to_right', "true"^^xsd:boolean),
	fail.

% Rule: has_highest_priority_to_right_ternary []
swrl_rule() :- 
	has_highest_priority_to_right(D, true), complex_boundaries(C, D),
	rdf_assert(C, 'http://penskoy.n/expressions#has_highest_priority_to_right', "true"^^xsd:boolean),
	fail.

% Rule: in_complex_step_skip_inner_complex []
swrl_rule() :- 
	in_complex(A, C), complex_boundaries(A, D), step(A, ^^(0,_)),
	rdf_assert(D, 'http://penskoy.n/expressions#in_complex', C),
	fail.

% Rule: high_priority []
swrl_rule() :- 
	precedence(A, ^^(A_PRIOR,_)), precedence(B, ^^(B_PRIOR,_)), lessThan(A_PRIOR, B_PRIOR), same_step(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#high_priority', B),
	rdf_assert(A, 'http://penskoy.n/expressions#high_priority_diff_priority', B),
	fail.

% Rule: is_operand_close_bracket []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("]",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operand', "true"^^xsd:boolean),
	fail.

% Rule: in_complex_step []
swrl_rule() :- 
	next_index(A, ^^(B,_)), step(A, ^^(0,_)), complex_beginning(A, false), in_complex(A, C), complex_ending(B, false),
	rdf_assert(B, 'http://penskoy.n/expressions#in_complex', C),
	fail.

% Rule: more_priority_right_by_step_first []
swrl_rule() :- 
	precedence(A, ^^(A_PRIOR,_)), init(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_right_by_step', A),
	fail.

% Rule: is_operand []
swrl_rule() :- 
	text(A, ^^(A_TEXT,_)), notEqual(A_TEXT, "sizeof"), matches(A_TEXT, "[a-zA-Z_0-9]+"), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operand', "true"^^xsd:boolean),
	fail.

% Rule: copy_to_1_step []
swrl_rule() :- 
	step(A, ^^(0,_)), step(B, ^^(1,_)), zero_step(B, A),
	rdf_assert(A, 'http://penskoy.n/expressions#copy', B),
	fail.

% Rule: is_operand_close_parenthesis []
swrl_rule() :- 
	text(A, ^^(")",_)), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operand', "true"^^xsd:boolean),
	fail.

% Rule: more_priority_left_by_step []
swrl_rule() :- 
	more_priority_left_by_step(A, B), prev_index(B, ^^(C,_)), high_priority(A, C),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_left_by_step', C),
	fail.

% Rule: more_priority_left_by_step_app []
swrl_rule() :- 
	more_priority_left_by_step(A, B), prev_index(B, ^^(C,_)), app(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_left_by_step', C),
	fail.

% Rule: more_priority_left_by_step_eval []
swrl_rule() :- 
	more_priority_left_by_step(A, B), prev_index(B, ^^(C,_)), eval(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_left_by_step', C),
	fail.

% Rule: more_priority_left_by_step_first []
swrl_rule() :- 
	precedence(A, ^^(A_PRIOR,_)), init(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_left_by_step', A),
	fail.

% Rule: more_priority_left_by_step_operand []
swrl_rule() :- 
	more_priority_left_by_step(A, B), prev_index(B, ^^(C,_)), is_operand(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_left_by_step', C),
	fail.

% Rule: more_priority_right_by_step []
swrl_rule() :- 
	more_priority_right_by_step(A, B), next_index(B, ^^(C,_)), high_priority(A, C),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_right_by_step', C),
	fail.

% Rule: more_priority_right_by_step_app []
swrl_rule() :- 
	more_priority_right_by_step(A, B), next_index(B, ^^(C,_)), app(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_right_by_step', C),
	fail.

% Rule: before_in_complex []
swrl_rule() :- 
	has_operand(A, B), text(B, ^^("(",_)), has_operand(B, C),
	rdf_assert(C, 'http://penskoy.n/expressions#before_direct', A),
	rdf_assert(C, 'http://penskoy.n/expressions#before_by_third_operator', A),
	rdf_assert(C, 'http://penskoy.n/expressions#before_third_operator', B),
	fail.

% Rule: more_priority_right_by_step_eval []
swrl_rule() :- 
	more_priority_right_by_step(A, B), next_index(B, ^^(C,_)), eval(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_right_by_step', C),
	fail.

% Rule: operator += []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("+=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: more_priority_right_by_step_operand []
swrl_rule() :- 
	more_priority_right_by_step(A, B), next_index(B, ^^(C,_)), is_operand(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#more_priority_right_by_step', C),
	fail.

% Rule: all_eval_to_right []
swrl_rule() :- 
	all_eval_to_right(A, B), next_index(B, ^^(C,_)), eval(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_eval_to_right', C),
	fail.

% Rule: next_prev []
swrl_rule() :- 
	index(A, ^^(A_INDEX,_)), index(B, ^^(B_INDEX,_)), add(B_INDEX, A_INDEX, 1), same_step(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#next_index', B),
	rdf_assert(B, 'http://penskoy.n/expressions#prev_index', A),
	fail.

% Rule: next_step []
swrl_rule() :- 
	index(A, ^^(A_INDEX,_)), index(B, ^^(A_INDEX,_)), step(A, ^^(A_STEP,_)), step(B, ^^(B_STEP,_)), add(B_STEP, A_STEP, 1),
	rdf_assert(A, 'http://penskoy.n/expressions#next_step', B),
	fail.

% Rule: not_index []
swrl_rule() :- 
	index(A, ^^(A_INDEX,_)), index(B, ^^(B_INDEX,_)), notEqual(A_INDEX, B_INDEX), same_step(A, B),
	rdf_assert(B, 'http://penskoy.n/expressions#not_index', A),
	rdf_assert(A, 'http://penskoy.n/expressions#not_index', B),
	fail.

% Rule: before []
swrl_rule() :- 
	has_operand(A, B), text(B, ^^(B_TEXT,_)), notEqual(B_TEXT, "("),
	rdf_assert(B, 'http://penskoy.n/expressions#before_direct', A),
	rdf_assert(B, 'http://penskoy.n/expressions#before_as_operand', A),
	fail.

% Rule: operator! []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("!",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: all_app_to_left_begin []
swrl_rule() :- 
	init(A, true), has_highest_priority_to_left(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_app_to_left', A),
	fail.

% Rule: operator!= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("!=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 10),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: zero_step []
swrl_rule() :- 
	index(A, ^^(A_INDEX,_)), index(B, ^^(A_INDEX,_)), step(B, ^^(0,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#zero_step', B),
	fail.

% Rule: operator% []
swrl_rule() :- 
	text(A, ^^("%",_)), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 5),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operator%= []
swrl_rule() :- 
	text(A, ^^("%=",_)), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator& []
swrl_rule() :- 
	text(A, ^^("&",_)), step(A, ^^(1,_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator&& []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("&&",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operator_with_strict_operands_order', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 14),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operator|= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("|=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator&= []
swrl_rule() :- 
	text(A, ^^("&=",_)), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator( []
swrl_rule() :- 
	text(A, ^^("(",_)), step(A, ^^(1,_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 0),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "complex"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#complex_beginning', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#is_function_call', "false"^^xsd:boolean),
	fail.

% Rule: operator*= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("*=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: complex_boundaries_empty []
swrl_rule() :- 
	next_index(A, ^^(B,_)), step(A, ^^(0,_)), complex_beginning(A, true), complex_ending(B, true),
	rdf_assert(A, 'http://penskoy.n/expressions#complex_boundaries', B),
	fail.

% Rule: operator, []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^(",",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 17),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operator_with_strict_operands_order', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: complex_boundaries []
swrl_rule() :- 
	in_complex(A, C), next_index(A, ^^(B,_)), complex_beginning(A, false), complex_ending(B, true), step(A, ^^(0,_)),
	rdf_assert(C, 'http://penskoy.n/expressions#complex_boundaries', B),
	fail.

% Rule: operator-= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("-=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator|| []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("||",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 15),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operator_with_strict_operands_order', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: copy_app []
swrl_rule() :- 
	copy(A, TO), app(A, true),
	rdf_assert(TO, 'http://penskoy.n/expressions#app', "true"^^xsd:boolean),
	fail.

% Rule: prev_operand []
swrl_rule() :- 
	prev_index(A, ^^(B,_)), text(B, ^^(B_TEXT,_)), is_operand(B, true), step(B, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#prev_operand', B),
	fail.

% Rule: before_strict_order_operands_ternary []
swrl_rule() :- 
	text(A, ^^("?",_)), has_operand(A, B), has_operand(A, C), has_operand(A, D), index(B, ^^(B_INDEX,_)), index(C, ^^(C_INDEX,_)), index(D, ^^(D_INDEX,_)), not_index(C, ^^(D,_)), lessThan(B_INDEX, C_INDEX), lessThan(B_INDEX, D_INDEX),
	rdf_assert(B, 'http://penskoy.n/expressions#before_direct', C),
	rdf_assert(B, 'http://penskoy.n/expressions#before_all_operands', C),
	rdf_assert(B, 'http://penskoy.n/expressions#before_by_third_operator', C),
	rdf_assert(B, 'http://penskoy.n/expressions#before_third_operator', A),
	fail.

% Rule: operator-gt []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("->",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 2),
	fail.

% Rule: copy_to_zero_step []
swrl_rule() :- 
	step(A, ^^(0,_)), step(B, ^^(1,_)), zero_step(B, A),
	rdf_assert(B, 'http://penskoy.n/expressions#copy_without_marks', A),
	fail.

% Rule: operator. []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^(".",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 2),
	fail.

% Rule: operator/ []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("/",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 5),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operator/= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("/=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator: []
swrl_rule() :- 
	text(A, ^^(":",_)), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "ternary"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#complex_ending', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator:: []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("::",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 1),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: all_eval_to_right_begin []
swrl_rule() :- 
	has_highest_priority_to_right(A, true), init(A, true), complex_beginning(A, true), has_highest_priority_to_left(A, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_eval_to_right', A),
	fail.

% Rule: all_eval_to_right_app []
swrl_rule() :- 
	all_eval_to_right(A, B), next_index(B, ^^(C,_)), app(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_eval_to_right', C),
	fail.

% Rule: operatorlt []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("<",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 9),
	fail.

% Rule: operatorltlt []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("<<",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 7),
	fail.

% Rule: before_function_call []
swrl_rule() :- 
	has_operand(A, B), text(B, ^^("(",_)), is_function_call(B, true),
	rdf_assert(B, 'http://penskoy.n/expressions#before_direct', A),
	rdf_assert(B, 'http://penskoy.n/expressions#before_as_operand', A),
	fail.

% Rule: all_app_to_right []
swrl_rule() :- 
	all_app_to_right(A, B), next_index(B, ^^(C,_)), app(C, true),
	rdf_assert(A, 'http://penskoy.n/expressions#all_app_to_right', C),
	fail.

% Rule: operatorltlt= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("<<=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: before_direct []
swrl_rule() :- 
	before_direct(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#before', B),
	fail.

% Rule: operatorlt= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("<=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 9),
	fail.

% Rule: operator= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator== []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("==",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 10),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: ast_edge_has_complex_operator_part []
swrl_rule() :- 
	has_complex_operator_part(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#ast_edge', B),
	fail.

% Rule: operatorgt []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^(">",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 9),
	fail.

% Rule: operatorgt= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^(">=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 9),
	fail.

% Rule: operatorgtgt []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^(">>",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 7),
	fail.

% Rule: before_before []
swrl_rule() :- 
	before(A, B), before(B, C),
	rdf_assert(A, 'http://penskoy.n/expressions#before', C),
	fail.

% Rule: operator_binary& []
swrl_rule() :- 
	text(A, ^^("&",_)), step(A, ^^(1,_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 11),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operatorgtgt= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^(">>=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator? []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("?",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "ternary"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#is_operator_with_strict_operands_order', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#complex_beginning', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator^ []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("^",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 12),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operator^= []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("^=",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 16),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator_binary* []
swrl_rule() :- 
	text(A, ^^("*",_)), step(A, ^^(1,_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 5),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operator_binary+ []
swrl_rule() :- 
	text(A, ^^("+",_)), step(A, ^^(1,_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 6),
	fail.

% Rule: operator_binary- []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("-",_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 6),
	fail.

% Rule: operator_function_call []
swrl_rule() :- 
	text(A, ^^("(",_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "complex"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#is_function_call', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 2),
	fail.

% Rule: copy_eval_step_to_zero_step []
swrl_rule() :- 
	eval_step(A, A_STEP), zero_step(A, A0),
	rdf_assert(A0, 'http://penskoy.n/expressions#eval_step', A_STEP),
	fail.

% Rule: operator_postfix++ []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("++",_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "postfix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 2),
	fail.

% Rule: copy_eval []
swrl_rule() :- 
	copy(A, TO), eval(A, true),
	rdf_assert(TO, 'http://penskoy.n/expressions#eval', "true"^^xsd:boolean),
	fail.

% Rule: operator_postfix-- []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("--",_)), prev_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "postfix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 2),
	fail.

% Rule: operator_prefix++ []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("++",_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator_prefix-- []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("--",_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator_subscript []
swrl_rule() :- 
	text(A, ^^("[",_)), step(A, ^^(1,_)),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "complex"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#complex_beginning', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#is_function_call', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 2),
	fail.

% Rule: copy_has_complex_operator_part_to_zero_step []
swrl_rule() :- 
	has_complex_operator_part(A, B), zero_step(A, A0), zero_step(B, B0),
	rdf_assert(A0, 'http://penskoy.n/expressions#has_complex_operator_part', B0),
	fail.

% Rule: operator~ []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("~",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: operator_unary* []
swrl_rule() :- 
	text(A, ^^("*",_)), step(A, ^^(1,_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: before_all_operands []
swrl_rule() :- 
	before_all_operands(A, B), has_operand(B, C),
	rdf_assert(A, 'http://penskoy.n/expressions#before_direct', C),
	rdf_assert(A, 'http://penskoy.n/expressions#before_by_third_operator', C),
	rdf_assert(A, 'http://penskoy.n/expressions#before_all_operands', C),
	fail.

% Rule: copy_has_operand_to_zero_step []
swrl_rule() :- 
	has_operand(A, B), zero_step(A, A0), zero_step(B, B0),
	rdf_assert(A0, 'http://penskoy.n/expressions#has_operand', B0),
	fail.

% Rule: operator_unary+ []
swrl_rule() :- 
	text(A, ^^("+",_)), step(A, ^^(1,_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: copy_without_marks []
swrl_rule() :- 
	copy(A, TO),
	rdf_assert(A, 'http://penskoy.n/expressions#copy_without_marks', TO),
	fail.

% Rule: operator_unary- []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("-",_)), prev_operation(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "unary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	rdf_assert(A, 'http://penskoy.n/expressions#prefix_postfix', "prefix"),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 3),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "R"),
	fail.

% Rule: copy_init []
swrl_rule() :- 
	copy(A, TO), init(A, true),
	rdf_assert(TO, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: operator| []
swrl_rule() :- 
	step(A, ^^(1,_)), text(A, ^^("|",_)),
	rdf_assert(A, 'http://penskoy.n/expressions#precedence', 13),
	rdf_assert(A, 'http://penskoy.n/expressions#associativity', "L"),
	rdf_assert(A, 'http://penskoy.n/expressions#arity', "binary"),
	rdf_assert(A, 'http://penskoy.n/expressions#init', "true"^^xsd:boolean),
	fail.

% Rule: copy_without_marks_arity []
swrl_rule() :- 
	arity(A, A_ARITY), copy_without_marks(A, TO),
	rdf_assert(TO, 'http://penskoy.n/expressions#arity', A_ARITY),
	fail.

% Rule: ast_edge_has_operand []
swrl_rule() :- 
	has_operand(A, B),
	rdf_assert(A, 'http://penskoy.n/expressions#ast_edge', B),
	fail.
