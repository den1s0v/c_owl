% init_ontology

:- ensure_loaded( library(rdfs2pl) ).
:- use_module(library(semweb/rdf_db)).

% % load syntactic wrappers
% [my_onto_hand].

% load data
load_onto :-
        rdf_db:rdf_load('test_data/test_all_output.rdf', []) ,
		[my_onto_hand].

% ################ Служебные правила ################


% # (s1)
% "next_to__current_act": """
	% current_act(?a), index(?a, ?ia), add(?ib, ?ia, 1),
	% act(?b), index(?b, ?_ib),
	% equal(?_ib, ?ib), 
	 % -> next(?a, ?b)
	 
swrl_rule() :- 
	current_act(A) , % act(B) ,
	index(A, ^^(IA, _)) , 
	index(B, ^^(IB, _)) , 
	IB =:= IA + 1 ,

	next_sibling(Pr, B), correct_act(Pr),
	% exec_time(Pr, ^^(NPr,_)),
	% exec_time(B, ^^(NB,_)), 
	% NPr < NB ,  % должен стоять иметь следующий номер!
	index(Pr, ^^(IPr,_)), 
	IPr =< IA ,  % пред. брат B должен стоять НЕ позже предыдущего акта A!
	
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#next', B) ,
	% print("A:") , print(A) , nl,
	% print("P:") , print(Pr) , nl,
	% print("B:") , print(B) , nl,
	% % print(B) , nl,
	% % format(' n~d --next-> n~d', [NPr, NB]) , nl,
	% nl,
	fail.
	
	% OK! Работает в прологе:
		% ?- swrl_rule.
		% ?- next(A,B).
	
	
% # (s2)
% "assign_next_sibling_0-1-b": """
	% trace(?a),
	% act_begin(?b), exec_time(?b, ?_ib),
	% equal(?_ib, 1),
	% # DifferentFrom(?a, ?b),  # stardog fails the rule here!
	 % -> next_sibling(?a, ?b)
	
swrl_rule_once() :- 
	trace(A) , act_begin(B) ,
	not(A = B) ,
	in_trace(B, A) ,
	exec_time(B, ^^(IB, _)) , 
	IB =:= 1 ,
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#next_sibling', B) ,
	% print(B) , nl,
	% print(IB) , nl,
	% nl,
	fail.


% # (s3)
% "assign_next_sibling_0-1-e": """
	% trace(?a),
	% act_end(?b), exec_time(?b, ?_ib),
	% equal(?_ib, 1), 
	% # DifferentFrom(?a, ?b),
	 % -> next_sibling(?a, ?b)

swrl_rule_once() :- 
	trace(A) , act_end(B) ,
	not(A = B) ,
	in_trace(B, A) ,
	exec_time(B, ^^(IB, _)) , 
	IB =:= 1 ,
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#next_sibling', B) ,
	% print(B) , nl,
	% print(IB) , nl,
	% nl,
	fail.


% # (s4)
% "assign_next_sibling-b": """
	% act_begin(?a), exec_time(?a, ?ia), add(?_ib, ?ia, 1),
	% act_begin(?b), exec_time(?b, ?ib),  # unification of a bound var does rebind in stardog ??!
	% equal(?_ib, ?ib), 
	% # DifferentFrom(?a, ?b),
	% executes(?a, ?st),
	% executes(?b, ?st),
	 % -> next_sibling(?a, ?b)

swrl_rule_once() :- 
	act_begin(A) , act_begin(B) ,
	not(A = B) ,
	not(next_sibling(A, B)) ,
	in_trace(A, T) , in_trace(B, T) , 
	exec_time(A, ^^(IA, _)) , 
	exec_time(B, ^^(IB, _)) , 
	executes(A, St),
	executes(B, St),
	IB =:= IA + 1 ,
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#next_sibling', B) ,
	% print(B) , nl,
	% print(IB) , nl,
	fail.


% # (s5)
% "assign_next_sibling-e": """

swrl_rule_once() :- 
	act_end(A) , act_end(B) ,
	not(A = B) ,
	not(next_sibling(A, B)) ,
	in_trace(A, T) , in_trace(B, T) , 
	exec_time(A, ^^(IA, _)) , 
	exec_time(B, ^^(IB, _)) , 
	executes(A, St),
	executes(B, St),
	IB =:= IA + 1 ,
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#next_sibling', B) ,
	% print(B) , nl,
	% print(IB) , nl,
	fail.


% # (s6)
% "DepthIncr": """
	% act_begin(?a), next(?a, ?b), act_begin(?b), 
	% # depth(?a, ?da), add(?db, ?da, 1)
	 % -> parent_of(?a, ?b)  # depth(?b, ?db),

