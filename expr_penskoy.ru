PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX my:  <http://penskoy.n/expressions#>

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


# Rule: rule_operator-gt []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 2 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "->" .
  } ;

# Rule: rule_before_before []
INSERT
  { ?a my:before ?c . }
WHERE
  {
    ?a my:before ?b . ?b my:before ?c .
  } ;

# Rule: rule_operator( []
INSERT
  { ?a my:associativity "L" . ?a my:precedence 0 . ?a my:arity "complex" . ?a my:init true . ?a my:complex_beginning true . ?a my:is_function_call false . }
WHERE
  {
    ?a my:text "<(>" . ?a my:step 1 . ?a my:prev_operation ?b .
  } ;

# Rule: rule_operator*= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "*=" .
  } ;

# Rule: rule_operator, []
INSERT
  { ?a my:associativity "L" . ?a my:precedence 17 . ?a my:arity "binary" . ?a my:is_operator_with_strict_operands_order true . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "<,>" .
  } ;

# Rule: rule_operator-= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "-=" .
  } ;

# Rule: rule_operator. []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 2 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "." .
  } ;

# Rule: rule_operator/ []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:precedence 5 . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "/" .
  } ;

# Rule: rule_operator/= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "/=" .
  } ;

# Rule: rule_operator: []
INSERT
  { ?a my:arity "ternary" . ?a my:precedence 16 . ?a my:init true . ?a my:complex_ending true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:text ":" . ?a my:step 1 .
  } ;

# Rule: rule_operatorltlt []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 7 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "<<" .
  } ;

# Rule: rule_operator:: []
INSERT
  { ?a my:associativity "L" . ?a my:precedence 1 . ?a my:arity "binary" . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "::" .
  } ;

# Rule: rule_complex_boundaries_empty []
INSERT
  { ?a my:complex_boundaries ?b . }
WHERE
  {
    ?a my:next_index ?b . ?a my:step 0 . ?a my:complex_beginning true . ?b my:complex_ending true .
  } ;

# Rule: rule_operatorlt []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 9 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "<" .
  } ;

# Rule: rule_operatorltlt= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "<<=" .
  } ;

# Rule: rule_operatorlt= []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 9 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "<=" .
  } ;

# Rule: rule_copy_eval_step_to_zero_step []
INSERT
  { ?a0 my:eval_step ?a_step . }
WHERE
  {
    ?a my:eval_step ?a_step . ?a my:zero_step ?a0 .
  } ;

# Rule: rule_operator= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "=" .
  } ;

# Rule: rule_operatorgt= []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 9 . }
WHERE
  {
    ?a my:step 1 . ?a my:text ">=" .
  } ;

# Rule: rule_copy_app []
INSERT
  { ?to my:app true . }
WHERE
  {
    ?a my:copy ?to . ?a my:app true .
  } ;

# Rule: rule_operator== []
INSERT
  { ?a my:precedence 10 . ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "==" .
  } ;

# Rule: rule_copy_eval []
INSERT
  { ?to my:eval true . }
WHERE
  {
    ?a my:copy ?to . ?a my:eval true .
  } ;

# Rule: rule_operatorgt []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 9 . }
WHERE
  {
    ?a my:step 1 . ?a my:text ">" .
  } ;

# Rule: rule_copy_has_complex_operator_part_to_zero_step []
INSERT
  { ?a0 my:has_complex_operator_part ?b0 . }
WHERE
  {
    ?a my:has_complex_operator_part ?b . ?a my:zero_step ?a0 . ?b my:zero_step ?b0 .
  } ;

# Rule: rule_operatorgtgt []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 7 . }
WHERE
  {
    ?a my:step 1 . ?a my:text ">>" .
  } ;

# Rule: rule_copy_has_operand_to_zero_step []
INSERT
  { ?a0 my:has_operand ?b0 . }
WHERE
  {
    ?a my:has_operand ?b . ?a my:zero_step ?a0 . ?b my:zero_step ?b0 .
  } ;

# Rule: rule_operatorgtgt= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text ">>=" .
  } ;

# Rule: rule_copy_to_zero_step []
INSERT
  { ?b my:copy_without_marks ?a . }
WHERE
  {
    ?a my:step 0 . ?b my:step 1 . ?b my:zero_step ?a .
  } ;

# Rule: rule_operator_binary& []
INSERT
  { ?a my:precedence 11 . ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . }
WHERE
  {
    ?a my:text "&" . ?a my:step 1 . ?a my:prev_operand ?b .
  } ;

# Rule: rule_eval_complex_operation_copy_other_right []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?c my:next_step ?c_next . ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:complex_boundaries ?c . ?c my:index ?c_index . ?a my:all_eval_to_right ?b . ?a my:arity "complex" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?a my:next_step ?a_next . ?c my:not_index ?other . ?a my:same_step ?c . ?other my:index ?other_index . ?a my:index ?a_index . FILTER ( ?other_index > ?c_index ) .
  } ;

# Rule: rule_copy_init []
INSERT
  { ?to my:init true . }
WHERE
  {
    ?a my:copy ?to . ?a my:init true .
  } ;

