# run_dec.py
# DEC: Discrete Event Calculus


from ctrlstrct_run import *



N_MAXSTEP = 10
N_FLUENTS = 2
N_EVENTS = 2


r'''
CMD_SPARQL = r'java -jar jena/Jena.jar sparql .\sparql\dec_in.ttl .\sparql\DEC.ru .\sparql\dec_out.n3'
CMD_CLINGO = r'clingo.exe .\sparql\DEC.lp .\sparql\dec_in.lp -n 0'
'''

DIRECTORY = './sparql/'

TEMPLATE_EXT = '.tpl'
INPUT_TEMPLATES_SPARQL = [DIRECTORY + f for f in ('dec_in.ttl.tpl', 'DEC.ru.tpl')]
INPUT_TEMPLATES_CLINGO = [DIRECTORY + 'dec_in.lp.tpl']


class SPARQL_Syntax:
    @staticmethod
    def declaration(entity) -> str:
        return f':{entity} rdf:type :{entity.class_name()} .'
    @staticmethod
    def relation(subj, prop, obj) -> str:
        if not isinstance(obj, int):
            obj = f':{obj}'
        return f':{subj} :{prop} {obj} .'

class CLINGO_Syntax:
    @staticmethod
    def declaration(entity) -> str:
        return f'{entity.class_name()}({entity}).'
    @staticmethod
    def relation(subj, prop, obj) -> str:
        return f'{prop}({subj}, {obj}).'


class Fluent:
    def __init__(self, i):
        self.i: int = i
        self.holds_at_0 = bool(i % 2)
        self.initiated_by = []  # Events
        self.terminated_by = [] # Events
    def __str__(self) -> str: return f'f{self.i}'
    def class_name(self) -> str: return 'fluent'
    def make_fillins(self, syntax: 'class') -> dict:
        "fill-ins list by template field"
        return {
        'FLUENTS_DECLARATION': [syntax.declaration(self)],
        'FLUENTS_DEPENDENCIES': [
            syntax.relation(ev, 'initiates', self) for ev in self.initiated_by
        ] + [
            syntax.relation(ev, 'terminates', self) for ev in self.terminated_by
        ],
        'FLUENTS_INITIAL_STATE': [syntax.relation(self, 'holdsAt', 0)] if self.holds_at_0 else ()
        }

class Event:
    def __init__(self, i):
        self.i: int = i
        self.happens_at = []  # ints
    def __str__(self) -> str: return f'ev{self.i}'
    def class_name(self) -> str: return 'event'
    def make_fillins(self, syntax: 'class') -> dict:
        "fill-ins list by template field"
        return {
        'EVENTS_DECLARATION': [syntax.declaration(self)],
        'EVENTS_HAPPEN': [
            syntax.relation(self, 'happens', moment) for moment in self.happens_at
        ],
        }


def prepare_entities(n_maxstep=N_MAXSTEP, n_fluents=N_FLUENTS, n_events=N_EVENTS):
    
    fluents = [Fluent(i) for i in range(n_fluents)]
    events  = [Event (i) for i in range(n_events)]
    
    # set fire moments
    occupied_moments = set()  # prevent sharing moments among events
    for event in events[::-1]:
        moments = set(range(event.i, n_maxstep, event.i + 2))
        event.happens_at.extend(sorted(moments - occupied_moments))
        occupied_moments |= moments
    
    # bind fluents to events: 2 events for each fluent
    for fluent in fluents:
        fluent.initiated_by.append(events[fluent.i % n_fluents])
        fluent.terminated_by.append(events[-(1 + fluent.i % n_fluents)])
        
    return fluents, events


LOADED_FILES = {}

def file_contents(filepath) -> str:
    if filepath in LOADED_FILES:
        return LOADED_FILES[filepath]
    
    with open(filepath) as f:
        contents = f.read()
            
    LOADED_FILES[filepath] = contents
    # print("Loaded contents of file:", filepath)
    return contents
    
def simple_format(format_string: str, replacements: dict) -> str:
    '''same as `format_string.format(**replacements)` but:
    - only simple keys are supported: {key1}
    - only keys from `replacements` dict are considered (no fail on arbitrarily used { or })
    '''
    for key, replace_with in replacements.items():
        format_string = format_string.replace('{' + key + '}', replace_with)
    return format_string

def prepare_input_files(template_files: list, fillins: dict):
    for template_file in template_files:
        template = file_contents(template_file)
        filled_template = simple_format(template, fillins)
        new_filename = template_file.replace(TEMPLATE_EXT, '')
        with open(new_filename, 'w') as f:
            f.write(filled_template)
        
def make_fillins(fluents, events, syntax: 'class') -> dict:
    fillins = {
        'MAXSTEP': N_MAXSTEP,
        'FLUENTS_DECLARATION': [],
        'FLUENTS_DEPENDENCIES': [],
        'FLUENTS_INITIAL_STATE': [],
        'EVENTS_DECLARATION': [],
        'EVENTS_HAPPEN': [],
    }
    for entity in [*fluents, *events]:
        for key, vals in entity.make_fillins(syntax).items():
            fillins[key].extend(vals)
    
    return {key: ('\n'.join(vals) if type(vals) is list else str(vals)) for key, vals in fillins.items()}

    
def prepare_eval_case_input(n_params: dict, syntaxes=(SPARQL_Syntax, CLINGO_Syntax)):
    for syntax in syntaxes:
        if syntax is SPARQL_Syntax:
            template_files = INPUT_TEMPLATES_SPARQL
        elif syntax is CLINGO_Syntax:
            template_files = INPUT_TEMPLATES_CLINGO
        else:
            raise ValueError("Unknown syntax: " + str(syntax))
        prepare_input_files(template_files, 
            make_fillins(*prepare_entities(**n_params), syntax))
    
    
