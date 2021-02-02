# Discrete Event Calculus for SPARQL

# maximum time constant set to 10 explicitly
# initiates/3 was reduced to initiates/2 (drop Time)
    # ASP's `time(T)` is not required, as period of a fluent existance starts by event or via explicit holdsAt fact.

PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX :  <http://vstu.ru/poas/ctrl_structs_2020-05_v1#>

# Rule: DEC 5
# Fluent remains for the next moment if not terminated now
INSERT
  { ?f :holdsAt ?t1 . }
WHERE
  {
    ?f :holdsAt ?t . 
    ?f rdf:type :fluent . 
    BIND( ?t + 1 as ?t1 ) . 
    FILTER( ?t < 10 ).
    FILTER NOT EXISTS { 
        ?e :happens ?t .
        ?e :terminates ?f .
        ?e rdf:type :event . 
    }
  } ;

# Rule: DEC 9
# Fluent appears at the next moment if is initiated now
INSERT
  { ?f :holdsAt ?t1 . }
WHERE
  {
    ?e :happens ?t .
    ?e :initiates ?f .
    ?e rdf:type :event . 
    ?f rdf:type :fluent . 
    BIND( ?t + 1 as ?t1 ) . 
    FILTER( ?t < 10 ).
  } ;
