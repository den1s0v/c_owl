:- ensure_loaded( library(rdfs2pl) ).
:- use_module(library(semweb/rdf_db)).
% :- use_module(library(semweb/rdf_turtle)).
% :- use_module(library(semweb/rdf_http_plugin)).


load_onto :-
        rdf_load('test_data/test_make_trace_output.rdf').

w_onto :-
        load_onto,
        write_schema(ctrlstrct,'http://vstu.ru/poas/ctrl_structs_2020-05_v1#',[use_labels(true)]).


load_onto2 :-
        rdf_load('pl_in_expr.rdf').

w_onto2 :-
        load_onto2,
        write_schema(penskoy,'http://penskoy.n/expressions#',[use_labels(true)]).


/*

  swipl -g "[onto2pl],w_onto,halt." > my_onto.pl
  swipl -g "[onto2pl],w_onto2,halt." > expr_onto_definitions.pl
  
*/
