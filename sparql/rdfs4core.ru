PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
PREFIX my:  <http://vstu.ru/poas/ctrl_structs_2020-05_v1#>

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