# Rule: rule_operator? []
INSERT
  { ?a my:arity "ternary" . ?a my:precedence 16 . ?a my:is_operator_with_strict_operands_order true . ?a my:init true . ?a my:complex_beginning true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "?" .
  } ;

# Rule: rule_copy_to_1_step []
INSERT
  { ?a my:copy ?b . }
WHERE
  {
    ?a my:step 0 . ?b my:step 1 . ?b my:zero_step ?a .
  } ;

# Rule: rule_copy_without_marks []
INSERT
  { ?a my:copy_without_marks ?to . }
WHERE
  {
    ?a my:copy ?to .
  } ;

# Rule: rule_operator^ []
INSERT
  { ?a my:precedence 12 . ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "^" .
  } ;

# Rule: rule_copy_without_marks_arity []
INSERT
  { ?to my:arity ?a_arity . }
WHERE
  {
    ?a my:arity ?a_arity . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_copy_without_marks_associativity []
INSERT
  { ?to my:associativity ?a_associativity . }
WHERE
  {
    ?a my:associativity ?a_associativity . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator^= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "^=" .
  } ;

# Rule: rule_copy_without_marks_complex_beginning []
INSERT
  { ?to my:complex_beginning ?b . }
WHERE
  {
    ?a my:complex_beginning ?b . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_binary* []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:precedence 5 . ?a my:init true . }
WHERE
  {
    ?a my:text "*" . ?a my:step 1 . ?a my:prev_operand ?b .
  } ;

# Rule: rule_copy_without_marks_complex_boundaries []
INSERT
  { ?to my:complex_boundaries ?c . }
WHERE
  {
    ?c my:same_step ?to . ?a my:copy_without_marks ?to . ?a my:complex_boundaries ?b . ?c my:zero_step ?b0 . ?b my:zero_step ?b0 .
  } ;

# Rule: rule_operator_binary+ []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 6 . }
WHERE
  {
    ?a my:text "+" . ?a my:step 1 . ?a my:prev_operand ?b .
  } ;

# Rule: rule_copy_without_marks_complex_ending []
INSERT
  { ?to my:complex_ending ?b . }
WHERE
  {
    ?a my:complex_ending ?b . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_binary- []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . ?a my:precedence 6 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "-" . ?a my:prev_operand ?b .
  } ;

# Rule: rule_copy_without_marks_in_complex []
INSERT
  { ?to my:in_complex ?c . }
WHERE
  {
    ?c my:same_step ?to . ?a my:copy_without_marks ?to . ?a my:in_complex ?b . ?c my:zero_step ?b0 . ?b my:zero_step ?b0 .
  } ;

# Rule: rule_operator_function_call []
INSERT
  { ?a my:associativity "L" . ?a my:arity "complex" . ?a my:init true . ?a my:is_function_call true . ?a my:precedence 2 . }
WHERE
  {
    ?a my:text "<(>" . ?a my:prev_operand ?b .
  } ;

# Rule: rule_copy_without_marks_is_function_call []
INSERT
  { ?to my:is_function_call ?a_fc . }
WHERE
  {
    ?a my:is_function_call ?a_fc . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_postfix++ []
INSERT
  { ?a my:associativity "L" . ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "postfix" . ?a my:precedence 2 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "++" . ?a my:prev_operand ?b .
  } ;

# Rule: rule_copy_without_marks_is_operand []
INSERT
  { ?to my:is_operand ?is_op . }
WHERE
  {
    ?a my:copy_without_marks ?to . ?a my:is_operand ?is_op .
  } ;

# Rule: rule_operator_postfix-- []
INSERT
  { ?a my:associativity "L" . ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "postfix" . ?a my:precedence 2 . }
WHERE
  {
    ?a my:step 1 . ?a my:text "--" . ?a my:prev_operand ?b .
  } ;

# Rule: rule_copy_without_marks_is_operator_with_strict_operands_order []
INSERT
  { ?to my:is_operator_with_strict_operands_order ?is_op . }
WHERE
  {
    ?a my:copy_without_marks ?to . ?a my:is_operator_with_strict_operands_order ?is_op .
  } ;

# Rule: rule_operator_prefix++ []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "++" . ?a my:prev_operation ?b .
  } ;

# Rule: rule_copy_without_marks_last []
INSERT
  { ?to my:last ?a_last . }
WHERE
  {
    ?a my:last ?a_last . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_prefix-- []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "--" . ?a my:prev_operation ?b .
  } ;

# Rule: rule_copy_without_marks_prefix_postfix []
INSERT
  { ?to my:prefix_postfix ?a_pr . }
WHERE
  {
    ?a my:prefix_postfix ?a_pr . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_subscript []
INSERT
  { ?a my:associativity "L" . ?a my:arity "complex" . ?a my:init true . ?a my:complex_beginning true . ?a my:is_function_call true . ?a my:precedence 2 . }
WHERE
  {
    ?a my:text "[" . ?a my:step 1 .
  } ;

# Rule: rule_copy_without_marks_priority []
INSERT
  { ?to my:precedence ?a_priority . }
WHERE
  {
    ?a my:precedence ?a_priority . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_unary* []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:text "*" . ?a my:step 1 . ?a my:prev_operation ?b .
  } ;

# Rule: rule_copy_without_marks_real_pos []
INSERT
  { ?to my:real_pos ?a_rp . }
WHERE
  {
    ?a my:real_pos ?a_rp . ?a my:copy_without_marks ?to .
  } ;

# Rule: rule_operator_unary+ []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:text "+" . ?a my:step 1 . ?a my:prev_operation ?b .
  } ;

# Rule: rule_copy_without_marks_student_pos []
INSERT
  { ?to my:student_pos ?a_sp . }
WHERE
  {
    ?a my:copy_without_marks ?to . ?a my:student_pos ?a_sp .
  } ;

# Rule: rule_operator_unary- []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "-" . ?a my:prev_operation ?b .
  } ;

