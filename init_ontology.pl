% init_ontology

% :- use_module(library(semweb/rdf_db)).  % migrate to newer wrapper "rdf11"
:- use_module(library(semweb/rdf11)).

% % load syntactic wrappers
% [my_onto].

% load data
load_onto :-
        rdf_load('test_data/test_make_trace_output.rdf', []) ,
		[my_onto], [polyfill], [from_swrl].


dump_rdf(Filename)  :-
		rdf_save(Filename),
		format("Saved all the triples to file:\n\t~s", [Filename]), nl.

count_triples(CountOut) :-
  % получение числа триплетов RDF
	% rdf_graph_property(user, triples(CountOut))  % old variant
	rdf_statistics(triples(CountOut))
	.


% %%%%%%%%%%%%%%%  Запуск  %%%%%%%%%%%%%%%

run_onto :- 
	statistics(walltime, [_ | [_]]),
	load_onto, fail;  % Не важно, как завершится load_onto - 
					  % эта ветка выполнится всё равно.
	
			statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
			format("Loading the ontology took ~d ms.", [TimeSinceLastCall]), nl ,
	dump_rdf('test_data/prolog_pre-output.rdf'),
	run_swrl, !.         



% Запуск всех "правил SWRL" в цикле, пока после очередного прогона триплеты не перестанут появляться.
  % обёртка рекурсии
run_swrl :- 
	count_triples(Count), 
	write(Count), writeln(" triples at start."), 
	statistics(walltime, [_ | [_]]),
	run_swrl(Count, 1), !.

run_swrl :-   % Когда граф пуст / не создан
	statistics(walltime, [_ | [_]]),
	% not(swrl_rule_once), 
			% statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
			% format("Run-once-rules finished in ~d ms.", [TimeSinceLastCall]), nl ,
	run_swrl(0, 1), !.



run_swrl(Prev3plesCount, Depth) :- 
	format("Reasoning started from ~d triples (take ~d)...", [Prev3plesCount, Depth]), nl, 
	not(swrl_rule),  % NOT, as it fails anyway
	(
		count_triples(Count)  % получение числа триплетов
		;
		Count = Prev3plesCount  % if still nothing in the graph.
	),
	(
		Count > Prev3plesCount,     % новые триплеты появились, нужно продолжать
		run_swrl(Count, Depth + 1)  % шаг рекурсии
		;
		% !, 
		statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
		format("Reasoning finished in ~d iterations, ~d triples in graph total.\n\tTime it took: ~d ms.", [Depth, Count, TimeSinceLastCall]), nl,
		
		dump_rdf('test_data/prolog_output.rdf')
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