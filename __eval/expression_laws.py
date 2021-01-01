# expression_laws.py

import types
from owlready2 import *

from ctrlstrct_swrl import DomainRule
from ctrlstrct_run import prepare_name


if True:

    def getOWLLawFormulation(*args):
        return tuple(args)
    
    def getSWRLLawFormulation(name, swrl):
        # Jena "(" workaround
        swrl = swrl.replace('"("', '"<(>"')
        swrl = swrl.replace('","', '"<,>"')

        swrl = swrl.replace(' ^ ', ', ')
        swrl = swrl.replace('swrlb:', '')
        name = name.replace('>', 'gt')
        name = name.replace('<', 'lt')
        name = 'rule_' + name
        return DomainRule(name=prepare_name(name), swrl=swrl)

# '''
    # List<LawFormulation> getSWRLBackendBaseLaws() {
    def getSWRLBackendBaseLaws():
    #     List<LawFormulation> laws = new ArrayList<>();
        laws = set()
        laws.add(getOWLLawFormulation("zero_step", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("all_app_to_left", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("all_app_to_right", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("all_eval_to_right", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("ast_edge", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_all_operands", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_as_operand", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_by_third_operator", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_direct", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_third_operator", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("complex_boundaries", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("copy", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("copy_without_marks", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("describe_error", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("find_left_operand", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("find_right_operand", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("has_complex_operator_part", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("has_operand", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority_diff_priority", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority_left_assoc", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority_right_assoc", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("in_complex", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("more_priority_left_by_step", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("more_priority_right_by_step", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("next_index", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("next_step", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("not_index", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("prev_index", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("prev_operand", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("prev_operation", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("same_step", "owl:ObjectProperty"));

        laws.add(getOWLLawFormulation("app", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("arity", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("associativity", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("complex_beginning", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("complex_ending", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("error_description", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("eval", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("eval_step", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("has_highest_priority_to_left", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("has_highest_priority_to_right", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("index", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("init", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("is_function_call", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("is_operand", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("is_operator_with_strict_operands_order", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("last", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("precedence", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("prefix_postfix", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("real_pos", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("step", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("student_pos", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("text", "owl:DatatypeProperty"));

        return laws;
    # }

    # public List<LawFormulation> getAllLaws() {
    def getAllLaws():
        # List<LawFormulation> laws = getSWRLBackendBaseLaws();
        laws = getSWRLBackendBaseLaws();
        laws.add(getSWRLLawFormulation(
                "zero_step",
                "index(?a, ?a_index) ^ index(?b, ?a_index) ^ step(?b, 0) -> zero_step(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_app_to_left",
                "all_app_to_left(?a, ?b) ^ prev_index(?b, ?c) ^ app(?c, true) -> all_app_to_left(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_app_to_left_begin",
                "init(?a, true) ^ has_highest_priority_to_left(?a, true) -> all_app_to_left(?a, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_app_to_right",
                "all_app_to_right(?a, ?b) ^ next_index(?b, ?c) ^ app(?c, true) -> all_app_to_right(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_app_to_right_begin",
                "has_highest_priority_to_right(?a, true) ^ init(?a, true) -> all_app_to_right(?a, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_eval_to_right",
                "all_eval_to_right(?a, ?b) ^ next_index(?b, ?c) ^ eval(?c, true) -> all_eval_to_right(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_eval_to_right_app",
                "all_eval_to_right(?a, ?b) ^ next_index(?b, ?c) ^ app(?c, true) -> all_eval_to_right(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "all_eval_to_right_begin",
                "has_highest_priority_to_right(?a, true) ^ init(?a, true) ^ complex_beginning(?a, true) ^ has_highest_priority_to_left(?a, true) -> all_eval_to_right(?a, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "ast_edge_has_complex_operator_part",
                "has_complex_operator_part(?a, ?b) -> ast_edge(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "ast_edge_has_operand",
                "has_operand(?a, ?b) -> ast_edge(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "before",
                "has_operand(?a, ?b) ^ text(?b, ?b_text) ^ swrlb:notEqual(?b_text, \"(\") -> before_direct(?b, ?a) ^ before_as_operand(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_all_operands",
                "before_all_operands(?a, ?b) ^ has_operand(?b, ?c) -> before_direct(?a, ?c) ^ before_by_third_operator(?a, ?c) ^ before_all_operands(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_before",
                "before(?a, ?b) ^ before(?b, ?c) -> before(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_direct",
                "before_direct(?a, ?b) -> before(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_function_call",
                "has_operand(?a, ?b) ^ text(?b, \"(\") ^ is_function_call(?b, true) -> before_direct(?b, ?a) ^ before_as_operand(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_in_complex",
                "has_operand(?a, ?b) ^ text(?b, \"(\") ^ has_operand(?b, ?c) -> before_direct(?c, ?a) ^ before_by_third_operator(?c, ?a) ^ before_third_operator(?c, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_strict_order_operands",
                "is_operator_with_strict_operands_order(?a, true) ^ text(?a, ?a_text) ^ swrlb:notEqual(?a_text, \"?\") ^ has_operand(?a, ?b) ^ has_operand(?a, ?c) ^ index(?b, ?b_index) ^ index(?c, ?c_index) ^ swrlb:lessThan(?b_index, ?c_index) -> before_direct(?b, ?c) ^ before_all_operands(?b, ?c) ^ before_by_third_operator(?b, ?c) ^ before_third_operator(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "before_strict_order_operands_ternary",
                "text(?a, \"?\") ^ has_operand(?a, ?b) ^ has_operand(?a, ?c) ^ has_operand(?a, ?d) ^ index(?b, ?b_index) ^ index(?c, ?c_index) ^ index(?d, ?d_index) ^ not_index(?c, ?d) ^ swrlb:lessThan(?b_index, ?c_index) ^ swrlb:lessThan(?b_index, ?d_index) -> before_direct(?b, ?c) ^ before_all_operands(?b, ?c) ^ before_by_third_operator(?b, ?c) ^ before_third_operator(?b, ?a)"
        ));
# //        laws.add(getLawFormulation(
# //                "complex_beggining_false",
# //                "swrlb:notEqual(?a_text, \"(\") ^ swrlb:notEqual(?a_text, \"[\") ^ swrlb:notEqual(?a_text, \"?\") ^ text(?a, ?a_text) ^ step(?a, 0) -> complex_beginning(?a, false)"
# //        ));
# //        laws.add(getLawFormulation(
# //                "complex_beginning(",
# //                "text(?a, \"(\") ^ step(?a, 0) -> complex_beginning(?a, true)"
# //        ));
# //        laws.add(getLawFormulation(
# //                "complex_beginning?",
# //                "text(?a, \"?\") ^ step(?a, 0) -> complex_beginning(?a, true)"
# //        ));
# //        laws.add(getLawFormulation(
# //                "complex_beginning[",
# //                "text(?a, \"[\") ^ step(?a, 0) -> complex_beginning(?a, true)"
# //        ));
        laws.add(getSWRLLawFormulation(
                "complex_boundaries",
                "in_complex(?a, ?c) ^ next_index(?a, ?b) ^ complex_beginning(?a, false) ^ complex_ending(?b, true) ^ step(?a, 0) -> complex_boundaries(?c, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "complex_boundaries_empty",
                "next_index(?a, ?b) ^ step(?a, 0) ^ complex_beginning(?a, true) ^ complex_ending(?b, true) -> complex_boundaries(?a, ?b)"
        ));
# //        laws.add(getLawFormulation(
# //                "complex_ending)",
# //                "text(?a, \")\") ^ step(?a, 0) -> complex_ending(?a, true)"
# //        ));
# //        laws.add(getLawFormulation(
# //                "complex_ending:",
# //                "text(?a, \":\") ^ step(?a, 0) -> complex_ending(?a, true)"
# //        ));
# //        laws.add(getLawFormulation(
# //                "complex_ending]",
# //                "text(?a, \"]\") ^ step(?a, 0) -> complex_ending(?a, true)"
# //        ));
# //        laws.add(getLawFormulation(
# //                "complex_ending_false",
# //                "text(?a, ?a_text) ^ swrlb:notEqual(?a_text, \")\") ^ swrlb:notEqual(?a_text, \"]\") ^ swrlb:notEqual(?a_text, \":\") ^ step(?a, 0) -> complex_ending(?a, false)"
# //        ));
        laws.add(getSWRLLawFormulation(
                "copy_app",
                "copy(?a, ?to) ^ app(?a, true) -> app(?to, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_eval",
                "copy(?a, ?to) ^ eval(?a, true) -> eval(?to, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_eval_step_to_zero_step",
                "eval_step(?a, ?a_step) ^ zero_step(?a, ?a0) -> eval_step(?a0, ?a_step)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_has_complex_operator_part_to_zero_step",
                "has_complex_operator_part(?a, ?b) ^ zero_step(?a, ?a0) ^ zero_step(?b, ?b0) -> has_complex_operator_part(?a0, ?b0)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_has_operand_to_zero_step",
                "has_operand(?a, ?b) ^ zero_step(?a, ?a0) ^ zero_step(?b, ?b0) -> has_operand(?a0, ?b0)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_init",
                "copy(?a, ?to) ^ init(?a, true) -> init(?to, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_to_zero_step",
                "step(?a, 0) ^ step(?b, 1) ^ zero_step(?b, ?a) -> copy_without_marks(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_to_1_step",
                "step(?a, 0) ^ step(?b, 1) ^ zero_step(?b, ?a) -> copy(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks",
                "copy(?a, ?to) -> copy_without_marks(?a, ?to)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_arity",
                "arity(?a, ?a_arity) ^ copy_without_marks(?a, ?to) -> arity(?to, ?a_arity)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_associativity",
                "associativity(?a, ?a_associativity) ^ copy_without_marks(?a, ?to) -> associativity(?to, ?a_associativity)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_complex_beginning",
                "complex_beginning(?a, ?b) ^ copy_without_marks(?a, ?to) -> complex_beginning(?to, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_complex_boundaries",
                "same_step(?c, ?to) ^ copy_without_marks(?a, ?to) ^ complex_boundaries(?a, ?b) ^ zero_step(?c, ?b0) ^ zero_step(?b, ?b0) -> complex_boundaries(?to, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_complex_ending",
                "complex_ending(?a, ?b) ^ copy_without_marks(?a, ?to) -> complex_ending(?to, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_in_complex",
                "same_step(?c, ?to) ^ copy_without_marks(?a, ?to) ^ in_complex(?a, ?b) ^ zero_step(?c, ?b0) ^ zero_step(?b, ?b0) -> in_complex(?to, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_is_function_call",
                "is_function_call(?a, ?a_fc) ^ copy_without_marks(?a, ?to) -> is_function_call(?to, ?a_fc)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_is_operand",
                "copy_without_marks(?a, ?to) ^ is_operand(?a, ?is_op) -> is_operand(?to, ?is_op)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_is_operator_with_strict_operands_order",
                "copy_without_marks(?a, ?to) ^ is_operator_with_strict_operands_order(?a, ?is_op) -> is_operator_with_strict_operands_order(?to, ?is_op)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_last",
                "last(?a, ?a_last) ^ copy_without_marks(?a, ?to) -> last(?to, ?a_last)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_prefix_postfix",
                "prefix_postfix(?a, ?a_pr) ^ copy_without_marks(?a, ?to) -> prefix_postfix(?to, ?a_pr)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_priority",
                "precedence(?a, ?a_priority) ^ copy_without_marks(?a, ?to) -> precedence(?to, ?a_priority)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_real_pos",
                "real_pos(?a, ?a_rp) ^ copy_without_marks(?a, ?to) -> real_pos(?to, ?a_rp)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_student_pos",
                "copy_without_marks(?a, ?to) ^ student_pos(?a, ?a_sp) -> student_pos(?to, ?a_sp)"
        ));
        laws.add(getSWRLLawFormulation(
                "copy_without_marks_text",
                "copy_without_marks(?a, ?to) ^ text(?a, ?a_text) -> text(?to, ?a_text)"
        ));
        laws.add(getSWRLLawFormulation(
                "equal_priority_L_assoc",
                "swrlb:equal(?a_prior, ?b_prior) ^ swrlb:equal(?a_assoc, ?b_assoc) ^ index(?b, ?b_index) ^ precedence(?a, ?a_prior) ^ associativity(?b, ?b_assoc) ^ precedence(?b, ?b_prior) ^ associativity(?a, ?a_assoc) ^ swrlb:equal(?a_assoc, \"L\") ^ index(?a, ?a_index) ^ swrlb:lessThan(?a_index, ?b_index) ^ same_step(?a, ?b) -> high_priority_left_assoc(?a, ?b) ^ high_priority(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "equal_priority_R_assoc",
                "swrlb:equal(?a_prior, ?b_prior) ^ swrlb:equal(?a_assoc, ?b_assoc) ^ index(?b, ?b_index) ^ precedence(?a, ?a_prior) ^ associativity(?b, ?b_assoc) ^ precedence(?b, ?b_prior) ^ associativity(?a, ?a_assoc) ^ swrlb:equal(?a_assoc, \"R\") ^ index(?a, ?a_index) ^ same_step(?a, ?b) ^ swrlb:greaterThan(?a_index, ?b_index) -> high_priority(?a, ?b) ^ high_priority_right_assoc(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_,_in_function_call",
                "text(?a, \",\") ^ init(?a, true) ^ in_complex(?a, ?b) ^ is_function_call(?b, true) -> app(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_binary_operation",
                "next_step(?b, ?b_next) ^ next_step(?c, ?c_next) ^ has_highest_priority_to_right(?a, true) ^ find_left_operand(?a, ?b) ^ step(?a, ?a_step) ^ arity(?a, \"binary\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ find_right_operand(?a, ?c) ^ next_step(?a, ?a_next) ^ same_step(?a, ?c) ^ same_step(?a, ?b) -> has_operand(?a, ?c) ^ copy_without_marks(?a, ?a_next) ^ copy_without_marks(?c, ?c_next) ^ app(?b_next, true) ^ eval_step(?a, ?a_step) ^ app(?c_next, true) ^ eval(?a_next, true) ^ copy_without_marks(?b, ?b_next) ^ has_operand(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_binary_operation_copy_other",
                "has_highest_priority_to_right(?a, true) ^ arity(?a, \"binary\") ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ find_right_operand(?a, ?c) ^ find_left_operand(?a, ?b) ^ init(?a, true) ^ not_index(?b, ?other) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ not_index(?c, ?other) ^ same_step(?a, ?c) ^ same_step(?a, ?b) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_complex_operation",
                "next_step(?c, ?c_next) ^ next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ all_eval_to_right(?a, ?b) ^ step(?a, ?a_step) ^ arity(?a, \"complex\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ next_step(?a, ?a_next) ^ same_step(?a, ?c) ^ complex_boundaries(?a, ?c) -> copy_without_marks(?a, ?a_next) ^ copy_without_marks(?c, ?c_next) ^ eval_step(?a, ?a_step) ^ has_complex_operator_part(?a, ?c) ^ app(?c_next, true) ^ eval(?a_next, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_complex_operation_copy_inner_app",
                "next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ complex_boundaries(?a, ?c) ^ index(?c, ?c_index) ^ all_eval_to_right(?a, ?b) ^ arity(?a, \"complex\") ^ app(?other, true) ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ not_index(?c, ?other) ^ index(?other, ?other_index) ^ swrlb:lessThan(?other_index, ?c_index) ^ same_step(?a, ?c) ^ index(?a, ?a_index) ^ swrlb:lessThan(?a_index, ?other_index) -> copy_without_marks(?other, ?other_next) ^ app(?other_next, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_complex_operation_copy_inner_eval",
                "next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ complex_boundaries(?a, ?c) ^ index(?c, ?c_index) ^ all_eval_to_right(?a, ?b) ^ arity(?a, \"complex\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ not_index(?c, ?other) ^ index(?other, ?other_index) ^ swrlb:lessThan(?other_index, ?c_index) ^ same_step(?a, ?c) ^ index(?a, ?a_index) ^ swrlb:lessThan(?a_index, ?other_index) ^ eval(?other, true) -> copy_without_marks(?other, ?other_next) ^ app(?other_next, true) ^ has_operand(?a, ?other)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_complex_operation_copy_other_left",
                "next_step(?c, ?c_next) ^ next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ complex_boundaries(?a, ?c) ^ index(?c, ?c_index) ^ all_eval_to_right(?a, ?b) ^ arity(?a, \"complex\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ next_step(?a, ?a_next) ^ not_index(?c, ?other) ^ is_function_call(?a, false) ^ same_step(?a, ?c) ^ index(?other, ?other_index) ^ index(?a, ?a_index) ^ swrlb:lessThan(?other_index, ?a_index) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_complex_operation_copy_other_right",
                "next_step(?c, ?c_next) ^ next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ complex_boundaries(?a, ?c) ^ index(?c, ?c_index) ^ all_eval_to_right(?a, ?b) ^ arity(?a, \"complex\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ next_step(?a, ?a_next) ^ not_index(?c, ?other) ^ same_step(?a, ?c) ^ index(?other, ?other_index) ^ index(?a, ?a_index) ^ swrlb:greaterThan(?other_index, ?c_index) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_complex_operation_copy_others_left_no_function_name",
                "next_step(?c, ?c_next) ^ next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ complex_boundaries(?a, ?c) ^ index(?c, ?c_index) ^ find_left_operand(?a, ?d) ^ all_eval_to_right(?a, ?b) ^ arity(?a, \"complex\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ next_step(?a, ?a_next) ^ is_function_call(?a, true) ^ not_index(?d, ?other) ^ not_index(?c, ?other) ^ same_step(?a, ?c) ^ index(?other, ?other_index) ^ index(?a, ?a_index) ^ swrlb:lessThan(?other_index, ?a_index) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_function_name",
                "next_step(?function_name, ?function_name_next) ^ next_index(?b, ?c) ^ has_highest_priority_to_right(?a, true) ^ all_eval_to_right(?a, ?b) ^ find_left_operand(?a, ?function_name) ^ same_step(?a, ?function_name) ^ arity(?a, \"complex\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ is_function_call(?a, true) ^ same_step(?a, ?c) ^ complex_boundaries(?a, ?c) -> copy_without_marks(?function_name, ?function_name_next) ^ app(?function_name_next, true) ^ has_complex_operator_part(?a, ?function_name)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_operand_in_complex",
                "init(?a, true) ^ in_complex(?a, ?b) ^ is_operand(?a, true) -> eval(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_postfix_operation",
                "next_step(?b, ?b_next) ^ has_highest_priority_to_right(?a, true) ^ find_left_operand(?a, ?b) ^ step(?a, ?a_step) ^ arity(?a, \"unary\") ^ init(?a, true) ^ has_highest_priority_to_left(?a, true) ^ prefix_postfix(?a, \"postfix\") ^ next_step(?a, ?a_next) ^ same_step(?a, ?b) -> copy_without_marks(?a, ?a_next) ^ app(?b_next, true) ^ eval_step(?a, ?a_step) ^ eval(?a_next, true) ^ copy_without_marks(?b, ?b_next) ^ has_operand(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_postfix_operation_copy_others",
                "has_highest_priority_to_right(?a, true) ^ find_left_operand(?a, ?b) ^ arity(?a, \"unary\") ^ init(?a, true) ^ not_index(?b, ?other) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ prefix_postfix(?a, \"postfix\") ^ same_step(?a, ?b) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_prefix_operation",
                "next_step(?b, ?b_next) ^ has_highest_priority_to_right(?a, true) ^ step(?a, ?a_step) ^ arity(?a, \"unary\") ^ init(?a, true) ^ not_index(?b, ?other) ^ prefix_postfix(?a, \"prefix\") ^ has_highest_priority_to_left(?a, true) ^ next_step(?a, ?a_next) ^ find_right_operand(?a, ?b) ^ same_step(?a, ?b) -> copy_without_marks(?a, ?a_next) ^ app(?b_next, true) ^ eval_step(?a, ?a_step) ^ eval(?a_next, true) ^ copy_without_marks(?b, ?b_next) ^ has_operand(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_prefix_operation_copy_others",
                "has_highest_priority_to_right(?a, true) ^ arity(?a, \"unary\") ^ init(?a, true) ^ not_index(?b, ?other) ^ next_step(?other, ?other_next) ^ prefix_postfix(?a, \"prefix\") ^ same_step(?a, ?other) ^ has_highest_priority_to_left(?a, true) ^ not_index(?a, ?other) ^ find_right_operand(?a, ?b) ^ same_step(?a, ?b) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_ternary_operation",
                "arity(?a, \"ternary\") ^ next_step(?c, ?c_next) ^ next_index(?b, ?c) ^ step(?a, ?a_step) ^ has_highest_priority_to_right(?c, true) ^ find_right_operand(?c, ?e) ^ complex_boundaries(?a, ?c) ^ find_left_operand(?a, ?d) ^ all_eval_to_right(?a, ?b) ^ next_step(?e, ?e_next) ^ init(?a, true) ^ next_step(?d, ?d_next) ^ next_step(?a, ?a_next) ^ has_highest_priority_to_left(?c, true) ^ same_step(?a, ?c) -> has_operand(?a, ?e) ^ copy_without_marks(?d, ?d_next) ^ has_operand(?a, ?d) ^ copy_without_marks(?a, ?a_next) ^ copy_without_marks(?c, ?c_next) ^ copy_without_marks(?e, ?e_next) ^ eval_step(?a, ?a_step) ^ has_complex_operator_part(?a, ?c) ^ app(?c_next, true) ^ app(?d_next, true) ^ app(?e_next, true) ^ eval(?a_next, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_ternary_operation_copy_inner_app",
                "index(?c, ?c_index) ^ arity(?a, \"ternary\") ^ step(?a, ?a_step) ^ step(?other, ?a_step) ^ eval_step(?a, ?a_step) ^ app(?other, true) ^ next_step(?other, ?other_next) ^ index(?other, ?other_index) ^ swrlb:lessThan(?other_index, ?c_index) ^ complex_boundaries(?a, ?c) ^ index(?a, ?a_index) ^ swrlb:lessThan(?a_index, ?other_index) -> copy_without_marks(?other, ?other_next) ^ app(?other_next, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_ternary_operation_copy_inner_eval",
                "index(?c, ?c_index) ^ arity(?a, \"ternary\") ^ step(?a, ?a_step) ^ step(?other, ?a_step) ^ eval_step(?a, ?a_step) ^ next_step(?other, ?other_next) ^ index(?other, ?other_index) ^ swrlb:lessThan(?other_index, ?c_index) ^ complex_boundaries(?a, ?c) ^ index(?a, ?a_index) ^ swrlb:lessThan(?a_index, ?other_index) ^ eval(?other, true) -> copy_without_marks(?other, ?other_next) ^ app(?other_next, true) ^ has_operand(?a, ?other)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_ternary_operation_copy_other_left",
                "arity(?a, \"ternary\") ^ eval_step(?a, ?a_step) ^ step(?a, ?a_step) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ find_left_operand(?a, ?d) ^ not_index(?d, ?other) ^ index(?other, ?other_index) ^ index(?a, ?a_index) ^ swrlb:lessThan(?other_index, ?a_index) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "eval_ternary_operation_copy_other_right",
                "arity(?a, \"ternary\") ^ eval_step(?a, ?a_step) ^ step(?a, ?a_step) ^ next_step(?other, ?other_next) ^ same_step(?a, ?other) ^ complex_boundaries(?a, ?c) ^ find_right_operand(?c, ?d) ^ not_index(?d, ?other) ^ index(?other, ?other_index) ^ index(?c, ?c_index) ^ swrlb:lessThan(?c_index, ?other_index) -> copy(?other, ?other_next)"
        ));
        laws.add(getSWRLLawFormulation(
                "find_left_operand_eval",
                "has_highest_priority_to_right(?a, true) ^ prev_index(?b, ?c) ^ eval(?c, true) ^ has_highest_priority_to_left(?a, true) ^ all_app_to_left(?a, ?b) -> find_left_operand(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "find_left_operand_init",
                "has_highest_priority_to_right(?a, true) ^ prev_index(?b, ?c) ^ has_highest_priority_to_left(?a, true) ^ init(?c, true) ^ all_app_to_left(?a, ?b) -> find_left_operand(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "find_right_operand_eval",
                "has_highest_priority_to_right(?a, true) ^ next_index(?b, ?c) ^ all_app_to_right(?a, ?b) ^ eval(?c, true) ^ has_highest_priority_to_left(?a, true) -> find_right_operand(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "find_right_operand_init",
                "has_highest_priority_to_right(?a, true) ^ next_index(?b, ?c) ^ all_app_to_right(?a, ?b) ^ has_highest_priority_to_left(?a, true) ^ init(?c, true) -> find_right_operand(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_left",
                "more_priority_left_by_step(?a, ?b) ^ index(?b, 1) -> has_highest_priority_to_left(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_left_in_complex_,",
                "prev_index(?b, ?c) ^ in_complex(?a, ?c) ^ text(?a, \",\") ^ is_function_call(?c, false) ^ more_priority_left_by_step(?a, ?b) ^ has_highest_priority_to_left(?c, true) ^ complex_boundaries(?c, ?d) -> has_highest_priority_to_left(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_left_in_complex_not_,",
                "text(?a, ?a_text) ^ swrlb:notEqual(?a_text, \",\") ^ prev_index(?b, ?c) ^ in_complex(?a, ?c) ^ more_priority_left_by_step(?a, ?b) ^ has_highest_priority_to_left(?c, true) -> has_highest_priority_to_left(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_left_ternary",
                "has_highest_priority_to_left(?c, true) ^ complex_boundaries(?c, ?d) -> has_highest_priority_to_left(?d, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_right",
                "more_priority_right_by_step(?a, ?b) ^ last(?b, true) -> has_highest_priority_to_right(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_right_in_complex",
                "next_index(?b, ?d) ^ has_highest_priority_to_right(?c, true) ^ in_complex(?a, ?c) ^ more_priority_right_by_step(?a, ?b) ^ complex_boundaries(?c, ?d) -> has_highest_priority_to_right(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "has_highest_priority_to_right_ternary",
                "has_highest_priority_to_right(?d, true) ^ complex_boundaries(?c, ?d) -> has_highest_priority_to_right(?c, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "high_priority",
                "precedence(?a, ?a_prior) ^ precedence(?b, ?b_prior) ^ swrlb:lessThan(?a_prior, ?b_prior) ^ same_step(?a, ?b) -> high_priority(?a, ?b) ^ high_priority_diff_priority(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "in_complex_begin",
                "next_index(?a, ?b) ^ complex_beginning(?a, true) ^ complex_ending(?b, false) ^ step(?a, 0) -> in_complex(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "in_complex_step",
                "next_index(?a, ?b) ^ step(?a, 0) ^ complex_beginning(?a, false) ^ in_complex(?a, ?c) ^ complex_ending(?b, false) -> in_complex(?b, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "in_complex_step_skip_inner_complex",
                "in_complex(?a, ?c) ^ complex_boundaries(?a, ?d) ^ step(?a, 0) -> in_complex(?d, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "is_operand",
                "text(?a, ?a_text) ^ swrlb:notEqual(?a_text, \"sizeof\") ^ swrlb:matches(?a_text, \"[a-zA-Z_0-9]+\") ^ step(?a, 1) -> init(?a, true) ^ is_operand(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "is_operand_close_bracket",
                "step(?a, 1) ^ text(?a, \"]\") -> init(?a, true) ^ is_operand(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "is_operand_close_parenthesis",
                "text(?a, \")\") ^ step(?a, 1) -> init(?a, true) ^ is_operand(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_left_by_step",
                "more_priority_left_by_step(?a, ?b) ^ prev_index(?b, ?c) ^ high_priority(?a, ?c) -> more_priority_left_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_left_by_step_app",
                "more_priority_left_by_step(?a, ?b) ^ prev_index(?b, ?c) ^ app(?c, true) -> more_priority_left_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_left_by_step_eval",
                "more_priority_left_by_step(?a, ?b) ^ prev_index(?b, ?c) ^ eval(?c, true) -> more_priority_left_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_left_by_step_first",
                "precedence(?a, ?a_prior) ^ init(?a, true) -> more_priority_left_by_step(?a, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_left_by_step_operand",
                "more_priority_left_by_step(?a, ?b) ^ prev_index(?b, ?c) ^ is_operand(?c, true) -> more_priority_left_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_right_by_step",
                "more_priority_right_by_step(?a, ?b) ^ next_index(?b, ?c) ^ high_priority(?a, ?c) -> more_priority_right_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_right_by_step_app",
                "more_priority_right_by_step(?a, ?b) ^ next_index(?b, ?c) ^ app(?c, true) -> more_priority_right_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_right_by_step_eval",
                "more_priority_right_by_step(?a, ?b) ^ next_index(?b, ?c) ^ eval(?c, true) -> more_priority_right_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_right_by_step_first",
                "precedence(?a, ?a_prior) ^ init(?a, true) -> more_priority_right_by_step(?a, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "more_priority_right_by_step_operand",
                "more_priority_right_by_step(?a, ?b) ^ next_index(?b, ?c) ^ is_operand(?c, true) -> more_priority_right_by_step(?a, ?c)"
        ));
        laws.add(getSWRLLawFormulation(
                "next_prev",
                "index(?a, ?a_index) ^ swrlb:add(?b_index, ?a_index, 1) ^ index(?b, ?b_index) ^ same_step(?a, ?b) -> next_index(?a, ?b) ^ prev_index(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "next_step",
                "index(?a, ?a_index) ^ index(?b, ?a_index) ^ step(?a, ?a_step) ^ swrlb:add(?b_step, ?a_step, 1) ^ step(?b, ?b_step) -> next_step(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "not_index",
                "index(?a, ?a_index) ^ index(?b, ?b_index) ^ swrlb:notEqual(?a_index, ?b_index) ^ same_step(?a, ?b) -> not_index(?b, ?a) ^ not_index(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator +=",
                "step(?a, 1) ^ text(?a, \"+=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator!",
                "step(?a, 1) ^ text(?a, \"!\") -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator!=",
                "step(?a, 1) ^ text(?a, \"!=\") -> precedence(?a, 10) ^ associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator%",
                "text(?a, \"%\") ^ step(?a, 1) -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ precedence(?a, 5) ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator%=",
                "text(?a, \"%=\") ^ step(?a, 1) -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator&",
                "text(?a, \"&\") ^ step(?a, 1) ^ prev_operation(?a, ?b) -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator&&",
                "step(?a, 1) ^ text(?a, \"&&\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ is_operator_with_strict_operands_order(?a, true) ^ precedence(?a, 14) ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator&=",
                "text(?a, \"&=\") ^ step(?a, 1) -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator(",
                "text(?a, \"(\") ^ step(?a, 1) ^ prev_operation(?a, ?b) -> associativity(?a, \"L\") ^ precedence(?a, 0) ^ arity(?a, \"complex\") ^ init(?a, true) ^ complex_beginning(?a, true) ^ is_function_call(?a, false)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator*=",
                "step(?a, 1) ^ text(?a, \"*=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator,",
                "step(?a, 1) ^ text(?a, \",\") -> associativity(?a, \"L\") ^ precedence(?a, 17) ^ arity(?a, \"binary\") ^ is_operator_with_strict_operands_order(?a, true) ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator-=",
                "step(?a, 1) ^ text(?a, \"-=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator->",
                "step(?a, 1) ^ text(?a, \"->\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 2)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator.",
                "step(?a, 1) ^ text(?a, \".\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 2)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator/",
                "step(?a, 1) ^ text(?a, \"/\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ precedence(?a, 5) ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator/=",
                "step(?a, 1) ^ text(?a, \"/=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator:",
                "text(?a, \":\") ^ step(?a, 1) -> arity(?a, \"ternary\") ^ precedence(?a, 16) ^ init(?a, true) ^ complex_ending(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator::",
                "step(?a, 1) ^ text(?a, \"::\") -> associativity(?a, \"L\") ^ precedence(?a, 1) ^ arity(?a, \"binary\") ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator<",
                "step(?a, 1) ^ text(?a, \"<\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 9)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator<<",
                "step(?a, 1) ^ text(?a, \"<<\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 7)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator<<=",
                "step(?a, 1) ^ text(?a, \"<<=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator<=",
                "step(?a, 1) ^ text(?a, \"<=\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 9)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator=",
                "step(?a, 1) ^ text(?a, \"=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator==",
                "step(?a, 1) ^ text(?a, \"==\") -> precedence(?a, 10) ^ associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator>",
                "step(?a, 1) ^ text(?a, \">\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 9)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator>=",
                "step(?a, 1) ^ text(?a, \">=\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 9)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator>>",
                "step(?a, 1) ^ text(?a, \">>\") -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 7)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator>>=",
                "step(?a, 1) ^ text(?a, \">>=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator?",
                "step(?a, 1) ^ text(?a, \"?\") -> arity(?a, \"ternary\") ^ precedence(?a, 16) ^ is_operator_with_strict_operands_order(?a, true) ^ init(?a, true) ^ complex_beginning(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator^",
                "step(?a, 1) ^ text(?a, \"^\") -> precedence(?a, 12) ^ associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator^=",
                "step(?a, 1) ^ text(?a, \"^=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_binary&",
                "text(?a, \"&\") ^ step(?a, 1) ^ prev_operand(?a, ?b) -> precedence(?a, 11) ^ associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_binary*",
                "text(?a, \"*\") ^ step(?a, 1) ^ prev_operand(?a, ?b) -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ precedence(?a, 5) ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_binary+",
                "text(?a, \"+\") ^ step(?a, 1) ^ prev_operand(?a, ?b) -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 6)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_binary-",
                "step(?a, 1) ^ text(?a, \"-\") ^ prev_operand(?a, ?b) -> associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true) ^ precedence(?a, 6)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_function_call",
                "text(?a, \"(\") ^ prev_operand(?a, ?b) -> associativity(?a, \"L\") ^ arity(?a, \"complex\") ^ init(?a, true) ^ is_function_call(?a, true) ^ precedence(?a, 2)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_postfix++",
                "step(?a, 1) ^ text(?a, \"++\") ^ prev_operand(?a, ?b) -> associativity(?a, \"L\") ^ arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"postfix\") ^ precedence(?a, 2)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_postfix--",
                "step(?a, 1) ^ text(?a, \"--\") ^ prev_operand(?a, ?b) -> associativity(?a, \"L\") ^ arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"postfix\") ^ precedence(?a, 2)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_prefix++",
                "step(?a, 1) ^ text(?a, \"++\") ^ prev_operation(?a, ?b) -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_prefix--",
                "step(?a, 1) ^ text(?a, \"--\") ^ prev_operation(?a, ?b) -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_subscript",
                "text(?a, \"[\") ^ step(?a, 1) -> associativity(?a, \"L\") ^ arity(?a, \"complex\") ^ init(?a, true) ^ complex_beginning(?a, true) ^ is_function_call(?a, true) ^ precedence(?a, 2)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_unary*",
                "text(?a, \"*\") ^ step(?a, 1) ^ prev_operation(?a, ?b) -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_unary+",
                "text(?a, \"+\") ^ step(?a, 1) ^ prev_operation(?a, ?b) -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator_unary-",
                "step(?a, 1) ^ text(?a, \"-\") ^ prev_operation(?a, ?b) -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator|",
                "step(?a, 1) ^ text(?a, \"|\") -> precedence(?a, 13) ^ associativity(?a, \"L\") ^ arity(?a, \"binary\") ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator|=",
                "step(?a, 1) ^ text(?a, \"|=\") -> precedence(?a, 16) ^ arity(?a, \"binary\") ^ init(?a, true) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "operator||",
                "step(?a, 1) ^ text(?a, \"||\") -> associativity(?a, \"L\") ^ precedence(?a, 15) ^ arity(?a, \"binary\") ^ is_operator_with_strict_operands_order(?a, true) ^ init(?a, true)"
        ));
        laws.add(getSWRLLawFormulation(
                "operator~",
                "step(?a, 1) ^ text(?a, \"~\") -> arity(?a, \"unary\") ^ init(?a, true) ^ prefix_postfix(?a, \"prefix\") ^ precedence(?a, 3) ^ associativity(?a, \"R\")"
        ));
        laws.add(getSWRLLawFormulation(
                "prev_operand",
                "prev_index(?a, ?b) ^ text(?b, ?b_text) ^ is_operand(?b, true) ^ step(?b, 1) -> prev_operand(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "prev_operand_unary_postfix",
                "prev_index(?a, ?b) ^ arity(?b, \"unary\") ^ prefix_postfix(?b, \"postfix\") ^ step(?b, 1) -> prev_operand(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "prev_operation",
                "prev_index(?a, ?b) ^ arity(?b, ?b_arity) ^ swrlb:notEqual(?b_arity, \"unary\") ^ step(?b, 1) -> prev_operation(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "prev_operation_beggining",
                "step(?a, 1) ^ index(?a, 1) -> prev_operation(?a, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "prev_operation_unary_prefix",
                "prev_index(?a, ?b) ^ arity(?b, \"unary\") ^ prefix_postfix(?b, \"prefix\") ^ step(?b, 1) -> prev_operation(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "same_step",
                "step(?a, ?a_step) ^ step(?b, ?a_step) -> same_step(?a, ?b)"
        ));

        return laws;
    # }

    # public List<LawFormulation> getErrorLaws() {
    def getErrorLaws():
        # List<LawFormulation> laws = new ArrayList<>();
        laws = set()
        laws.add(getOWLLawFormulation("before_as_operand", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_by_third_operator", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_direct", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("before_third_operator", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("complex_beginning", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("describe_error", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority_left_assoc", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority_diff_priority", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("high_priority_right_assoc", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("is_operator_with_strict_operands_order", "owl:DatatypeProperty"));
        laws.add(getOWLLawFormulation("student_pos_less", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_equal_priority", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_in_complex", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_left_assoc", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_more_priority", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_more_priority_left", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_more_priority_right", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_right_assoc", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("student_error_strict_operands_order", "owl:ObjectProperty"));
        laws.add(getOWLLawFormulation("text", "owl:DatatypeProperty"));
        laws.add(getSWRLLawFormulation(
                "describe_error",
                "student_pos_less(?b, ?a) ^ before_direct(?a, ?b) -> describe_error(?a, ?b)"
        ));
        laws.add(getSWRLLawFormulation(
                "student_error_in_complex",
                "before_by_third_operator(?a, ?b) ^ before_third_operator(?a, ?c) ^ text(?c, \"(\") ^ describe_error(?a, ?b) -> student_error_in_complex(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "student_error_in_complex_bound",
                "before_as_operand(?a, ?b) ^ complex_beginning(?b, true) ^ describe_error(?a, ?b) -> student_error_in_complex(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "student_error_left_assoc",
                "before_as_operand(?a, ?b) ^ describe_error(?a, ?b) ^ high_priority_left_assoc(?a, ?b) -> student_error_left_assoc(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "student_error_more_priority",
                "before_as_operand(?a, ?b) ^ describe_error(?a, ?b) ^ high_priority_diff_priority(?a, ?b) -> student_error_more_priority(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "student_error_right_assoc",
                "before_as_operand(?a, ?b) ^ describe_error(?a, ?b) ^ high_priority_right_assoc(?a, ?b) -> student_error_right_assoc(?b, ?a)"
        ));
        laws.add(getSWRLLawFormulation(
                "student_error_strict_operands_order",
                "before_by_third_operator(?a, ?b) ^ before_third_operator(?a, ?c) ^ is_operator_with_strict_operands_order(?c, true) ^ describe_error(?a, ?b) -> student_error_strict_operands_order(?b, ?a)"
        ));
        return laws;
    # }
# '''

    def get_owl_swrl_laws():
        all_laws = getAllLaws() | getErrorLaws()
        owl = []
        swrl = []
        for law in all_laws:
            arr = owl if isinstance(law, tuple) else swrl
            arr.append(law)
            
        return owl, swrl

    def inject_laws(onto, omit_swrl=False):
        owl, swrl = get_owl_swrl_laws()
        with onto:
            for law in owl:
                name, property_type_name = law
                property_type_name = property_type_name.replace('owl:', '')
                property_type = globals()[property_type_name]
                types.new_class(name, (property_type, ))

            print('OWL laws injected:', len(owl))
            
            if not omit_swrl:
                for r in swrl:
                    # name, rule = r.name, r.swrl
                    try:
                        Imp(r.name).set_as_rule(r.swrl)
                    except Exception as e:
                        print("Error in SWRL rule: \t", r.name)
                        print(e)
                        raise e

                print('SWRL laws injected:', len(swrl))
