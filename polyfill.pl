
lessThan(A, B) :- A < B .

greaterThan(A, B) :- A > B .

notEqual(A, B) :- A =\= B .
notEqual(A, B) :- not(equal(A, B)).

equal(A, A).
equal(A, B) :- rdf_compare(=, A, B).

add(C, A, B) :- C is A + B.

