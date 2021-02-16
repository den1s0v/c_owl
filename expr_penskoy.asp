#script (lua)
function matches(s, pattern)
    ss = s.string
    if ss == nil then
        ss = s.name
    end
    if ss:match(pattern.string) ~= nil then
        return 1
    else
        return 0
    end
end
#end.


% Rule: rule_find_left_operand_init []
	t(A, find_left_operand, C):-t(A, has_highest_priority_to_right, true), t(B, prev_index, C), t(A, has_highest_priority_to_left, true), t(C, init, true), t(A, all_app_to_left, B).

% Rule: rule_before_strict_order_operands_ternary []
	t(B, before_direct, C):-t(A, text, "?"), t(A, has_operand, B), t(A, has_operand, C), t(A, has_operand, D), t(B, index, B_INDEX), t(C, index, C_INDEX), t(D, index, D_INDEX), t(C, not_index, D), B_INDEX < C_INDEX, B_INDEX < D_INDEX.
	t(B, before_all_operands, C):-t(A, text, "?"), t(A, has_operand, B), t(A, has_operand, C), t(A, has_operand, D), t(B, index, B_INDEX), t(C, index, C_INDEX), t(D, index, D_INDEX), t(C, not_index, D), B_INDEX < C_INDEX, B_INDEX < D_INDEX.
	t(B, before_by_third_operator, C):-t(A, text, "?"), t(A, has_operand, B), t(A, has_operand, C), t(A, has_operand, D), t(B, index, B_INDEX), t(C, index, C_INDEX), t(D, index, D_INDEX), t(C, not_index, D), B_INDEX < C_INDEX, B_INDEX < D_INDEX.
	t(B, before_third_operator, A):-t(A, text, "?"), t(A, has_operand, B), t(A, has_operand, C), t(A, has_operand, D), t(B, index, B_INDEX), t(C, index, C_INDEX), t(D, index, D_INDEX), t(C, not_index, D), B_INDEX < C_INDEX, B_INDEX < D_INDEX.

% Rule: rule_student_error_strict_operands_order []
	t(B, student_error_strict_operands_order, A):-t(A, before_by_third_operator, B), t(A, before_third_operator, C), t(C, is_operator_with_strict_operands_order, true), t(A, describe_error, B).

% Rule: rule_complex_boundaries_empty []
	t(A, complex_boundaries, B):-t(A, next_index, B), t(A, step, 0), t(A, complex_beginning, true), t(B, complex_ending, true).

% Rule: rule_eval_ternary_operation_copy_other_right []
	t(OTHER, copy, OTHER_NEXT):-t(A, arity, "ternary"), t(A, eval_step, A_STEP), t(A, step, A_STEP), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, find_right_operand, D), t(D, not_index, OTHER), t(OTHER, index, OTHER_INDEX), t(C, index, C_INDEX), C_INDEX < OTHER_INDEX.

% Rule: rule_complex_boundaries []
	t(C, complex_boundaries, B):-t(A, in_complex, C), t(A, next_index, B), t(A, complex_beginning, false), t(B, complex_ending, true), t(A, step, 0).

% Rule: rule_find_left_operand_eval []
	t(A, find_left_operand, C):-t(A, has_highest_priority_to_right, true), t(B, prev_index, C), t(C, eval, true), t(A, has_highest_priority_to_left, true), t(A, all_app_to_left, B).

% Rule: rule_high_priority []
	t(A, high_priority, B):-t(A, precedence, A_PRIOR), t(B, precedence, B_PRIOR), A_PRIOR < B_PRIOR, t(A, same_step, B).
	t(A, high_priority_diff_priority, B):-t(A, precedence, A_PRIOR), t(B, precedence, B_PRIOR), A_PRIOR < B_PRIOR, t(A, same_step, B).

% Rule: rule_in_complex_step []
	t(B, in_complex, C):-t(A, next_index, B), t(A, step, 0), t(A, complex_beginning, false), t(A, in_complex, C), t(B, complex_ending, false).

% Rule: rule_has_highest_priority_to_left_ternary []
	t(D, has_highest_priority_to_left, true):-t(C, has_highest_priority_to_left, true), t(C, complex_boundaries, D).

% Rule: rule_in_complex_begin []
	t(B, in_complex, A):-t(A, next_index, B), t(A, complex_beginning, true), t(B, complex_ending, false), t(A, step, 0).

% Rule: rule_before []
	t(B, before_direct, A):-t(A, has_operand, B), t(B, text, B_TEXT), B_TEXT != "<(>".
	t(B, before_as_operand, A):-t(A, has_operand, B), t(B, text, B_TEXT), B_TEXT != "<(>".

% Rule: rule_before_all_operands []
	t(A, before_direct, C):-t(A, before_all_operands, B), t(B, has_operand, C).
	t(A, before_by_third_operator, C):-t(A, before_all_operands, B), t(B, has_operand, C).
	t(A, before_all_operands, C):-t(A, before_all_operands, B), t(B, has_operand, C).

% Rule: rule_copy_eval_step_to_zero_step []
	t(A0, eval_step, A_STEP):-t(A, eval_step, A_STEP), t(A, zero_step, A0).

% Rule: rule_find_right_operand_eval []
	t(A, find_right_operand, C):-t(A, has_highest_priority_to_right, true), t(B, next_index, C), t(A, all_app_to_right, B), t(C, eval, true), t(A, has_highest_priority_to_left, true).

% Rule: rule_before_strict_order_operands []
	t(B, before_direct, C):-t(A, is_operator_with_strict_operands_order, true), t(A, text, A_TEXT), A_TEXT != "?", t(A, has_operand, B), t(A, has_operand, C), t(B, index, B_INDEX), t(C, index, C_INDEX), B_INDEX < C_INDEX.
	t(B, before_all_operands, C):-t(A, is_operator_with_strict_operands_order, true), t(A, text, A_TEXT), A_TEXT != "?", t(A, has_operand, B), t(A, has_operand, C), t(B, index, B_INDEX), t(C, index, C_INDEX), B_INDEX < C_INDEX.
	t(B, before_by_third_operator, C):-t(A, is_operator_with_strict_operands_order, true), t(A, text, A_TEXT), A_TEXT != "?", t(A, has_operand, B), t(A, has_operand, C), t(B, index, B_INDEX), t(C, index, C_INDEX), B_INDEX < C_INDEX.
	t(B, before_third_operator, A):-t(A, is_operator_with_strict_operands_order, true), t(A, text, A_TEXT), A_TEXT != "?", t(A, has_operand, B), t(A, has_operand, C), t(B, index, B_INDEX), t(C, index, C_INDEX), B_INDEX < C_INDEX.

