from __eval.expression_makeup import *
from ctrlstrct_run import *

# main()
    
DATA = test_items_to_expressions(load_all_test_items())
PREV_COUNT = {}


def proccess_onto_with_reasoner(reasoning, count=30):
    
    expr_chain = make_expr_chain(DATA, count)
        
    if reasoning in PREV_COUNT and len(expr_chain) == PREV_COUNT[reasoning]:
        print('Skip this iteration')
        return None
        
    PREV_COUNT[reasoning] = len(expr_chain)
    
    if reasoning == "pellet":
        
        onto = prepare_ontology(expr_chain, inject_swrl=True)
        
        if True:
            debug_rdf_fpath = 'exprs_dump.rdf'  # +"_ext.rdf"
            onto.save(file=debug_rdf_fpath, format='rdfxml')
            debug_rdf_fpath = 'exprs_dump.n3'
            onto.save(file=debug_rdf_fpath, format='ntriples')
            print(f"Saved RDF file: {debug_rdf_fpath} !")
        else:
            debug_rdf_fpath = None


        print(">_ running Pellet ...")
        
        # if _eval_max_traces is not None:
        measure_stats_for_pellet_running()
        
        start = timer()
        
        with onto:
            # запуск Pellet
            try:
                sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=0)
            except Exception as e:
                print(e)
            
        end = timer()
        seconds = end - start
        time_report = "   Time elapsed: %.3f s." % seconds
        print(">_ Pellet finished")
        print(time_report)
        
        # if _eval_max_traces is not None:
        run_stats = get_process_run_stats()
        run_stats.update({"wall_time": seconds})
        run_stats.update({"count": len(expr_chain)})

        if debug_rdf_fpath:
            onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
            print(f"Saved RDF file: {debug_rdf_fpath}_ext.rdf !")
        return run_stats
            
    
    onto = prepare_ontology(expr_chain, inject_swrl=False)

            
            
    if reasoning in ("clingo", "dlv"):
        raise RuntimeError("ASP solver does not support match(regex, str)!")
        print(f">_ running {reasoning} ...")
        
        import asp_helpers
        
        measure_f, run_f = {
            "clingo": (measure_stats_for_clingo_running, asp_helpers.run_clingo_on_ontology),
            "dlv": (measure_stats_for_dlv_running, asp_helpers.run_DLV_on_ontology),
        }.get(reasoning)
        
        # if _eval_max_traces is not None:
        measure_f()
            
        start = timer()
        
        # запуск Clingo / DLV
        onto, elapsed_times = run_f(onto, rules_fpath='expr_penskoy.asp', stats=True)  # ?
            
        end = timer()
        seconds = end - start
        time_report = "   Time elapsed: %.3f s." % seconds
        print(f">_ {reasoning} finished")
        print(time_report)
        
        # if _eval_max_traces is not None:
        run_stats = get_process_run_stats()
        run_stats.update(elapsed_times)  # add data from dict
        return run_stats

        # if debug_rdf_fpath:
        #     onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
        #     print(f"Saved RDF file: {debug_rdf_fpath}_ext.rdf !")

            
    if reasoning == "prolog":
        name_in = "pl_in_expr.rdf"
        name_out = "pl_out_expr.rdf"
        onto.save(file=name_in, format='rdfxml')
        
        eval_stats = run_swiprolog_reasoning(name_in, name_out, verbose=1, command_name="run_ontology")
        
        # if _eval_max_traces is not None:
        eval_stats.update({"count": len(expr_chain)})
        return eval_stats
        
        # clear_ontology(onto)
        # onto = get_ontology("file://" + name_out).load()
        # seconds = eval_stats['wall_time']
        
            
    if reasoning in ('sparql', 'jena'):
        name_in = f"{reasoning}_in_expr.n3"
        name_out = f"{reasoning}_out_expr.n3"
        onto.save(file=name_in, format='ntriples')
        
        rules_path = {
            'jena': "jena/all_for_exprs.rules",
            'sparql': "expr_penskoy.ru", 
        }[reasoning]
        
        eval_stats = run_jena_reasoning(name_in, name_out, reasoning_mode=reasoning, verbose=1, rules_path=rules_path)
        
        # if _eval_max_traces is not None:
        eval_stats.update({"count": len(expr_chain)})
        return eval_stats
        
        # clear_ontology(onto)
        # onto = get_ontology("file://" + name_out).load()
        # seconds = eval_stats['wall_time']
    raise ValueError(reasoning)
        
    
def eval_expressions():
    eval_results = []
    # 46
    for n in sorted({
                        # *range(50, 52 + 1, 6),
                        # *range(5, 20 + 1, 5),
                        *range(25, 35 + 1, 5),
                    }):
        # reasoners = ("pellet", )
        # reasoners = ("prolog", );
        # reasoners = ("sparql", )
        # reasoners = ("jena", )
        # reasoners = ("clingo", )
        # reasoners = ("dlv", )
        # reasoners = ("jena", "clingo")
        # reasoners = ("jena", "sparql")
        reasoners = ("jena", "prolog", "sparql")
        # reasoners = ("clingo", "jena", "prolog", "sparql")
            
        for reasoning_type in reasoners:
            print(' >  >  >  >  >  >  >  >  >  >  >  >  > ')
            print(f"  Running {n} operands with {reasoning_type}")
            print(' <  <  <  <  <  <  <  <  <  <  <  <  < ')
            
            eval_result = proccess_onto_with_reasoner(count=n, reasoning=reasoning_type)
            
            if eval_result is None:
                continue
            
            eval_item = {
                'dataset': 'penskoy-expressions',
                'reasoner': reasoning_type,
                'count': n,
            }
            eval_item.update(eval_result)
            
            # dump current result
            with open('partial_eval_expr.txt', "a") as file:
                file.write(str(eval_item))
                file.write('\n')
            
            eval_results.append(eval_item)
            
        # break
            
    # dump full result
    with open('saved_eval_expr.txt', "a") as file:
        for eval_item in eval_results:
            file.write(str(eval_item))
            file.write('\n')
            
    print(' ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^ ')    
    print("Expr eval finished.") 
    # exit()


def convert_rules():
    from rule_converter import to_prolog, to_jena, to_sparql, to_clingo
    from __eval.expression_laws import get_owl_swrl_laws
    _owl, swrl = get_owl_swrl_laws()
    # to_prolog(swrl, out_path='expr_penskoy.pl', iri_prefix="http://penskoy.n/expressions#")
    # to_jena(swrl, out_path='expr_penskoy.jena_rules')
    to_sparql(swrl, out_path='expr_penskoy.ru', base_iri="http://penskoy.n/expressions#")
    # to_clingo(swrl, out_path='expr_penskoy.asp')  # match() built-in cannot be converted to ASP !!!


def main():
    # convert_rules()
    eval_expressions()

if __name__ == '__main__':
    main()
