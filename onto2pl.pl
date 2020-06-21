:- ensure_loaded( library(rdfs2pl) ).
:- use_module(library(semweb/rdf_db)).
% :- use_module(library(semweb/rdf_turtle)).
% :- use_module(library(semweb/rdf_http_plugin)).


load_onto :-
        rdf_load('test_data/test_all_output.rdf').

w_onto :-
        load_onto,
        write_schema(ctrlstrct,'http://vstu.ru/poas/ctrl_structs_2020-05_v1#',[use_labels(true)]).


/*

  swipl -g "[onto2pl],w_onto,halt." > my_onto.pl
  
*/