% Rule: rule_copy_to_1_step []
	t(A, copy, B):-t(A, step, 0), t(B, step, 1), t(B, zero_step, A).

% Rule: rule_copy_init []
	t(TO, init, true):-t(A, copy, TO), t(A, init, true).

% Rule: rule_copy_without_marks_text []
	t(TO, text, A_TEXT):-t(A, copy_without_marks, TO), t(A, text, A_TEXT).

% Rule: rule_copy_to_zero_step []
	t(B, copy_without_marks, A):-t(A, step, 0), t(B, step, 1), t(B, zero_step, A).

% Rule: rule_copy_has_operand_to_zero_step []
	t(A0, has_operand, B0):-t(A, has_operand, B), t(A, zero_step, A0), t(B, zero_step, B0).

% Rule: rule_copy_eval []
	t(TO, eval, true):-t(A, copy, TO), t(A, eval, true).

% Rule: rule_copy_app []
	t(TO, app, true):-t(A, copy, TO), t(A, app, true).

% Rule: rule_copy_has_complex_operator_part_to_zero_step []
	t(A0, has_complex_operator_part, B0):-t(A, has_complex_operator_part, B), t(A, zero_step, A0), t(B, zero_step, B0).

% Rule: rule_copy_without_marks_complex_boundaries []
	t(TO, complex_boundaries, C):-t(C, same_step, TO), t(A, copy_without_marks, TO), t(A, complex_boundaries, B), t(C, zero_step, B0), t(B, zero_step, B0).

% Rule: rule_copy_without_marks_complex_ending []
	t(TO, complex_ending, B):-t(A, complex_ending, B), t(A, copy_without_marks, TO).

% Rule: rule_copy_without_marks_in_complex []
	t(TO, in_complex, C):-t(C, same_step, TO), t(A, copy_without_marks, TO), t(A, in_complex, B), t(C, zero_step, B0), t(B, zero_step, B0).

% Rule: rule_has_highest_priority_to_left []
	t(A, has_highest_priority_to_left, true):-t(A, more_priority_left_by_step, B), t(B, index, 1).

% Rule: rule_copy_without_marks_is_function_call []
	t(TO, is_function_call, A_FC):-t(A, is_function_call, A_FC), t(A, copy_without_marks, TO).

% Rule: rule_find_right_operand_init []
	t(A, find_right_operand, C):-t(A, has_highest_priority_to_right, true), t(B, next_index, C), t(A, all_app_to_right, B), t(A, has_highest_priority_to_left, true), t(C, init, true).

% Rule: rule_copy_without_marks_complex_beginning []
	t(TO, complex_beginning, B):-t(A, complex_beginning, B), t(A, copy_without_marks, TO).

% Rule: rule_copy_without_marks []
	t(A, copy_without_marks, TO):-t(A, copy, TO).

% Rule: rule_has_highest_priority_to_left_in_complex_, []
	t(A, has_highest_priority_to_left, true):-t(B, prev_index, C), t(A, in_complex, C), t(A, text, "<,>"), t(C, is_function_call, false), t(A, more_priority_left_by_step, B), t(C, has_highest_priority_to_left, true), t(C, complex_boundaries, D).

% Rule: rule_copy_without_marks_arity []
	t(TO, arity, A_ARITY):-t(A, arity, A_ARITY), t(A, copy_without_marks, TO).

% Rule: rule_copy_without_marks_associativity []
	t(TO, associativity, A_ASSOCIATIVITY):-t(A, associativity, A_ASSOCIATIVITY), t(A, copy_without_marks, TO).

% Rule: rule_has_highest_priority_to_left_in_complex_not_, []
	t(A, has_highest_priority_to_left, true):-t(A, text, A_TEXT), A_TEXT != "<,>", t(B, prev_index, C), t(A, in_complex, C), t(A, more_priority_left_by_step, B), t(C, has_highest_priority_to_left, true).

% Rule: rule_copy_without_marks_priority []
	t(TO, precedence, A_PRIORITY):-t(A, precedence, A_PRIORITY), t(A, copy_without_marks, TO).

% Rule: rule_copy_without_marks_real_pos []
	t(TO, real_pos, A_RP):-t(A, real_pos, A_RP), t(A, copy_without_marks, TO).

% Rule: rule_copy_without_marks_student_pos []
	t(TO, student_pos, A_SP):-t(A, copy_without_marks, TO), t(A, student_pos, A_SP).

% Rule: rule_has_highest_priority_to_right []
	t(A, has_highest_priority_to_right, true):-t(A, more_priority_right_by_step, B), t(B, last, true).

% Rule: rule_copy_without_marks_prefix_postfix []
	t(TO, prefix_postfix, A_PR):-t(A, prefix_postfix, A_PR), t(A, copy_without_marks, TO).

% Rule: rule_copy_without_marks_is_operand []
	t(TO, is_operand, IS_OP):-t(A, copy_without_marks, TO), t(A, is_operand, IS_OP).

% Rule: rule_ast_edge_has_operand []
	t(A, ast_edge, B):-t(A, has_operand, B).

% Rule: rule_copy_without_marks_is_operator_with_strict_operands_order []
	t(TO, is_operator_with_strict_operands_order, IS_OP):-t(A, copy_without_marks, TO), t(A, is_operator_with_strict_operands_order, IS_OP).

% Rule: rule_has_highest_priority_to_right_ternary []
	t(C, has_highest_priority_to_right, true):-t(D, has_highest_priority_to_right, true), t(C, complex_boundaries, D).

% Rule: rule_copy_without_marks_last []
	t(TO, last, A_LAST):-t(A, last, A_LAST), t(A, copy_without_marks, TO).

% Rule: rule_has_highest_priority_to_right_in_complex []
	t(A, has_highest_priority_to_right, true):-t(B, next_index, D), t(C, has_highest_priority_to_right, true), t(A, in_complex, C), t(A, more_priority_right_by_step, B), t(C, complex_boundaries, D).

