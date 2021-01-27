# asp_helpers.py
'''
Converting the ontology (structure and data) to ASP and back.
Конвертируем онтологию (структуру и данные) в ASP и обратно.
'''


import re
import string
from timeit import default_timer as timer

from clyngor import solve  # $ pip install clyngor-with-clingo
# from owlready2 import *

from upd_onto import make_triple


class Checkpointer():  # dict
    'Measures time between hits. requires default_timer as timer'
    def __init__(self, start=True):
        super().__init__()
        self.first = timer()
        self.last = self.first
        # if start:
        #     self.hit()
    def reset_now(self):
        self.__init__(start=False)
    def hit(self, label=None) -> float:
        now = timer()
        delta = now - self.last
        if label:
            print((label or 'Checkpoint') + ':', "%.3f" % delta, 's')
        self.last = now
        return delta
    def since_start(self, label=None, hit=False) -> float:
        now = timer()
        delta = now - self.first
        if label:
            print(label or 'Checkpoint:', "%.3f" % delta, 's')
        if hit:
            self.last = now
        return delta
        
        
############# Clingo #############


def run_clingo_on_ontology(onto, rules_fpath=None, stats=False) -> 'onto, {wall_time: float, exclusive_time: float}':
    "Apply incremental (non-mutable) reasoning via Clingo (ASP) and augment the given ontology"
    ch = Checkpointer()
    elapsed_times = {}
    triples = triples_from_ontology(onto)
    # ch.hit("      + Triples created ")
    if rules_fpath:
        use_rules_file(rules_fpath)
    asp = get_rules()
    asp += RDF_CORE_RULES_asp
    asp += triples_to_asp(triples)
    # ch.hit("      + ASP concatenated ")
    if 0:  # debugging ASP input
        with open('clingo_in.asp', 'w') as file:
            file.write(asp)
    # ch.hit("      + ASP saved to file ")
    
    ch.since_start("   ** Preparation took ")
    
    answers = solve(inline=asp, nb_model=1, stats=stats)
    # print(answers)
    answers_list = list(answers)
    # print(len(answers))
    elapsed_times['wall_time'] = ch.hit("   ** Clingo exclusively took ")
    if stats:
        # Note: Access answers.statistics AFTER obtaining the results!
        # print(answers.statistics["Time"])
        # print(answers.statistics["CPU Time"])
        time_str = answers.statistics["Time"]
        time_str = time_str.split('s')[0]
        elapsed_times['exclusive_time'] = float(time_str)
    # ch.hit("      + Obtain answers")
    
    ch.reset_now()
    del asp  # free memory
    
    if not answers_list:
        print("   ** ASP: nothing inferred.")
    answer = answers_list[0]
    answer_triples = {spo for t, spo in answer}
    triples_set = set(triples)
    # ch.hit("      + Obtain triple sets")
    new_triples = answer_triples - triples_set
    # ch.hit("      + Substract sets")
    
    add_triples_to_ontology(onto, new_triples)

    # ch.hit("      + Written to ontology ")
    ch.since_start("   ** Integrating results took ")

    return onto, elapsed_times
    


RDF_CORE_RULES_asp = '''
    % (?a ?p ?b), (?p rdfs:subPropertyOf ?q) -> (?a ?q ?b) .
t(A, Q, B) :- t(A, P, B), t(P, subPropertyOf, Q).
    % (?x rdfs:subClassOf ?y), (?a rdf:type ?x) -> (?a rdf:type ?y) .
t(A, type, Y) :- t(A, type, X), t(X, subClassOf, Y).
'''


def lower_first_char(s):
    return f"{s[0].lower()}{s[1:]}" if s else s

def idfy_name(s):
    return re.sub(r'[^\w\d_]', '', s.replace('-', '_'))
    
NAME2ENTITY_MAP = {}  # name to entity
ID2NAME_MAP = {}  # id to name (logically, reverse of NAME2ENTITY_MAP)
ASP_RULES = {}  # filename to textual rules


def entity_of(s) -> object:
    '''Inverse of string_of(entity): get entity by string `s` or return `s`'''
    return NAME2ENTITY_MAP.get(s, s)
    

def string_of(entity) -> str:
    '''owlready2's entity to string suitable for ASP program (term or double-quoted literal)'''
    id_ = id(entity)
    if id_ in ID2NAME_MAP:
        return ID2NAME_MAP[id_]
    try:
        s = idfy_name(entity.name)
        if s[0] not in string.ascii_letters:
            s = 'o_' + s  # prepand with letter (which is required)
    except AttributeError:
        if type(entity) is str:
            s = '"%s"' % entity
        else:
            s = str(entity)
    s = lower_first_char(s)  # the quote char is not affected
    # add to mapping if not trivial
    if True:  # s != entity:
        NAME2ENTITY_MAP[s] = entity
        ID2NAME_MAP[id(entity)] = s
    ###
    else: print('string_of: skip string:', s, 'from entity:', entity)
    return s


def triples_from_ontology(onto) -> list:
    NAME2ENTITY_MAP.clear()
    ID2NAME_MAP.clear()  # ??
    
    tbox = []
    abox = []

    for cl in onto.classes():
        for sup in cl.is_a:
            tbox += [(string_of(cl), 'subClassOf', string_of(sup))]
        for obj in cl.instances():
            abox += [(string_of(obj), 'type', string_of(cl))]

    for p in onto.properties():
        for sup in p.is_a:
            if 'Property' in sup.name:
                continue  # omit special types of Property - we don't need them
            tbox += [(string_of(p), 'subPropertyOf', string_of(sup))]
        for subj, obj in p.get_relations():
            abox += [(string_of(subj), string_of(p), string_of(obj))]
    return tbox + abox


