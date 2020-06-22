# stardog_test

import time
# _start_time = time.time()
# print("Running...")

# print("Started at", _start_time, "and running...")

# def secondsToStr(t):
#     return "%d:%02d:%02d.%03d" % \
#         reduce(lambda ll,b : divmod(ll[0],b) + ll[1:],
#             [(t*1000,),1000,60,60])


import stardog
from pprint import pprint


# help(stardog.Connection.add)
# exit(1)


# stardog query --reasoning rule_ex "SELECT ?s ?v { ?s :area ?v } LIMIT 10"

from stardog_credentails import *

def run_query(ontology_prefix=None):
    
    ontology_prefix = ontology_prefix or "http://vstu.ru/poas/ctrl_structs_2020-05_v1#"
    
    # conn_details = {
    # 'endpoint': 'http://localhost:5820',
    # 'username': 'admin',
    # 'password': 'admin'
    # }

    # dbname = "ctrlstrct_db"
    # # dbname = "rule_ex"
    # # graphname = "urn:graph1"


    with stardog.Connection(dbname, **conn_details) as conn:
        # query = """PREFIX onto: <http://vstu.ru/poas/ctrl_structs_2020-05_v1#>
              
        #       SELECT DISTINCT ?s ?o WHERE {  
        #           # ?s a ?o . 
        #           # ?o rdfs:subClassOf onto:Erroneous 
        #           ?o rdfs:subClassOf onto:act 
        #       }"""
        
        # ?o a onto:act_begin
        # ?s a ?o . 
        
        # SELECT ?s ?o WHERE { ?o rdfs:subClassOf onto:act }
        
              # ?s a / rdfs:subClassOf onto:act .  # prop chain!
              # ?o a onto:act .  # indirect cast does not work without reasoning!

        query = """PREFIX onto: <%s>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
          
          SELECT DISTINCT * WHERE {  
              # ?s a onto:DebugObj .
              # ?o a onto:DebugObj .
              ?s a onto:current_act .
              # ?s a onto:act . 
              # ?s a onto:trace . 
              # ?s ?p ?o .
              ?s a ?o .
              # ?p a owl:DatatypeProperty .
              # ?s onto:next ?o .
              # ?s onto:before ?o .
              # ?s onto:next_sibling ?o .
              # ?s onto:before ?o .
              # ?o rdfs:subClassOf onto:Erroneous 
              # ?o rdfs:subClassOf onto:correct_act 
          }""" % ontology_prefix
        
        # r = conn.select(query, reasoning=True)
        # r = conn.select(query, reasoning=False)
        r = conn.select(query, reasoning=bool(1))
        
        pprint(r['results']['bindings'])
        print(len(r['results']['bindings']), "total.")

def main(ontology_prefix=None) -> float:
    _start_time = time.time()
    print("Running SPARQL query...")
    
    try:
        run_query(ontology_prefix)
        # pass
    except Exception as e:
        print(e)
        pass
  
    seconds = time.time() - _start_time
    print("[%.2f sec elapsed]" % seconds, end=" ")
    return seconds

    
if __name__ == '__main__':
    main()