% Rule: rule_eval_ternary_operation_copy_other_left []
	t(OTHER, copy, OTHER_NEXT):-t(A, arity, "ternary"), t(A, eval_step, A_STEP), t(A, step, A_STEP), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, find_left_operand, D), t(D, not_index, OTHER), t(OTHER, index, OTHER_INDEX), t(A, index, A_INDEX), OTHER_INDEX < A_INDEX.

% Rule: rule_all_app_to_left []
	t(A, all_app_to_left, C):-t(A, all_app_to_left, B), t(B, prev_index, C), t(C, app, true).

% Rule: rule_equal_priority_R_assoc []
	t(A, high_priority, B):-A_PRIOR = B_PRIOR, A_ASSOC = B_ASSOC, t(B, index, B_INDEX), t(A, precedence, A_PRIOR), t(B, associativity, B_ASSOC), t(B, precedence, B_PRIOR), t(A, associativity, A_ASSOC), A_ASSOC = "R", t(A, index, A_INDEX), t(A, same_step, B), A_INDEX > B_INDEX.
	t(A, high_priority_right_assoc, B):-A_PRIOR = B_PRIOR, A_ASSOC = B_ASSOC, t(B, index, B_INDEX), t(A, precedence, A_PRIOR), t(B, associativity, B_ASSOC), t(B, precedence, B_PRIOR), t(A, associativity, A_ASSOC), A_ASSOC = "R", t(A, index, A_INDEX), t(A, same_step, B), A_INDEX > B_INDEX.

% Rule: rule_eval_,_in_function_call []
	t(A, app, true):-t(A, text, "<,>"), t(A, init, true), t(A, in_complex, B), t(B, is_function_call, true).

% Rule: rule_operator/= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "/=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "/=").
	t(A, init, true):-t(A, step, 1), t(A, text, "/=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "/=").

% Rule: rule_eval_binary_operation []
	t(A, has_operand, C):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(A, copy_without_marks, A_NEXT):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(C, copy_without_marks, C_NEXT):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(B_NEXT, app, true):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(A, eval_step, A_STEP):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(C_NEXT, app, true):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(A_NEXT, eval, true):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(B, copy_without_marks, B_NEXT):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).
	t(A, has_operand, B):-t(B, next_step, B_NEXT), t(C, next_step, C_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "binary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, find_right_operand, C), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, same_step, B).

% Rule: rule_zero_step []
	t(A, zero_step, B):-t(A, index, A_INDEX), t(B, index, A_INDEX), t(B, step, 0).

% Rule: rule_equal_priority_L_assoc []
	t(A, high_priority_left_assoc, B):-A_PRIOR = B_PRIOR, A_ASSOC = B_ASSOC, t(B, index, B_INDEX), t(A, precedence, A_PRIOR), t(B, associativity, B_ASSOC), t(B, precedence, B_PRIOR), t(A, associativity, A_ASSOC), A_ASSOC = "L", t(A, index, A_INDEX), A_INDEX < B_INDEX, t(A, same_step, B).
	t(A, high_priority, B):-A_PRIOR = B_PRIOR, A_ASSOC = B_ASSOC, t(B, index, B_INDEX), t(A, precedence, A_PRIOR), t(B, associativity, B_ASSOC), t(B, precedence, B_PRIOR), t(A, associativity, A_ASSOC), A_ASSOC = "L", t(A, index, A_INDEX), A_INDEX < B_INDEX, t(A, same_step, B).

% Rule: rule_operator: []
	t(A, arity, "ternary"):-t(A, text, ":"), t(A, step, 1).
	t(A, precedence, 16):-t(A, text, ":"), t(A, step, 1).
	t(A, init, true):-t(A, text, ":"), t(A, step, 1).
	t(A, complex_ending, true):-t(A, text, ":"), t(A, step, 1).
	t(A, associativity, "R"):-t(A, text, ":"), t(A, step, 1).

% Rule: rule_operatorltlt []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "<<").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "<<").
	t(A, init, true):-t(A, step, 1), t(A, text, "<<").
	t(A, precedence, 7):-t(A, step, 1), t(A, text, "<<").

% Rule: rule_operator:: []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "::").
	t(A, precedence, 1):-t(A, step, 1), t(A, text, "::").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "::").
	t(A, init, true):-t(A, step, 1), t(A, text, "::").

% Rule: rule_operatorlt []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "<").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "<").
	t(A, init, true):-t(A, step, 1), t(A, text, "<").
	t(A, precedence, 9):-t(A, step, 1), t(A, text, "<").

% Rule: rule_operatorltlt= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "<<=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "<<=").
	t(A, init, true):-t(A, step, 1), t(A, text, "<<=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "<<=").

% Rule: rule_eval_complex_operation []
	t(A, copy_without_marks, A_NEXT):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, step, A_STEP), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, complex_boundaries, C).
	t(C, copy_without_marks, C_NEXT):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, step, A_STEP), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, complex_boundaries, C).
	t(A, eval_step, A_STEP):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, step, A_STEP), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, complex_boundaries, C).
	t(A, has_complex_operator_part, C):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, step, A_STEP), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, complex_boundaries, C).
	t(C_NEXT, app, true):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, step, A_STEP), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, complex_boundaries, C).
	t(A_NEXT, eval, true):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, step, A_STEP), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, same_step, C), t(A, complex_boundaries, C).

% Rule: rule_operatorlt= []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "<=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "<=").
	t(A, init, true):-t(A, step, 1), t(A, text, "<=").
	t(A, precedence, 9):-t(A, step, 1), t(A, text, "<=").

% Rule: rule_eval_complex_operation_copy_inner_app []
	t(OTHER, copy_without_marks, OTHER_NEXT):-t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(OTHER, app, true), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(C, not_index, OTHER), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, same_step, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX.
	t(OTHER_NEXT, app, true):-t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(OTHER, app, true), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(C, not_index, OTHER), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, same_step, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX.

% Rule: rule_eval_complex_operation_copy_inner_eval []
	t(OTHER, copy_without_marks, OTHER_NEXT):-t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(C, not_index, OTHER), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, same_step, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX, t(OTHER, eval, true).
	t(OTHER_NEXT, app, true):-t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(C, not_index, OTHER), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, same_step, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX, t(OTHER, eval, true).
	t(A, has_operand, OTHER):-t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(C, not_index, OTHER), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, same_step, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX, t(OTHER, eval, true).