# Rule: rule_copy_without_marks_text []
INSERT
  { ?to my:text ?a_text . }
WHERE
  {
    ?a my:copy_without_marks ?to . ?a my:text ?a_text .
  } ;

# Rule: rule_prev_operand []
INSERT
  { ?a my:prev_operand ?b . }
WHERE
  {
    ?a my:prev_index ?b . ?b my:text ?b_text . ?b my:is_operand true . ?b my:step 1 .
  } ;

# Rule: rule_equal_priority_L_assoc []
INSERT
  { ?a my:high_priority_left_assoc ?b . ?a my:high_priority ?b . }
WHERE
  {
    FILTER ( ?a_prior = ?b_prior ) . FILTER ( ?a_assoc = ?b_assoc ) . ?b my:index ?b_index . ?a my:precedence ?a_prior . ?b my:associativity ?b_assoc . ?b my:precedence ?b_prior . ?a my:associativity ?a_assoc . FILTER ( ?a_assoc = "L" ) . ?a my:index ?a_index . FILTER ( ?a_index < ?b_index ) . ?a my:same_step ?b .
  } ;

# Rule: rule_equal_priority_R_assoc []
INSERT
  { ?a my:high_priority ?b . ?a my:high_priority_right_assoc ?b . }
WHERE
  {
    FILTER ( ?a_prior = ?b_prior ) . FILTER ( ?a_assoc = ?b_assoc ) . ?b my:index ?b_index . ?a my:precedence ?a_prior . ?b my:associativity ?b_assoc . ?b my:precedence ?b_prior . ?a my:associativity ?a_assoc . FILTER ( ?a_assoc = "R" ) . ?a my:index ?a_index . ?a my:same_step ?b . FILTER ( ?a_index > ?b_index ) .
  } ;

# Rule: rule_operator| []
INSERT
  { ?a my:precedence 13 . ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "|" .
  } ;

# Rule: rule_eval_,_in_function_call []
INSERT
  { ?a my:app true . }
WHERE
  {
    ?a my:text "<,>" . ?a my:init true . ?a my:in_complex ?b . ?b my:is_function_call true .
  } ;

# Rule: rule_eval_binary_operation []
INSERT
  { ?a my:has_operand ?c . ?a my:copy_without_marks ?a_next . ?c my:copy_without_marks ?c_next . ?b_next my:app true . ?a my:eval_step ?a_step . ?c_next my:app true . ?a_next my:eval true . ?b my:copy_without_marks ?b_next . ?a my:has_operand ?b . }
WHERE
  {
    ?b my:next_step ?b_next . ?c my:next_step ?c_next . ?a my:has_highest_priority_to_right true . ?a my:find_left_operand ?b . ?a my:step ?a_step . ?a my:arity "binary" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:find_right_operand ?c . ?a my:next_step ?a_next . ?a my:same_step ?c . ?a my:same_step ?b .
  } ;

# Rule: rule_operator|= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "|=" .
  } ;

# Rule: rule_eval_binary_operation_copy_other []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?a my:arity "binary" . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:find_right_operand ?c . ?a my:find_left_operand ?b . ?a my:init true . ?b my:not_index ?other . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?c my:not_index ?other . ?a my:same_step ?c . ?a my:same_step ?b .
  } ;

# Rule: rule_eval_complex_operation []
INSERT
  { ?a my:copy_without_marks ?a_next . ?c my:copy_without_marks ?c_next . ?a my:eval_step ?a_step . ?a my:has_complex_operator_part ?c . ?c_next my:app true . ?a_next my:eval true . }
WHERE
  {
    ?c my:next_step ?c_next . ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?a my:all_eval_to_right ?b . ?a my:step ?a_step . ?a my:arity "complex" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:next_step ?a_next . ?a my:same_step ?c . ?a my:complex_boundaries ?c .
  } ;

# Rule: rule_operator|| []
INSERT
  { ?a my:associativity "L" . ?a my:precedence 15 . ?a my:arity "binary" . ?a my:is_operator_with_strict_operands_order true . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "||" .
  } ;

# Rule: rule_eval_complex_operation_copy_inner_app []
INSERT
  { ?other my:copy_without_marks ?other_next . ?other_next my:app true . }
WHERE
  {
    ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:complex_boundaries ?c . ?c my:index ?c_index . ?a my:all_eval_to_right ?b . ?a my:arity "complex" . ?other my:app true . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?c my:not_index ?other . ?other my:index ?other_index . FILTER ( ?other_index < ?c_index ) . ?a my:same_step ?c . ?a my:index ?a_index . FILTER ( ?a_index < ?other_index ) .
  } ;

