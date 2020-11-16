% init_ontology

:- ensure_loaded( library(rdfs2pl) ).
:- use_module(library(semweb/rdf_db)).

% % load syntactic wrappers
% [my_onto].

% load data
load_onto :-
        rdf_db:rdf_load('test_data/test_make_trace_output.rdf', []) ,
		[my_onto], [polyfill], [from_swrl].




% %%%%%%%%%%%%%%%  Запуск  %%%%%%%%%%%%%%%

run_onto :- 
	statistics(walltime, [_ | [_]]),
	load_onto, fail;  % Не важно, как завершится load_onto - 
					  % эта ветка выполнится всё равно.
	
			statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
			format("Loading the ontology took ~d ms.", [TimeSinceLastCall]), nl ,
	run_swrl, !.         


% Запуск всех "правил SWRL" в цикле, пока триплеты не перестанут появляться после прогона.
  % обёртка рекурсии
run_swrl :- 
	rdf_graph_property(user, triples(Count)), 
	statistics(walltime, [_ | [_]]),
	run_swrl(Count, 1), !.

run_swrl :-   % Когда граф пуст / не создан
	% statistics(walltime, [_ | [_]]),
	% not(swrl_rule_once), 
			% statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
			% format("Run-once-rules finished in ~d ms.", [TimeSinceLastCall]), nl ,
	run_swrl(0, 1), !.

% run_swrl(Prev3plesCount) :- 
	% statistics(walltime, [_ | [_]]),
	% run_swrl(Prev3plesCount, 1).

run_swrl(Prev3plesCount, Depth) :- 
	format("Reasoning started from ~d triples ...", [Prev3plesCount]), nl, 
	not(swrl_rule),  % NOT, as it fails anyway
	rdf_graph_property(user, triples(Count)),  % получение числа триплетов
	(
		Count > Prev3plesCount,     % новые триплеты появились, нужно продолжать
		run_swrl(Count, Depth + 1)  % шаг рекурсии
		;
		% !, 
		statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
		format("Reasoning finished in ~d iterations, ~d triples in graph total.\nTime it took: ~d ms.", [Depth, Count, TimeSinceLastCall]), nl
	).


report_TimeSinceStart :-
		statistics(walltime, [TimeSinceStart | [_TimeSinceLastCall]]),
		format("Time Since Start: ~d ms.", [TimeSinceStart]), nl.


/*

[init_ontology].
run_onto.




	load_onto,
	swrl_rule.
% P = 33574 ;
	swrl_rule.
% P = 33657.

rdf_graph_property(user, triples(P)).
*/