% Rule: rule_eval_binary_operation_copy_other []
	t(OTHER, copy, OTHER_NEXT):-t(A, has_highest_priority_to_right, true), t(A, arity, "binary"), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, find_right_operand, C), t(A, find_left_operand, B), t(A, init, true), t(B, not_index, OTHER), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(C, not_index, OTHER), t(A, same_step, C), t(A, same_step, B).

% Rule: rule_operator= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "=").
	t(A, init, true):-t(A, step, 1), t(A, text, "=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "=").

% Rule: rule_in_complex_step_skip_inner_complex []
	t(D, in_complex, C):-t(A, in_complex, C), t(A, complex_boundaries, D), t(A, step, 0).

% Rule: rule_operatorgt= []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, ">=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, ">=").
	t(A, init, true):-t(A, step, 1), t(A, text, ">=").
	t(A, precedence, 9):-t(A, step, 1), t(A, text, ">=").

% Rule: rule_is_operand_close_bracket []
	t(A, init, true):-t(A, step, 1), t(A, text, "]").
	t(A, is_operand, true):-t(A, step, 1), t(A, text, "]").

% Rule: rule_operator== []
	t(A, precedence, 10):-t(A, step, 1), t(A, text, "==").
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "==").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "==").
	t(A, init, true):-t(A, step, 1), t(A, text, "==").

% Rule: rule_before_direct []
	t(A, before, B):-t(A, before_direct, B).

% Rule: rule_is_operand []
	t(A, init, true):-t(A, text, A_TEXT), A_TEXT != "sizeof", 1 = @matches(A_TEXT, "[a-zA-Z_0-9]+"), t(A, step, 1).
	t(A, is_operand, true):-t(A, text, A_TEXT), A_TEXT != "sizeof", 1 = @matches(A_TEXT, "[a-zA-Z_0-9]+"), t(A, step, 1).

% Rule: rule_operatorgt []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, ">").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, ">").
	t(A, init, true):-t(A, step, 1), t(A, text, ">").
	t(A, precedence, 9):-t(A, step, 1), t(A, text, ">").

% Rule: rule_eval_ternary_operation []
	t(A, has_operand, E):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(D, copy_without_marks, D_NEXT):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(A, has_operand, D):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(A, copy_without_marks, A_NEXT):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(C, copy_without_marks, C_NEXT):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(E, copy_without_marks, E_NEXT):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(A, eval_step, A_STEP):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(A, has_complex_operator_part, C):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(C_NEXT, app, true):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(D_NEXT, app, true):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(E_NEXT, app, true):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).
	t(A_NEXT, eval, true):-t(A, arity, "ternary"), t(C, next_step, C_NEXT), t(B, next_index, C), t(A, step, A_STEP), t(C, has_highest_priority_to_right, true), t(C, find_right_operand, E), t(A, complex_boundaries, C), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(E, next_step, E_NEXT), t(A, init, true), t(D, next_step, D_NEXT), t(A, next_step, A_NEXT), t(C, has_highest_priority_to_left, true), t(A, same_step, C).

% Rule: rule_is_operand_close_parenthesis []
	t(A, init, true):-t(A, text, ")"), t(A, step, 1).
	t(A, is_operand, true):-t(A, text, ")"), t(A, step, 1).

% Rule: rule_operatorgtgt []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, ">>").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, ">>").
	t(A, init, true):-t(A, step, 1), t(A, text, ">>").
	t(A, precedence, 7):-t(A, step, 1), t(A, text, ">>").

% Rule: rule_more_priority_left_by_step []
	t(A, more_priority_left_by_step, C):-t(A, more_priority_left_by_step, B), t(B, prev_index, C), t(A, high_priority, C).

% Rule: rule_operatorgtgt= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, ">>=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, ">>=").
	t(A, init, true):-t(A, step, 1), t(A, text, ">>=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, ">>=").

% Rule: rule_more_priority_left_by_step_app []
	t(A, more_priority_left_by_step, C):-t(A, more_priority_left_by_step, B), t(B, prev_index, C), t(C, app, true).

% Rule: rule_operator_binary& []
	t(A, precedence, 11):-t(A, text, "&"), t(A, step, 1), t(A, prev_operand, B).
	t(A, associativity, "L"):-t(A, text, "&"), t(A, step, 1), t(A, prev_operand, B).
	t(A, arity, "binary"):-t(A, text, "&"), t(A, step, 1), t(A, prev_operand, B).
	t(A, init, true):-t(A, text, "&"), t(A, step, 1), t(A, prev_operand, B).

% Rule: rule_before_function_call []
	t(B, before_direct, A):-t(A, has_operand, B), t(B, text, "<(>"), t(B, is_function_call, true).
	t(B, before_as_operand, A):-t(A, has_operand, B), t(B, text, "<(>"), t(B, is_function_call, true).

% Rule: rule_more_priority_left_by_step_eval []
	t(A, more_priority_left_by_step, C):-t(A, more_priority_left_by_step, B), t(B, prev_index, C), t(C, eval, true).

% Rule: rule_more_priority_left_by_step_first []
	t(A, more_priority_left_by_step, A):-t(A, precedence, A_PRIOR), t(A, init, true).

% Rule: rule_operator? []
	t(A, arity, "ternary"):-t(A, step, 1), t(A, text, "?").
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "?").
	t(A, is_operator_with_strict_operands_order, true):-t(A, step, 1), t(A, text, "?").
	t(A, init, true):-t(A, step, 1), t(A, text, "?").
	t(A, complex_beginning, true):-t(A, step, 1), t(A, text, "?").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "?").

% Rule: rule_more_priority_left_by_step_operand []
	t(A, more_priority_left_by_step, C):-t(A, more_priority_left_by_step, B), t(B, prev_index, C), t(C, is_operand, true).

% Rule: rule_eval_complex_operation_copy_other_right []
	t(OTHER, copy, OTHER_NEXT):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(A, next_step, A_NEXT), t(C, not_index, OTHER), t(A, same_step, C), t(OTHER, index, OTHER_INDEX), t(A, index, A_INDEX), OTHER_INDEX > C_INDEX.

% Rule: rule_more_priority_right_by_step []
	t(A, more_priority_right_by_step, C):-t(A, more_priority_right_by_step, B), t(B, next_index, C), t(A, high_priority, C).