# Rule: rule_prev_operation []
INSERT
  { ?a my:prev_operation ?b . }
WHERE
  {
    ?a my:prev_index ?b . ?b my:arity ?b_arity . FILTER ( ?b_arity != "unary" ) . ?b my:step 1 .
  } ;

# Rule: rule_eval_complex_operation_copy_inner_eval []
INSERT
  { ?other my:copy_without_marks ?other_next . ?other_next my:app true . ?a my:has_operand ?other . }
WHERE
  {
    ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:complex_boundaries ?c . ?c my:index ?c_index . ?a my:all_eval_to_right ?b . ?a my:arity "complex" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?c my:not_index ?other . ?other my:index ?other_index . FILTER ( ?other_index < ?c_index ) . ?a my:same_step ?c . ?a my:index ?a_index . FILTER ( ?a_index < ?other_index ) . ?other my:eval true .
  } ;

# Rule: rule_operator~ []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "~" .
  } ;

# Rule: rule_eval_complex_operation_copy_other_left []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?c my:next_step ?c_next . ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:complex_boundaries ?c . ?c my:index ?c_index . ?a my:all_eval_to_right ?b . ?a my:arity "complex" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?a my:next_step ?a_next . ?c my:not_index ?other . ?a my:is_function_call false . ?a my:same_step ?c . ?other my:index ?other_index . ?a my:index ?a_index . FILTER ( ?other_index < ?a_index ) .
  } ;

# Rule: rule_prev_operand_unary_postfix []
INSERT
  { ?a my:prev_operand ?b . }
WHERE
  {
    ?a my:prev_index ?b . ?b my:arity "unary" . ?b my:prefix_postfix "postfix" . ?b my:step 1 .
  } ;

# Rule: rule_eval_complex_operation_copy_others_left_no_function_name []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?c my:next_step ?c_next . ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:complex_boundaries ?c . ?c my:index ?c_index . ?a my:find_left_operand ?d . ?a my:all_eval_to_right ?b . ?a my:arity "complex" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?a my:next_step ?a_next . ?a my:is_function_call true . ?d my:not_index ?other . ?c my:not_index ?other . ?a my:same_step ?c . ?other my:index ?other_index . ?a my:index ?a_index . FILTER ( ?other_index < ?a_index ) .
  } ;

# Rule: rule_prev_operation_beggining []
INSERT
  { ?a my:prev_operation ?a . }
WHERE
  {
    ?a my:step 1 . ?a my:index 1 .
  } ;

# Rule: rule_all_eval_to_right []
INSERT
  { ?a my:all_eval_to_right ?c . }
WHERE
  {
    ?a my:all_eval_to_right ?b . ?b my:next_index ?c . ?c my:eval true .
  } ;

# Rule: rule_eval_function_name []
INSERT
  { ?function_name my:copy_without_marks ?function_name_next . ?function_name_next my:app true . ?a my:has_complex_operator_part ?function_name . }
WHERE
  {
    ?function_name my:next_step ?function_name_next . ?b my:next_index ?c . ?a my:has_highest_priority_to_right true . ?a my:all_eval_to_right ?b . ?a my:find_left_operand ?function_name . ?a my:same_step ?function_name . ?a my:arity "complex" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:is_function_call true . ?a my:same_step ?c . ?a my:complex_boundaries ?c .
  } ;

# Rule: rule_prev_operation_unary_prefix []
INSERT
  { ?a my:prev_operation ?b . }
WHERE
  {
    ?a my:prev_index ?b . ?b my:arity "unary" . ?b my:prefix_postfix "prefix" . ?b my:step 1 .
  } ;

# Rule: rule_eval_operand_in_complex []
INSERT
  { ?a my:eval true . }
WHERE
  {
    ?a my:init true . ?a my:in_complex ?b . ?a my:is_operand true .
  } ;

# Rule: rule_eval_postfix_operation []
INSERT
  { ?a my:copy_without_marks ?a_next . ?b_next my:app true . ?a my:eval_step ?a_step . ?a_next my:eval true . ?b my:copy_without_marks ?b_next . ?a my:has_operand ?b . }
WHERE
  {
    ?b my:next_step ?b_next . ?a my:has_highest_priority_to_right true . ?a my:find_left_operand ?b . ?a my:step ?a_step . ?a my:arity "unary" . ?a my:init true . ?a my:has_highest_priority_to_left true . ?a my:prefix_postfix "postfix" . ?a my:next_step ?a_next . ?a my:same_step ?b .
  } ;

# Rule: rule_eval_postfix_operation_copy_others []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?a my:find_left_operand ?b . ?a my:arity "unary" . ?a my:init true . ?b my:not_index ?other . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?a my:prefix_postfix "postfix" . ?a my:same_step ?b .
  } ;

# Rule: rule_same_step []
INSERT
  { ?a my:same_step ?b . }
WHERE
  {
    ?a my:step ?a_step . ?b my:step ?a_step .
  } ;

# Rule: rule_eval_prefix_operation []
INSERT
  { ?a my:copy_without_marks ?a_next . ?b_next my:app true . ?a my:eval_step ?a_step . ?a_next my:eval true . ?b my:copy_without_marks ?b_next . ?a my:has_operand ?b . }
