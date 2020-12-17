
lessThan(A, B) :- A < B .

greaterThan(A, B) :- A > B .

% notEqual(A, B) :- writeln(A), writeln(B), fail .
% notEqual(A, B) :- A =\= B .
notEqual(A, B) :- not(equal(A, B)).

equal(A, A).
equal(A, B) :- rdf_compare(=, A, B).

add(C, A, B) :- C1 is A + B, C1 = C.


% ?- pack_install(regex).
:- use_module(library(regex)).
matches(A, B) :- A =~ B.  % https://github.com/mndrix/regex

% true :- true^^xsd:boolean .
% true - is a builtin !