% Rule: rule_operator^ []
	t(A, precedence, 12):-t(A, step, 1), t(A, text, "^").
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "^").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "^").
	t(A, init, true):-t(A, step, 1), t(A, text, "^").

% Rule: rule_eval_complex_operation_copy_others_left_no_function_name []
	t(OTHER, copy, OTHER_NEXT):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, find_left_operand, D), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(A, next_step, A_NEXT), t(A, is_function_call, true), t(D, not_index, OTHER), t(C, not_index, OTHER), t(A, same_step, C), t(OTHER, index, OTHER_INDEX), t(A, index, A_INDEX), OTHER_INDEX < A_INDEX.

% Rule: rule_more_priority_right_by_step_app []
	t(A, more_priority_right_by_step, C):-t(A, more_priority_right_by_step, B), t(B, next_index, C), t(C, app, true).

% Rule: rule_eval_complex_operation_copy_other_left []
	t(OTHER, copy, OTHER_NEXT):-t(C, next_step, C_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, complex_boundaries, C), t(C, index, C_INDEX), t(A, all_eval_to_right, B), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(A, next_step, A_NEXT), t(C, not_index, OTHER), t(A, is_function_call, false), t(A, same_step, C), t(OTHER, index, OTHER_INDEX), t(A, index, A_INDEX), OTHER_INDEX < A_INDEX.

% Rule: rule_more_priority_right_by_step_eval []
	t(A, more_priority_right_by_step, C):-t(A, more_priority_right_by_step, B), t(B, next_index, C), t(C, eval, true).

% Rule: rule_operator^= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "^=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "^=").
	t(A, init, true):-t(A, step, 1), t(A, text, "^=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "^=").

% Rule: rule_before_before []
	t(A, before, C):-t(A, before, B), t(B, before, C).

% Rule: rule_more_priority_right_by_step_first []
	t(A, more_priority_right_by_step, A):-t(A, precedence, A_PRIOR), t(A, init, true).

% Rule: rule_operator_binary* []
	t(A, associativity, "L"):-t(A, text, "*"), t(A, step, 1), t(A, prev_operand, B).
	t(A, arity, "binary"):-t(A, text, "*"), t(A, step, 1), t(A, prev_operand, B).
	t(A, precedence, 5):-t(A, text, "*"), t(A, step, 1), t(A, prev_operand, B).
	t(A, init, true):-t(A, text, "*"), t(A, step, 1), t(A, prev_operand, B).

% Rule: rule_more_priority_right_by_step_operand []
	t(A, more_priority_right_by_step, C):-t(A, more_priority_right_by_step, B), t(B, next_index, C), t(C, is_operand, true).

% Rule: rule_operator_binary+ []
	t(A, associativity, "L"):-t(A, text, "+"), t(A, step, 1), t(A, prev_operand, B).
	t(A, arity, "binary"):-t(A, text, "+"), t(A, step, 1), t(A, prev_operand, B).
	t(A, init, true):-t(A, text, "+"), t(A, step, 1), t(A, prev_operand, B).
	t(A, precedence, 6):-t(A, text, "+"), t(A, step, 1), t(A, prev_operand, B).

% Rule: rule_operator += []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "+=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "+=").
	t(A, init, true):-t(A, step, 1), t(A, text, "+=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "+=").

% Rule: rule_operator_binary- []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "-"), t(A, prev_operand, B).
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "-"), t(A, prev_operand, B).
	t(A, init, true):-t(A, step, 1), t(A, text, "-"), t(A, prev_operand, B).
	t(A, precedence, 6):-t(A, step, 1), t(A, text, "-"), t(A, prev_operand, B).

% Rule: rule_operator_function_call []
	t(A, associativity, "L"):-t(A, text, "<(>"), t(A, prev_operand, B).
	t(A, arity, "complex"):-t(A, text, "<(>"), t(A, prev_operand, B).
	t(A, init, true):-t(A, text, "<(>"), t(A, prev_operand, B).
	t(A, is_function_call, true):-t(A, text, "<(>"), t(A, prev_operand, B).
	t(A, precedence, 2):-t(A, text, "<(>"), t(A, prev_operand, B).

% Rule: rule_eval_function_name []
	t(FUNCTION_NAME, copy_without_marks, FUNCTION_NAME_NEXT):-t(FUNCTION_NAME, next_step, FUNCTION_NAME_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, find_left_operand, FUNCTION_NAME), t(A, same_step, FUNCTION_NAME), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, is_function_call, true), t(A, same_step, C), t(A, complex_boundaries, C).
	t(FUNCTION_NAME_NEXT, app, true):-t(FUNCTION_NAME, next_step, FUNCTION_NAME_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, find_left_operand, FUNCTION_NAME), t(A, same_step, FUNCTION_NAME), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, is_function_call, true), t(A, same_step, C), t(A, complex_boundaries, C).
	t(A, has_complex_operator_part, FUNCTION_NAME):-t(FUNCTION_NAME, next_step, FUNCTION_NAME_NEXT), t(B, next_index, C), t(A, has_highest_priority_to_right, true), t(A, all_eval_to_right, B), t(A, find_left_operand, FUNCTION_NAME), t(A, same_step, FUNCTION_NAME), t(A, arity, "complex"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, is_function_call, true), t(A, same_step, C), t(A, complex_boundaries, C).

% Rule: rule_next_prev []
	t(A, next_index, B):-t(A, index, A_INDEX), B_INDEX = A_INDEX + 1, t(B, index, B_INDEX), t(A, same_step, B).
	t(B, prev_index, A):-t(A, index, A_INDEX), B_INDEX = A_INDEX + 1, t(B, index, B_INDEX), t(A, same_step, B).

% Rule: rule_operator_postfix++ []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "++"), t(A, prev_operand, B).
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "++"), t(A, prev_operand, B).
	t(A, init, true):-t(A, step, 1), t(A, text, "++"), t(A, prev_operand, B).
	t(A, prefix_postfix, "postfix"):-t(A, step, 1), t(A, text, "++"), t(A, prev_operand, B).
	t(A, precedence, 2):-t(A, step, 1), t(A, text, "++"), t(A, prev_operand, B).