WHERE
  {
    ?b my:next_step ?b_next . ?a my:has_highest_priority_to_right true . ?a my:step ?a_step . ?a my:arity "unary" . ?a my:init true . ?b my:not_index ?other . ?a my:prefix_postfix "prefix" . ?a my:has_highest_priority_to_left true . ?a my:next_step ?a_next . ?a my:find_right_operand ?b . ?a my:same_step ?b .
  } ;

# Rule: rule_eval_prefix_operation_copy_others []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?a my:arity "unary" . ?a my:init true . ?b my:not_index ?other . ?other my:next_step ?other_next . ?a my:prefix_postfix "prefix" . ?a my:same_step ?other . ?a my:has_highest_priority_to_left true . ?a my:not_index ?other . ?a my:find_right_operand ?b . ?a my:same_step ?b .
  } ;

# Rule: rule_eval_ternary_operation []
INSERT
  { ?a my:has_operand ?e . ?d my:copy_without_marks ?d_next . ?a my:has_operand ?d . ?a my:copy_without_marks ?a_next . ?c my:copy_without_marks ?c_next . ?e my:copy_without_marks ?e_next . ?a my:eval_step ?a_step . ?a my:has_complex_operator_part ?c . ?c_next my:app true . ?d_next my:app true . ?e_next my:app true . ?a_next my:eval true . }
WHERE
  {
    ?a my:arity "ternary" . ?c my:next_step ?c_next . ?b my:next_index ?c . ?a my:step ?a_step . ?c my:has_highest_priority_to_right true . ?c my:find_right_operand ?e . ?a my:complex_boundaries ?c . ?a my:find_left_operand ?d . ?a my:all_eval_to_right ?b . ?e my:next_step ?e_next . ?a my:init true . ?d my:next_step ?d_next . ?a my:next_step ?a_next . ?c my:has_highest_priority_to_left true . ?a my:same_step ?c .
  } ;

# Rule: rule_eval_ternary_operation_copy_inner_app []
INSERT
  { ?other my:copy_without_marks ?other_next . ?other_next my:app true . }
WHERE
  {
    ?c my:index ?c_index . ?a my:arity "ternary" . ?a my:step ?a_step . ?other my:step ?a_step . ?a my:eval_step ?a_step . ?other my:app true . ?other my:next_step ?other_next . ?other my:index ?other_index . FILTER ( ?other_index < ?c_index ) . ?a my:complex_boundaries ?c . ?a my:index ?a_index . FILTER ( ?a_index < ?other_index ) .
  } ;

# Rule: rule_eval_ternary_operation_copy_inner_eval []
INSERT
  { ?other my:copy_without_marks ?other_next . ?other_next my:app true . ?a my:has_operand ?other . }
WHERE
  {
    ?c my:index ?c_index . ?a my:arity "ternary" . ?a my:step ?a_step . ?other my:step ?a_step . ?a my:eval_step ?a_step . ?other my:next_step ?other_next . ?other my:index ?other_index . FILTER ( ?other_index < ?c_index ) . ?a my:complex_boundaries ?c . ?a my:index ?a_index . FILTER ( ?a_index < ?other_index ) . ?other my:eval true .
  } ;

# Rule: rule_eval_ternary_operation_copy_other_left []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?a my:arity "ternary" . ?a my:eval_step ?a_step . ?a my:step ?a_step . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:find_left_operand ?d . ?d my:not_index ?other . ?other my:index ?other_index . ?a my:index ?a_index . FILTER ( ?other_index < ?a_index ) .
  } ;

# Rule: rule_before_strict_order_operands []
INSERT
  { ?b my:before_direct ?c . ?b my:before_all_operands ?c . ?b my:before_by_third_operator ?c . ?b my:before_third_operator ?a . }
WHERE
  {
    ?a my:is_operator_with_strict_operands_order true . ?a my:text ?a_text . FILTER ( ?a_text != "?" ) . ?a my:has_operand ?b . ?a my:has_operand ?c . ?b my:index ?b_index . ?c my:index ?c_index . FILTER ( ?b_index < ?c_index ) .
  } ;

# Rule: rule_eval_ternary_operation_copy_other_right []
INSERT
  { ?other my:copy ?other_next . }
WHERE
  {
    ?a my:arity "ternary" . ?a my:eval_step ?a_step . ?a my:step ?a_step . ?other my:next_step ?other_next . ?a my:same_step ?other . ?a my:complex_boundaries ?c . ?c my:find_right_operand ?d . ?d my:not_index ?other . ?other my:index ?other_index . ?c my:index ?c_index . FILTER ( ?c_index < ?other_index ) .
  } ;

# Rule: rule_find_left_operand_eval []
INSERT
  { ?a my:find_left_operand ?c . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?b my:prev_index ?c . ?c my:eval true . ?a my:has_highest_priority_to_left true . ?a my:all_app_to_left ?b .
  } ;

# Rule: rule_all_eval_to_right_begin []
INSERT
  { ?a my:all_eval_to_right ?a . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?a my:init true . ?a my:complex_beginning true . ?a my:has_highest_priority_to_left true .
  } ;

