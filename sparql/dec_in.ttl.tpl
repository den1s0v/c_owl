# dec_in.ttl

@prefix : <http://vstu.ru/poas/ctrl_structs_2020-05_v1#> .

@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Declare fluents and events causing fluents to change

{FLUENTS_DECLARATION}

{EVENTS_DECLARATION}


# Plug events to dependent fluents

{FLUENTS_DEPENDENCIES}


# Initial state of fluents

{FLUENTS_INITIAL_STATE}


# Moments when events occur

{EVENTS_HAPPEN}