% Rule: rule_operator_postfix-- []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "--"), t(A, prev_operand, B).
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "--"), t(A, prev_operand, B).
	t(A, init, true):-t(A, step, 1), t(A, text, "--"), t(A, prev_operand, B).
	t(A, prefix_postfix, "postfix"):-t(A, step, 1), t(A, text, "--"), t(A, prev_operand, B).
	t(A, precedence, 2):-t(A, step, 1), t(A, text, "--"), t(A, prev_operand, B).

% Rule: rule_next_step []
	t(A, next_step, B):-t(A, index, A_INDEX), t(B, index, A_INDEX), t(A, step, A_STEP), B_STEP = A_STEP + 1, t(B, step, B_STEP).

% Rule: rule_operator_prefix++ []
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "++"), t(A, prev_operation, B).
	t(A, init, true):-t(A, step, 1), t(A, text, "++"), t(A, prev_operation, B).
	t(A, prefix_postfix, "prefix"):-t(A, step, 1), t(A, text, "++"), t(A, prev_operation, B).
	t(A, precedence, 3):-t(A, step, 1), t(A, text, "++"), t(A, prev_operation, B).
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "++"), t(A, prev_operation, B).

% Rule: rule_operator_prefix-- []
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "--"), t(A, prev_operation, B).
	t(A, init, true):-t(A, step, 1), t(A, text, "--"), t(A, prev_operation, B).
	t(A, prefix_postfix, "prefix"):-t(A, step, 1), t(A, text, "--"), t(A, prev_operation, B).
	t(A, precedence, 3):-t(A, step, 1), t(A, text, "--"), t(A, prev_operation, B).
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "--"), t(A, prev_operation, B).

% Rule: rule_not_index []
	t(B, not_index, A):-t(A, index, A_INDEX), t(B, index, B_INDEX), A_INDEX != B_INDEX, t(A, same_step, B).
	t(A, not_index, B):-t(A, index, A_INDEX), t(B, index, B_INDEX), A_INDEX != B_INDEX, t(A, same_step, B).

% Rule: rule_operator_subscript []
	t(A, associativity, "L"):-t(A, text, "["), t(A, step, 1).
	t(A, arity, "complex"):-t(A, text, "["), t(A, step, 1).
	t(A, init, true):-t(A, text, "["), t(A, step, 1).
	t(A, complex_beginning, true):-t(A, text, "["), t(A, step, 1).
	t(A, is_function_call, true):-t(A, text, "["), t(A, step, 1).
	t(A, precedence, 2):-t(A, text, "["), t(A, step, 1).

% Rule: rule_eval_postfix_operation_copy_others []
	t(OTHER, copy, OTHER_NEXT):-t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(OTHER, next_step, OTHER_NEXT), t(A, same_step, OTHER), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(A, prefix_postfix, "postfix"), t(A, same_step, B).

% Rule: rule_operator_unary* []
	t(A, arity, "unary"):-t(A, text, "*"), t(A, step, 1), t(A, prev_operation, B).
	t(A, init, true):-t(A, text, "*"), t(A, step, 1), t(A, prev_operation, B).
	t(A, prefix_postfix, "prefix"):-t(A, text, "*"), t(A, step, 1), t(A, prev_operation, B).
	t(A, precedence, 3):-t(A, text, "*"), t(A, step, 1), t(A, prev_operation, B).
	t(A, associativity, "R"):-t(A, text, "*"), t(A, step, 1), t(A, prev_operation, B).

% Rule: rule_eval_prefix_operation []
	t(A, copy_without_marks, A_NEXT):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(A, prefix_postfix, "prefix"), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, find_right_operand, B), t(A, same_step, B).
	t(B_NEXT, app, true):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(A, prefix_postfix, "prefix"), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, find_right_operand, B), t(A, same_step, B).
	t(A, eval_step, A_STEP):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(A, prefix_postfix, "prefix"), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, find_right_operand, B), t(A, same_step, B).
	t(A_NEXT, eval, true):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(A, prefix_postfix, "prefix"), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, find_right_operand, B), t(A, same_step, B).
	t(B, copy_without_marks, B_NEXT):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(A, prefix_postfix, "prefix"), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, find_right_operand, B), t(A, same_step, B).
	t(A, has_operand, B):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(A, prefix_postfix, "prefix"), t(A, has_highest_priority_to_left, true), t(A, next_step, A_NEXT), t(A, find_right_operand, B), t(A, same_step, B).

% Rule: rule_operator-gt []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "->").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "->").
	t(A, init, true):-t(A, step, 1), t(A, text, "->").
	t(A, precedence, 2):-t(A, step, 1), t(A, text, "->").

% Rule: rule_operator_unary+ []
	t(A, arity, "unary"):-t(A, text, "+"), t(A, step, 1), t(A, prev_operation, B).
	t(A, init, true):-t(A, text, "+"), t(A, step, 1), t(A, prev_operation, B).
	t(A, prefix_postfix, "prefix"):-t(A, text, "+"), t(A, step, 1), t(A, prev_operation, B).
	t(A, precedence, 3):-t(A, text, "+"), t(A, step, 1), t(A, prev_operation, B).
	t(A, associativity, "R"):-t(A, text, "+"), t(A, step, 1), t(A, prev_operation, B).

% Rule: rule_eval_postfix_operation []
	t(A, copy_without_marks, A_NEXT):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, prefix_postfix, "postfix"), t(A, next_step, A_NEXT), t(A, same_step, B).
	t(B_NEXT, app, true):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, prefix_postfix, "postfix"), t(A, next_step, A_NEXT), t(A, same_step, B).
	t(A, eval_step, A_STEP):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, prefix_postfix, "postfix"), t(A, next_step, A_NEXT), t(A, same_step, B).
	t(A_NEXT, eval, true):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, prefix_postfix, "postfix"), t(A, next_step, A_NEXT), t(A, same_step, B).
	t(B, copy_without_marks, B_NEXT):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, prefix_postfix, "postfix"), t(A, next_step, A_NEXT), t(A, same_step, B).
	t(A, has_operand, B):-t(B, next_step, B_NEXT), t(A, has_highest_priority_to_right, true), t(A, find_left_operand, B), t(A, step, A_STEP), t(A, arity, "unary"), t(A, init, true), t(A, has_highest_priority_to_left, true), t(A, prefix_postfix, "postfix"), t(A, next_step, A_NEXT), t(A, same_step, B).