# Rule: rule_find_left_operand_init []
INSERT
  { ?a my:find_left_operand ?c . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?b my:prev_index ?c . ?a my:has_highest_priority_to_left true . ?c my:init true . ?a my:all_app_to_left ?b .
  } ;

# Rule: rule_find_right_operand_eval []
INSERT
  { ?a my:find_right_operand ?c . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?b my:next_index ?c . ?a my:all_app_to_right ?b . ?c my:eval true . ?a my:has_highest_priority_to_left true .
  } ;

# Rule: rule_find_right_operand_init []
INSERT
  { ?a my:find_right_operand ?c . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?b my:next_index ?c . ?a my:all_app_to_right ?b . ?a my:has_highest_priority_to_left true . ?c my:init true .
  } ;

# Rule: rule_has_highest_priority_to_left []
INSERT
  { ?a my:has_highest_priority_to_left true . }
WHERE
  {
    ?a my:more_priority_left_by_step ?b . ?b my:index 1 .
  } ;

# Rule: rule_has_highest_priority_to_left_in_complex_, []
INSERT
  { ?a my:has_highest_priority_to_left true . }
WHERE
  {
    ?b my:prev_index ?c . ?a my:in_complex ?c . ?a my:text "<,>" . ?c my:is_function_call false . ?a my:more_priority_left_by_step ?b . ?c my:has_highest_priority_to_left true . ?c my:complex_boundaries ?d .
  } ;

# Rule: rule_has_highest_priority_to_left_in_complex_not_, []
INSERT
  { ?a my:has_highest_priority_to_left true . }
WHERE
  {
    ?a my:text ?a_text . FILTER ( ?a_text != "<,>" ) . ?b my:prev_index ?c . ?a my:in_complex ?c . ?a my:more_priority_left_by_step ?b . ?c my:has_highest_priority_to_left true .
  } ;

# Rule: rule_has_highest_priority_to_left_ternary []
INSERT
  { ?d my:has_highest_priority_to_left true . }
WHERE
  {
    ?c my:has_highest_priority_to_left true . ?c my:complex_boundaries ?d .
  } ;

# Rule: rule_has_highest_priority_to_right []
INSERT
  { ?a my:has_highest_priority_to_right true . }
WHERE
  {
    ?a my:more_priority_right_by_step ?b . ?b my:last true .
  } ;

# Rule: rule_has_highest_priority_to_right_in_complex []
INSERT
  { ?a my:has_highest_priority_to_right true . }
WHERE
  {
    ?b my:next_index ?d . ?c my:has_highest_priority_to_right true . ?a my:in_complex ?c . ?a my:more_priority_right_by_step ?b . ?c my:complex_boundaries ?d .
  } ;

# Rule: rule_operator&& []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:is_operator_with_strict_operands_order true . ?a my:precedence 14 . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "&&" .
  } ;

# Rule: rule_has_highest_priority_to_right_ternary []
INSERT
  { ?c my:has_highest_priority_to_right true . }
WHERE
  {
    ?d my:has_highest_priority_to_right true . ?c my:complex_boundaries ?d .
  } ;

# Rule: rule_high_priority []
INSERT
  { ?a my:high_priority ?b . ?a my:high_priority_diff_priority ?b . }
WHERE
  {
    ?a my:precedence ?a_prior . ?b my:precedence ?b_prior . FILTER ( ?a_prior < ?b_prior ) . ?a my:same_step ?b .
  } ;

# Rule: rule_in_complex_begin []
INSERT
  { ?b my:in_complex ?a . }
WHERE
  {
    ?a my:next_index ?b . ?a my:complex_beginning true . ?b my:complex_ending false . ?a my:step 0 .
  } ;

# Rule: rule_describe_error []
INSERT
  { ?a my:describe_error ?b . }
WHERE
  {
    ?b my:student_pos_less ?a . ?a my:before_direct ?b .
  } ;

# Rule: rule_in_complex_step []
INSERT
  { ?b my:in_complex ?c . }
WHERE
  {
    ?a my:next_index ?b . ?a my:step 0 . ?a my:complex_beginning false . ?a my:in_complex ?c . ?b my:complex_ending false .
  } ;

# Rule: rule_student_error_in_complex []
INSERT
  { ?b my:student_error_in_complex ?a . }
WHERE
  {
    ?a my:before_by_third_operator ?b . ?a my:before_third_operator ?c . ?c my:text "<(>" . ?a my:describe_error ?b .
  } ;

# Rule: rule_in_complex_step_skip_inner_complex []
INSERT
  { ?d my:in_complex ?c . }
WHERE
  {
    ?a my:in_complex ?c . ?a my:complex_boundaries ?d . ?a my:step 0 .
  } ;

# Rule: rule_student_error_in_complex_bound []
INSERT
  { ?b my:student_error_in_complex ?a . }
WHERE
  {
    ?a my:before_as_operand ?b . ?b my:complex_beginning true . ?a my:describe_error ?b .
  } ;

# Rule: rule_is_operand_close_bracket []
INSERT
  { ?a my:init true . ?a my:is_operand true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "]" .
  } ;

# Rule: rule_student_error_left_assoc []
INSERT
  { ?b my:student_error_left_assoc ?a . }