def add_triples_to_ontology(onto, triples):
    with onto:  # probably not nessessary
        for s, p, o in triples:
            subj = entity_of(s)
            obj = entity_of(o)
            try:
                if p == 'type':
                    subj.is_a.append(obj)
                else:
                    prop = entity_of(p)
                    if type(prop) is str:
                        prop = onto[prop]
                    make_triple(subj, prop, obj)
            except Exception as e:
                print("Exception applying inferred triple: ", s, p, o)
                raise e

    

def triples_to_asp(triples) -> str:
    return "\n".join(f't({", ".join(spo)}).' for spo in triples)
    

def get_rules():
    if not ASP_RULES:
        use_rules_file()
    return next(iter(ASP_RULES.values()))


def use_rules_file(fp='from_swrl.asp'):
    if fp not in ASP_RULES:
        ASP_RULES.clear()
        
        with open(fp) as f:
            asp = f.read()
            
        ASP_RULES[fp] = asp
        
        print("Loaded ASP rules from file:", fp)
        
        

############# DLV #############

DLV_EXECUTABLE_PATH = 'asp/dlv.mingw.exe'
DLV_MAX_N = 1000  # maximum integer to pass as cmd argument -N=1000
DLV_TEMP_IN_FNM = 'dlv_in.asp'

from clyngor.parsing import Parser  # https://github.com/Aluriak/clyngor/blob/f3f38b72b0496ca8b6d6f7d14e1a8691773c8ecf/clyngor/parsing.py#L101

from external_run import invoke_shell, get_process_run_stats


def run_DLV_on_ontology(onto, rules_fpath=None, stats=False) -> 'onto, {wall_time: float, exclusive_time: float}':
    """Apply incremental (non-mutable) reasoning via DLV (ASP) and augment the given ontology.
    Note: stats argument is ignored; returns whole call to run_DLV_solver() time"""
    ch = Checkpointer()
    elapsed_times = {}
    triples = triples_from_ontology(onto)
    # ch.hit("      + Triples created ")
    if rules_fpath:
        use_rules_file(rules_fpath)
    asp = get_rules()
    asp += RDF_CORE_RULES_asp
    asp += triples_to_asp(triples)
    with open(DLV_TEMP_IN_FNM, 'w') as file:
        file.write(asp)
    # ch.hit("      + ASP saved to file ")
    
    ch.since_start("   ** Preparation took ")
    
    answers = run_DLV_solver(DLV_TEMP_IN_FNM)
    answers_list = list(answers)
    elapsed_times['wall_time'] = ch.hit("   ** DLV exclusively took ")
    # if stats:
    #     time_str = answers.statistics["Time"]
    #     time_str = time_str.split('s')[0]
    #     elapsed_times['exclusive_time'] = float(time_str)
    
    ch.reset_now()
    del asp  # free memory
    
    if not answers_list:
        print("   ** ASP: nothing inferred.")
    answer = answers_list[0]
    answer_triples = {spo for t, spo in answer}
    triples_set = set(triples)
    # ch.hit("      + Obtain triple sets")
    new_triples = answer_triples - triples_set
    
    add_triples_to_ontology(onto, new_triples)

    # ch.hit("      + Written to ontology ")
    ch.since_start("   ** Integrating results took ")

    return onto, elapsed_times
    


# $ dlv.mingw.exe -n=1 -N=1000 in_1.dl
def run_DLV_solver(file_in_path, nb_model=1, max_int=DLV_MAX_N) -> 'list of frozensets':
    '''Note: Result of DLV parsing warks normally if nb_model==1'''
    cmd = f"{DLV_EXECUTABLE_PATH} -n={nb_model} -N={max_int} {file_in_path}"
    
    dlv_printout = None
    
    def stdout_handler(stdout, stderr):
        if isinstance(stdout, bytes):
            stdout = stdout.decode('utf8')
            # print(stdout)
        if isinstance(stderr, bytes):
            stderr = stderr.decode('utf8')
            # print(stderr)
            
        nonlocal dlv_printout
        dlv_printout = stdout
        
    
    exitcode = invoke_shell(cmd, gather_stats=False, output_handler=stdout_handler)
    # get_process_run_stats()
    if exitcode != 0:
        print("Error: DLV finished with code", exitcode)
        return ''
    
    assert dlv_printout, 'Expected dlv_printout to contain DLV output.'
    
    version, dlv_printout = dlv_printout.split('\n', maxsplit=1)
    assert version.startswith('DLV'), 'Remove this theck if raised'
    
    # return dlv_printout
    dlv_printout = dlv_printout.strip().lstrip('{').rstrip('}').replace(', ', ' ')

    return [Parser(False, True).parse_terms(dlv_printout)]


if __name__ == '__main__':
    res = run_DLV_solver(r'c:\D\Work\YDev\CompPr\reasoners_compare\ASP\DLV\exe-original\in_1.dl')
    print(res)
    res = res.lstrip('{')
    res = res.rstrip('}')
    
    # >>> Parser(False, True).parse_terms('a(b,c(d))')
    # frozenset({('a', ('b', 'c(d)'))})

    [print(Parser(False, True).parse_terms(r)) for r in res.split(', ')]