% Rule: rule_operator! []
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "!").
	t(A, init, true):-t(A, step, 1), t(A, text, "!").
	t(A, prefix_postfix, "prefix"):-t(A, step, 1), t(A, text, "!").
	t(A, precedence, 3):-t(A, step, 1), t(A, text, "!").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "!").

% Rule: rule_operator_unary- []
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "-"), t(A, prev_operation, B).
	t(A, init, true):-t(A, step, 1), t(A, text, "-"), t(A, prev_operation, B).
	t(A, prefix_postfix, "prefix"):-t(A, step, 1), t(A, text, "-"), t(A, prev_operation, B).
	t(A, precedence, 3):-t(A, step, 1), t(A, text, "-"), t(A, prev_operation, B).
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "-"), t(A, prev_operation, B).

% Rule: rule_eval_operand_in_complex []
	t(A, eval, true):-t(A, init, true), t(A, in_complex, B), t(A, is_operand, true).

% Rule: rule_prev_operand []
	t(A, prev_operand, B):-t(A, prev_index, B), t(B, text, B_TEXT), t(B, is_operand, true), t(B, step, 1).

% Rule: rule_operator!= []
	t(A, precedence, 10):-t(A, step, 1), t(A, text, "!=").
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "!=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "!=").
	t(A, init, true):-t(A, step, 1), t(A, text, "!=").

% Rule: rule_ast_edge_has_complex_operator_part []
	t(A, ast_edge, B):-t(A, has_complex_operator_part, B).

% Rule: rule_operator. []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, ".").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, ".").
	t(A, init, true):-t(A, step, 1), t(A, text, ".").
	t(A, precedence, 2):-t(A, step, 1), t(A, text, ".").

% Rule: rule_operator| []
	t(A, precedence, 13):-t(A, step, 1), t(A, text, "|").
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "|").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "|").
	t(A, init, true):-t(A, step, 1), t(A, text, "|").

% Rule: rule_operator% []
	t(A, associativity, "L"):-t(A, text, "%"), t(A, step, 1).
	t(A, arity, "binary"):-t(A, text, "%"), t(A, step, 1).
	t(A, precedence, 5):-t(A, text, "%"), t(A, step, 1).
	t(A, init, true):-t(A, text, "%"), t(A, step, 1).

% Rule: rule_all_eval_to_right_begin []
	t(A, all_eval_to_right, A):-t(A, has_highest_priority_to_right, true), t(A, init, true), t(A, complex_beginning, true), t(A, has_highest_priority_to_left, true).

% Rule: rule_operator|= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "|=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "|=").
	t(A, init, true):-t(A, step, 1), t(A, text, "|=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "|=").

% Rule: rule_operator%= []
	t(A, precedence, 16):-t(A, text, "%="), t(A, step, 1).
	t(A, arity, "binary"):-t(A, text, "%="), t(A, step, 1).
	t(A, init, true):-t(A, text, "%="), t(A, step, 1).
	t(A, associativity, "R"):-t(A, text, "%="), t(A, step, 1).

% Rule: rule_operator|| []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "||").
	t(A, precedence, 15):-t(A, step, 1), t(A, text, "||").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "||").
	t(A, is_operator_with_strict_operands_order, true):-t(A, step, 1), t(A, text, "||").
	t(A, init, true):-t(A, step, 1), t(A, text, "||").

% Rule: rule_eval_prefix_operation_copy_others []
	t(OTHER, copy, OTHER_NEXT):-t(A, has_highest_priority_to_right, true), t(A, arity, "unary"), t(A, init, true), t(B, not_index, OTHER), t(OTHER, next_step, OTHER_NEXT), t(A, prefix_postfix, "prefix"), t(A, same_step, OTHER), t(A, has_highest_priority_to_left, true), t(A, not_index, OTHER), t(A, find_right_operand, B), t(A, same_step, B).

% Rule: rule_operator& []
	t(A, arity, "unary"):-t(A, text, "&"), t(A, step, 1), t(A, prev_operation, B).
	t(A, init, true):-t(A, text, "&"), t(A, step, 1), t(A, prev_operation, B).
	t(A, prefix_postfix, "prefix"):-t(A, text, "&"), t(A, step, 1), t(A, prev_operation, B).
	t(A, precedence, 3):-t(A, text, "&"), t(A, step, 1), t(A, prev_operation, B).
	t(A, associativity, "R"):-t(A, text, "&"), t(A, step, 1), t(A, prev_operation, B).

% Rule: rule_all_app_to_right_begin []
	t(A, all_app_to_right, A):-t(A, has_highest_priority_to_right, true), t(A, init, true).

% Rule: rule_operator~ []
	t(A, arity, "unary"):-t(A, step, 1), t(A, text, "~").
	t(A, init, true):-t(A, step, 1), t(A, text, "~").
	t(A, prefix_postfix, "prefix"):-t(A, step, 1), t(A, text, "~").
	t(A, precedence, 3):-t(A, step, 1), t(A, text, "~").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "~").

% Rule: rule_before_in_complex []
	t(C, before_direct, A):-t(A, has_operand, B), t(B, text, "<(>"), t(B, has_operand, C).
	t(C, before_by_third_operator, A):-t(A, has_operand, B), t(B, text, "<(>"), t(B, has_operand, C).
	t(C, before_third_operator, B):-t(A, has_operand, B), t(B, text, "<(>"), t(B, has_operand, C).

% Rule: rule_operator&& []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "&&").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "&&").
	t(A, is_operator_with_strict_operands_order, true):-t(A, step, 1), t(A, text, "&&").
	t(A, precedence, 14):-t(A, step, 1), t(A, text, "&&").
	t(A, init, true):-t(A, step, 1), t(A, text, "&&").

% Rule: rule_prev_operand_unary_postfix []
	t(A, prev_operand, B):-t(A, prev_index, B), t(B, arity, "unary"), t(B, prefix_postfix, "postfix"), t(B, step, 1).

% Rule: rule_prev_operation []
	t(A, prev_operation, B):-t(A, prev_index, B), t(B, arity, B_ARITY), B_ARITY != "unary", t(B, step, 1).

% Rule: rule_operator&= []
	t(A, precedence, 16):-t(A, text, "&="), t(A, step, 1).
	t(A, arity, "binary"):-t(A, text, "&="), t(A, step, 1).
	t(A, init, true):-t(A, text, "&="), t(A, step, 1).
	t(A, associativity, "R"):-t(A, text, "&="), t(A, step, 1).