WHERE
  {
    ?a my:before_as_operand ?b . ?a my:describe_error ?b . ?a my:high_priority_left_assoc ?b .
  } ;

# Rule: rule_all_app_to_right_begin []
INSERT
  { ?a my:all_app_to_right ?a . }
WHERE
  {
    ?a my:has_highest_priority_to_right true . ?a my:init true .
  } ;

# Rule: rule_student_error_more_priority []
INSERT
  { ?b my:student_error_more_priority ?a . }
WHERE
  {
    ?a my:before_as_operand ?b . ?a my:describe_error ?b . ?a my:high_priority_diff_priority ?b .
  } ;

# Rule: rule_is_operand []
INSERT
  { ?a my:init true . ?a my:is_operand true . }
WHERE
  {
    ?a my:text ?a_text . FILTER ( ?a_text != "sizeof" ) . FILTER (regex ( ?a_text, "[a-zA-Z_0-9]+" )) . ?a my:step 1 .
  } ;

# Rule: rule_student_error_right_assoc []
INSERT
  { ?b my:student_error_right_assoc ?a . }
WHERE
  {
    ?a my:before_as_operand ?b . ?a my:describe_error ?b . ?a my:high_priority_right_assoc ?b .
  } ;

# Rule: rule_is_operand_close_parenthesis []
INSERT
  { ?a my:init true . ?a my:is_operand true . }
WHERE
  {
    ?a my:text ")" . ?a my:step 1 .
  } ;

# Rule: rule_student_error_strict_operands_order []
INSERT
  { ?b my:student_error_strict_operands_order ?a . }
WHERE
  {
    ?a my:before_by_third_operator ?b . ?a my:before_third_operator ?c . ?c my:is_operator_with_strict_operands_order true . ?a my:describe_error ?b .
  } ;

# Rule: rule_more_priority_left_by_step []
INSERT
  { ?a my:more_priority_left_by_step ?c . }
WHERE
  {
    ?a my:more_priority_left_by_step ?b . ?b my:prev_index ?c . ?a my:high_priority ?c .
  } ;

# Rule: rule_more_priority_left_by_step_app []
INSERT
  { ?a my:more_priority_left_by_step ?c . }
WHERE
  {
    ?a my:more_priority_left_by_step ?b . ?b my:prev_index ?c . ?c my:app true .
  } ;

# Rule: rule_more_priority_left_by_step_eval []
INSERT
  { ?a my:more_priority_left_by_step ?c . }
WHERE
  {
    ?a my:more_priority_left_by_step ?b . ?b my:prev_index ?c . ?c my:eval true .
  } ;

# Rule: rule_more_priority_left_by_step_first []
INSERT
  { ?a my:more_priority_left_by_step ?a . }
WHERE
  {
    ?a my:precedence ?a_prior . ?a my:init true .
  } ;

# Rule: rule_more_priority_left_by_step_operand []
INSERT
  { ?a my:more_priority_left_by_step ?c . }
WHERE
  {
    ?a my:more_priority_left_by_step ?b . ?b my:prev_index ?c . ?c my:is_operand true .
  } ;

# Rule: rule_ast_edge_has_complex_operator_part []
INSERT
  { ?a my:ast_edge ?b . }
WHERE
  {
    ?a my:has_complex_operator_part ?b .
  } ;

# Rule: rule_more_priority_right_by_step []
INSERT
  { ?a my:more_priority_right_by_step ?c . }
WHERE
  {
    ?a my:more_priority_right_by_step ?b . ?b my:next_index ?c . ?a my:high_priority ?c .
  } ;

# Rule: rule_more_priority_right_by_step_app []
INSERT
  { ?a my:more_priority_right_by_step ?c . }
WHERE
  {
    ?a my:more_priority_right_by_step ?b . ?b my:next_index ?c . ?c my:app true .
  } ;

# Rule: rule_more_priority_right_by_step_eval []
INSERT
  { ?a my:more_priority_right_by_step ?c . }
WHERE
  {
    ?a my:more_priority_right_by_step ?b . ?b my:next_index ?c . ?c my:eval true .
  } ;

# Rule: rule_more_priority_right_by_step_first []
INSERT
  { ?a my:more_priority_right_by_step ?a . }
WHERE
  {
    ?a my:precedence ?a_prior . ?a my:init true .
  } ;

# Rule: rule_more_priority_right_by_step_operand []
INSERT
  { ?a my:more_priority_right_by_step ?c . }
WHERE
  {
    ?a my:more_priority_right_by_step ?b . ?b my:next_index ?c . ?c my:is_operand true .
  } ;

# Rule: rule_operator += []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "+=" .
  } ;

# Rule: rule_next_prev []
INSERT
  { ?a my:next_index ?b . ?b my:prev_index ?a . }
WHERE
  {
    ?a my:index ?a_index . BIND( ?a_index + 1 as ?b_index ) . ?b my:index ?b_index . ?a my:same_step ?b .
  } ;

# Rule: rule_next_step []
INSERT
  { ?a my:next_step ?b . }
WHERE
  {
    ?a my:index ?a_index . ?b my:index ?a_index . ?a my:step ?a_step . BIND( ?a_step + 1 as ?b_step ) . ?b my:step ?b_step .
  } ;