swrl_rule() :- 
	act_begin(A) , act_begin(B) ,
	next(A, B),
	rdf_assert(A, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#parent_of', B) ,
	% print(B) , nl,
	% print(IB) , nl,
	fail.


% # (s7)
% "DepthSame_b-e": """
	% act_begin(?a), next(?a, ?b), act_end(?b), 
	% parent_of(?p, ?a),
	 % -> parent_of(?p, ?b), corresponding_end(?a, ?b)

swrl_rule() :- 
	act_begin(A) ,
	next(A, B) ,
	act_end(B) ,
	parent_of(P, A) ,
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#parent_of', B) ,
	fail.


% # (s8)
 % # проверка на Начало А - Конец Б (должен был быть Конец А) - CorrespondingActsMismatch_Error
% "DepthSame_e-b": """
	% act_end(?a), next(?a, ?b), act_begin(?b), 
	% parent_of(?p, ?a)
	 % -> parent_of(?p, ?b)

swrl_rule() :- 
	act_end(A) ,
	next(A, B) ,
	act_begin(B) ,
	parent_of(P, A) ,
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#parent_of', B) ,
	fail.


% # (s9)
% "DepthDecr": """
	% act_end(?a), next(?a, ?b), act_end(?b), 
	% parent_of(?p, ?a)
	 % -> corresponding_end(?p, ?b)

swrl_rule() :- 
	act_end(A) ,
	next(A, B) ,
	act_end(B) ,
	parent_of(P, A) ,
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#corresponding_end', B) ,
	fail.


% # (s10)
% "SameParentOfCorrActs": """
	% corresponding_end(?a, ?b), parent_of(?p, ?a)
	 % -> parent_of(?p, ?b)

swrl_rule() :- 
	corresponding_end(A, B) ,
	parent_of(P, A) ,
	not(parent_of(P, B)) ,
	rdf_assert(P, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#parent_of', B) ,
	fail.


% ################ Производящие правила ################


% # OK (g1) !
% "connect_FunctionBegin": """
	% current_act(?a),
	% act_begin(?a),
	% func(?func_), 
	% executes(?a, ?func_),
	% body(?func_, ?st),
	
	% next(?a, ?b),
	% act_begin(?b),
	% executes(?b, ?st),
	% # SameAs(?st, ?_st), # stardog fails with error here
	
	% # check that previous execution of st was in correct sub-trace
	% next_sibling(?pr, ?b), correct_act(?pr),
	 % -> correct_act(?b), current_act(?b), FunctionBegin(?b)

swrl_rule() :- 
	current_act(A) ,
	act_begin(A) ,
	func(Func) ,
	executes(A, Func),
	body(Func, St),
	
	next(A, B) ,
	act_begin(B) ,
	executes(B, St) ,
	
	% next_sibling(Pr, B), correct_act(Pr),
	% index(Pr, ^^(IPr,_)), index(B, ^^(IB,_)), IPr < IB ,  % должен стоять ПОСЛЕ!
	
	not(correct_act(B)) ,
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#correct_act') ,
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#current_act') ,
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#FunctionBegin') ,
	print("FunctionBegin: "),nl, print(A),nl, print(B),nl,nl,
	fail.


% # (g2) - Infers nothing  in Stardog
% "--- connect_SequenceBegin": """
	% current_act(?a),
	% act_begin(?a),
	% sequence(?block), 
	% executes(?a, ?block),
	% body_item(?block, ?st),
	% first_item(?st),
	
	% next(?a, ?b),
	% act_begin(?b),
	% executes(?b, ?st),
	
	% next_sibling(?pr, ?b), correct_act(?pr),
	 % -> correct_act(?b), current_act(?b), SequenceBegin(?b)

swrl_rule() :- 
	current_act(A) ,
	% act_begin(A) ,
	sequence(Block) ,
	executes(A, Block),
	body_item(Block, St),
	first_item(St),
	
	next(A, B) ,
	act_begin(B) ,
	executes(B, St) ,
	
	% next_sibling(Pr, B), correct_act(Pr), 
	% index(Pr, ^^(IPr,_)), index(B, ^^(IB,_)), IPr < IB ,  % должен стоять ПОСЛЕ!
	
	not(correct_act(B)) ,
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#correct_act') ,
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#current_act') ,
	rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#SequenceBegin') ,
	print("SequenceBegin: ") , print(B) , nl,
	fail.




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
	statistics(walltime, [_ | [_]]),
	not(swrl_rule_once), 
			statistics(walltime, [_TimeSinceStart | [TimeSinceLastCall]]),
			format("Run-once-rules finished in ~d ms.", [TimeSinceLastCall]), nl ,
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