% Rule: rule_prev_operation_beggining []
	t(A, prev_operation, A):-t(A, step, 1), t(A, index, 1).

% Rule: rule_prev_operation_unary_prefix []
	t(A, prev_operation, B):-t(A, prev_index, B), t(B, arity, "unary"), t(B, prefix_postfix, "prefix"), t(B, step, 1).

% Rule: rule_operator( []
	t(A, associativity, "L"):-t(A, text, "<(>"), t(A, step, 1), t(A, prev_operation, B).
	t(A, precedence, 0):-t(A, text, "<(>"), t(A, step, 1), t(A, prev_operation, B).
	t(A, arity, "complex"):-t(A, text, "<(>"), t(A, step, 1), t(A, prev_operation, B).
	t(A, init, true):-t(A, text, "<(>"), t(A, step, 1), t(A, prev_operation, B).
	t(A, complex_beginning, true):-t(A, text, "<(>"), t(A, step, 1), t(A, prev_operation, B).
	t(A, is_function_call, false):-t(A, text, "<(>"), t(A, step, 1), t(A, prev_operation, B).

% Rule: rule_describe_error []
	t(A, describe_error, B):-t(B, student_pos_less, A), t(A, before_direct, B).

% Rule: rule_all_eval_to_right []
	t(A, all_eval_to_right, C):-t(A, all_eval_to_right, B), t(B, next_index, C), t(C, eval, true).

% Rule: rule_operator*= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "*=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "*=").
	t(A, init, true):-t(A, step, 1), t(A, text, "*=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "*=").

% Rule: rule_same_step []
	t(A, same_step, B):-t(A, step, A_STEP), t(B, step, A_STEP).

% Rule: rule_eval_ternary_operation_copy_inner_eval []
	t(OTHER, copy_without_marks, OTHER_NEXT):-t(C, index, C_INDEX), t(A, arity, "ternary"), t(A, step, A_STEP), t(OTHER, step, A_STEP), t(A, eval_step, A_STEP), t(OTHER, next_step, OTHER_NEXT), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, complex_boundaries, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX, t(OTHER, eval, true).
	t(OTHER_NEXT, app, true):-t(C, index, C_INDEX), t(A, arity, "ternary"), t(A, step, A_STEP), t(OTHER, step, A_STEP), t(A, eval_step, A_STEP), t(OTHER, next_step, OTHER_NEXT), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, complex_boundaries, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX, t(OTHER, eval, true).
	t(A, has_operand, OTHER):-t(C, index, C_INDEX), t(A, arity, "ternary"), t(A, step, A_STEP), t(OTHER, step, A_STEP), t(A, eval_step, A_STEP), t(OTHER, next_step, OTHER_NEXT), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, complex_boundaries, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX, t(OTHER, eval, true).

% Rule: rule_student_error_in_complex []
	t(B, student_error_in_complex, A):-t(A, before_by_third_operator, B), t(A, before_third_operator, C), t(C, text, "<(>"), t(A, describe_error, B).

% Rule: rule_eval_ternary_operation_copy_inner_app []
	t(OTHER, copy_without_marks, OTHER_NEXT):-t(C, index, C_INDEX), t(A, arity, "ternary"), t(A, step, A_STEP), t(OTHER, step, A_STEP), t(A, eval_step, A_STEP), t(OTHER, app, true), t(OTHER, next_step, OTHER_NEXT), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, complex_boundaries, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX.
	t(OTHER_NEXT, app, true):-t(C, index, C_INDEX), t(A, arity, "ternary"), t(A, step, A_STEP), t(OTHER, step, A_STEP), t(A, eval_step, A_STEP), t(OTHER, app, true), t(OTHER, next_step, OTHER_NEXT), t(OTHER, index, OTHER_INDEX), OTHER_INDEX < C_INDEX, t(A, complex_boundaries, C), t(A, index, A_INDEX), A_INDEX < OTHER_INDEX.

% Rule: rule_operator, []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "<,>").
	t(A, precedence, 17):-t(A, step, 1), t(A, text, "<,>").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "<,>").
	t(A, is_operator_with_strict_operands_order, true):-t(A, step, 1), t(A, text, "<,>").
	t(A, init, true):-t(A, step, 1), t(A, text, "<,>").

% Rule: rule_all_app_to_right []
	t(A, all_app_to_right, C):-t(A, all_app_to_right, B), t(B, next_index, C), t(C, app, true).

% Rule: rule_student_error_in_complex_bound []
	t(B, student_error_in_complex, A):-t(A, before_as_operand, B), t(B, complex_beginning, true), t(A, describe_error, B).

% Rule: rule_student_error_left_assoc []
	t(B, student_error_left_assoc, A):-t(A, before_as_operand, B), t(A, describe_error, B), t(A, high_priority_left_assoc, B).

% Rule: rule_operator-= []
	t(A, precedence, 16):-t(A, step, 1), t(A, text, "-=").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "-=").
	t(A, init, true):-t(A, step, 1), t(A, text, "-=").
	t(A, associativity, "R"):-t(A, step, 1), t(A, text, "-=").

% Rule: rule_student_error_more_priority []
	t(B, student_error_more_priority, A):-t(A, before_as_operand, B), t(A, describe_error, B), t(A, high_priority_diff_priority, B).

% Rule: rule_operator/ []
	t(A, associativity, "L"):-t(A, step, 1), t(A, text, "/").
	t(A, arity, "binary"):-t(A, step, 1), t(A, text, "/").
	t(A, precedence, 5):-t(A, step, 1), t(A, text, "/").
	t(A, init, true):-t(A, step, 1), t(A, text, "/").

% Rule: rule_student_error_right_assoc []
	t(B, student_error_right_assoc, A):-t(A, before_as_operand, B), t(A, describe_error, B), t(A, high_priority_right_assoc, B).

% Rule: rule_all_eval_to_right_app []
	t(A, all_eval_to_right, C):-t(A, all_eval_to_right, B), t(B, next_index, C), t(C, app, true).

% Rule: rule_all_app_to_left_begin []
	t(A, all_app_to_left, A):-t(A, init, true), t(A, has_highest_priority_to_left, true).