# Rule: rule_all_app_to_left []
INSERT
  { ?a my:all_app_to_left ?c . }
WHERE
  {
    ?a my:all_app_to_left ?b . ?b my:prev_index ?c . ?c my:app true .
  } ;

# Rule: rule_not_index []
INSERT
  { ?b my:not_index ?a . ?a my:not_index ?b . }
WHERE
  {
    ?a my:index ?a_index . ?b my:index ?b_index . FILTER ( ?a_index != ?b_index ) . ?a my:same_step ?b .
  } ;

# Rule: rule_zero_step []
INSERT
  { ?a my:zero_step ?b . }
WHERE
  {
    ?a my:index ?a_index . ?b my:index ?a_index . ?b my:step 0 .
  } ;

# Rule: rule_before_direct []
INSERT
  { ?a my:before ?b . }
WHERE
  {
    ?a my:before_direct ?b .
  } ;

# Rule: rule_operator&= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:text "&=" . ?a my:step 1 .
  } ;

# Rule: rule_before []
INSERT
  { ?b my:before_direct ?a . ?b my:before_as_operand ?a . }
WHERE
  {
    ?a my:has_operand ?b . ?b my:text ?b_text . FILTER ( ?b_text != "<(>" ) .
  } ;

# Rule: rule_operator! []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:step 1 . ?a my:text "!" .
  } ;

# Rule: rule_before_function_call []
INSERT
  { ?b my:before_direct ?a . ?b my:before_as_operand ?a . }
WHERE
  {
    ?a my:has_operand ?b . ?b my:text "<(>" . ?b my:is_function_call true .
  } ;

# Rule: rule_operator!= []
INSERT
  { ?a my:precedence 10 . ?a my:associativity "L" . ?a my:arity "binary" . ?a my:init true . }
WHERE
  {
    ?a my:step 1 . ?a my:text "!=" .
  } ;

# Rule: rule_all_app_to_right []
INSERT
  { ?a my:all_app_to_right ?c . }
WHERE
  {
    ?a my:all_app_to_right ?b . ?b my:next_index ?c . ?c my:app true .
  } ;

# Rule: rule_ast_edge_has_operand []
INSERT
  { ?a my:ast_edge ?b . }
WHERE
  {
    ?a my:has_operand ?b .
  } ;

# Rule: rule_operator% []
INSERT
  { ?a my:associativity "L" . ?a my:arity "binary" . ?a my:precedence 5 . ?a my:init true . }
WHERE
  {
    ?a my:text "%" . ?a my:step 1 .
  } ;

# Rule: rule_before_in_complex []
INSERT
  { ?c my:before_direct ?a . ?c my:before_by_third_operator ?a . ?c my:before_third_operator ?b . }
WHERE
  {
    ?a my:has_operand ?b . ?b my:text "<(>" . ?b my:has_operand ?c .
  } ;

# Rule: rule_all_app_to_left_begin []
INSERT
  { ?a my:all_app_to_left ?a . }
WHERE
  {
    ?a my:init true . ?a my:has_highest_priority_to_left true .
  } ;

# Rule: rule_operator%= []
INSERT
  { ?a my:precedence 16 . ?a my:arity "binary" . ?a my:init true . ?a my:associativity "R" . }
WHERE
  {
    ?a my:text "%=" . ?a my:step 1 .
  } ;

# Rule: rule_before_strict_order_operands_ternary []
INSERT
  { ?b my:before_direct ?c . ?b my:before_all_operands ?c . ?b my:before_by_third_operator ?c . ?b my:before_third_operator ?a . }
WHERE
  {
    ?a my:text "?" . ?a my:has_operand ?b . ?a my:has_operand ?c . ?a my:has_operand ?d . ?b my:index ?b_index . ?c my:index ?c_index . ?d my:index ?d_index . ?c my:not_index ?d . FILTER ( ?b_index < ?c_index ) . FILTER ( ?b_index < ?d_index ) .
  } ;

# Rule: rule_all_eval_to_right_app []
INSERT
  { ?a my:all_eval_to_right ?c . }
WHERE
  {
    ?a my:all_eval_to_right ?b . ?b my:next_index ?c . ?c my:app true .
  } ;

# Rule: rule_operator& []
INSERT
  { ?a my:arity "unary" . ?a my:init true . ?a my:prefix_postfix "prefix" . ?a my:precedence 3 . ?a my:associativity "R" . }
WHERE
  {
    ?a my:text "&" . ?a my:step 1 . ?a my:prev_operation ?b .
  } ;

# Rule: rule_before_all_operands []
INSERT
  { ?a my:before_direct ?c . ?a my:before_by_third_operator ?c . ?a my:before_all_operands ?c . }
WHERE
  {
    ?a my:before_all_operands ?b . ?b my:has_operand ?c .
  } ;

# Rule: rule_complex_boundaries []
INSERT
  { ?c my:complex_boundaries ?b . }
WHERE
  {
    ?a my:in_complex ?c . ?a my:next_index ?b . ?a my:complex_beginning false . ?b my:complex_ending true . ?a my:step 0 .
  } ;