# if __name__ == '__main__':
    # prepare_eval_case_input(dict(n_maxstep=20, n_fluents=3, n_events=4))
    
    # dct = make_fillins(*prepare_entities(), SPARQL_Syntax)
    # prepare_input_files(INPUT_TEMPLATES_SPARQL, dct)
    # print("SPARQL")
    # dct = make_fillins(*prepare_entities(), CLINGO_Syntax)
    # prepare_input_files(INPUT_TEMPLATES_CLINGO, dct)
    # print("CLINGO")

def proccess_with_reasoner(reasoning, count=10):
    
    # expr_chain = make_expr_chain(DATA, count)
        
    # if reasoning in PREV_COUNT and len(expr_chain) == PREV_COUNT[reasoning]:
    #     print('Skip this iteration')
    #     return None
        
    # PREV_COUNT[reasoning] = len(expr_chain)
    
            
    
    # onto = prepare_ontology(expr_chain, inject_swrl=False)


    if reasoning in ("clingo", "dlv"):
        assert reasoning == "clingo"
        
        import asp_helpers
        
        measure_f, run_f = {
            "clingo": (measure_stats_for_clingo_running, asp_helpers.run_clingo_on_ontology),
            "dlv": (measure_stats_for_dlv_running, asp_helpers.run_DLV_on_ontology),
        }.get(reasoning)
        
        # if _eval_max_traces is not None:
        measure_f()
        elapsed_times = {}
            
        start = timer()
        
        answers = asp_helpers.solve(["./sparql/DEC.lp", "./sparql/dec_in.lp"], nb_model=1, stats=True)
        # print(answers)
        answers_list = list(answers)
        # print(len(answers))
        if True:  # stats:
            time_str = answers.statistics["Time"]
            time_str = time_str.split('s')[0]
            elapsed_times['exclusive_time'] = float(time_str)
        
        # запуск Clingo / DLV
        # onto, elapsed_times = run_f(onto, rules_fpath=DIRECTORY + 'DEC.lp', stats=True)  # ?
            
        end = timer()
        seconds = end - start
        elapsed_times['wall_time'] = seconds
        time_report = "   Time elapsed: %.3f s." % seconds
        print(f">_ {reasoning} finished")
        print(time_report)
        
        # if _eval_max_traces is not None:
        run_stats = get_process_run_stats()
        run_stats.update(elapsed_times)  # add data from dict
        run_stats.update({"count": count})
        return run_stats

        # if debug_rdf_fpath:
        #     onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
        #     print(f"Saved RDF file: {debug_rdf_fpath}_ext.rdf !")

            
    # if reasoning == "prolog":
    #     name_in = "pl_in_expr.rdf"
    #     name_out = "pl_out_expr.rdf"
    #     onto.save(file=name_in, format='rdfxml')
        
    #     eval_stats = run_swiprolog_reasoning(name_in, name_out, verbose=1, command_name="run_ontology")
        
    #     # if _eval_max_traces is not None:
    #     eval_stats.update({"count": len(expr_chain)})
    #     return eval_stats
        
    #     # clear_ontology(onto)
    #     # onto = get_ontology("file://" + name_out).load()
    #     # seconds = eval_stats['wall_time']
        
            
    if reasoning in ('sparql', 'jena'):
        name_in = DIRECTORY + "dec_in.ttl"
        name_out = DIRECTORY + "dec_out.n3"
        # onto.save(file=name_in, format='ntriples')
        
        rules_path = {
            'jena': "======Not=Applicable======",
            'sparql': "./sparql/DEC.ru", 
        }[reasoning]
        
        eval_stats = run_jena_reasoning(name_in, name_out, reasoning_mode=reasoning, verbose=1, rules_path=rules_path)
        
        # if _eval_max_traces is not None:
        eval_stats.update({"count": count})
        return eval_stats
        
        # clear_ontology(onto)
        # onto = get_ontology("file://" + name_out).load()
        # seconds = eval_stats['wall_time']
    raise ValueError(reasoning)
        

def eval_DEC():
    eval_results = []
    m = 10 ** 3
    for n in sorted({
                        *range(15 * m, 40 * m + 1, 5 * m),
                        # *range(25, 30 + 1, 5),
                        # *range(32, 35 + 1, 5),
                    }):
        # reasoners = ("clingo", )
        # reasoners = ("sparql", )
        reasoners = ("clingo", "sparql")
        
        prepare_eval_case_input(dict(n_maxstep=n, n_fluents=n // 5, n_events=n // 4))
                
                
        for reasoning_type in reasoners:
            print(' >  >  >  >  >  >  >  >  >  >  >  >  > ')
            print(f"  Running {n} steps with {reasoning_type}")
            print(' <  <  <  <  <  <  <  <  <  <  <  <  < ')
            
            eval_result = proccess_with_reasoner(count=n, reasoning=reasoning_type)
            
            if eval_result is None:
                continue
            
            eval_item = {
                'dataset': 'ASP-DEC',
                'reasoner': reasoning_type,
                'count': n,
            }
            eval_item.update(eval_result)
            
            # dump current result
            with open('partial_eval_DEC.txt', "a") as file:
                file.write(str(eval_item))
                file.write('\n')
            
            eval_results.append(eval_item)
            
        # break
            
    # dump full result
    with open('saved_eval_DEC.txt', "a") as file:
        for eval_item in eval_results:
            file.write(str(eval_item))
            file.write('\n')
            
    print(' ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^  ^ ')    
    print("DEC eval finished.") 
    # exit()


def main():
    eval_DEC()

if __name__ == '__main__':
    main()
