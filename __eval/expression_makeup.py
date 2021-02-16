# expressions-nikita.py

import json

from owlready2 import *

# omit this three imports if running this file in debug.
if  __name__ != '__main__':
	from ctrlstrct_run import clear_ontology, uniqualize_iri
	from upd_onto import make_triple
	from __eval.expression_laws import inject_laws


'''
    String getName(int step, int index) {
        return "op__" + step + "__" + index;
    }
'''

def getName(step: int, index:int) -> str:
    return "op__" + str(step) + "__" + str(index);

'''
    public List<BackendFact> getBackendFacts(List<String> expression) {
        List<BackendFact> facts = new ArrayList<>();
        int index = 0;
        for (String token : expression) {
            index++;
            for (int step = 0; step <= expression.size(); ++step) {
                String name = getName(step, index);
                facts.add(new BackendFact(name, "rdf:type", "owl:NamedIndividual"));
                facts.add(new BackendFact("owl:NamedIndividual", name, "index", "xsd:int", String.valueOf(index)));
                facts.add(new BackendFact("owl:NamedIndividual", name, "step", "xsd:int", String.valueOf(step)));
            }
            facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "text", "xsd:string", token));
            facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "complex_beginning", "xsd:boolean", Boolean.toString(token.equals("(") || token.equals("[") || token.equals("?"))));
            facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "complex_ending", "xsd:boolean", Boolean.toString(token.equals(")") || token.equals("]") || token.equals(":"))));
        }
        facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "last", "xsd:boolean", "true"));
        return facts;
    }
'''

def write_expression(onto, expression: list):
    with onto:
        index = 0;
        for token in expression:
            # index++;
            index += 1
            for step in range(len(expression) + 1):
                name = getName(step, index);
                name = uniqualize_iri(onto, name)
                # facts.add(new BackendFact(name, "rdf:type", "owl:NamedIndividual"));
                obj = Thing(name)
                
                # facts.add(new BackendFact("owl:NamedIndividual", name, "index", "xsd:int", String.valueOf(index)));
                make_triple(obj, onto["index"], index)
                # facts.add(new BackendFact("owl:NamedIndividual", name, "step", "xsd:int", String.valueOf(step)));
                make_triple(obj, onto["step"], step)
            
                if step == 0:
                    # facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "text", "xsd:string", token));
                    make_triple(obj, onto["text"], token)
                    # facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "complex_beginning", "xsd:boolean", Boolean.toString(token.equals("(") || token.equals("[") || token.equals("?"))));
                    make_triple(obj, onto["complex_beginning"], bool(token in '([?'))
                    # facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "complex_ending", "xsd:boolean", Boolean.toString(token.equals(")") || token.equals("]") || token.equals(":"))));
                    make_triple(obj, onto["complex_ending"], bool(token in ')]:'))
                    last_obj_with_step_0 = obj
        
        # facts.add(new BackendFact("owl:NamedIndividual", getName(0, index), "last", "xsd:boolean", "true"));
        make_triple(last_obj_with_step_0, onto["last"], True)
    
    
def test_items_to_expressions(test_items: list) -> list:
    field = 'expression'
    exprs = []
    for d in test_items:
        if field in d and d[field]:
            data = d[field]
            
            # in_list = False
            for old_data in exprs:
                if data == old_data:
                    # print('filtered out:', data)
                    break
            else:
                exprs.append(data)
    
    return exprs


def make_expr_chain(expressions: 'list of lists', size=30, sep=',') -> list:
    expressions = list(sorted(expressions, key=lambda ops: len(ops)))
    L = len(expressions)
    lens = [len(e) + 1 for e in expressions]
    ## print('	', lens)
    L0 = lens[0]
    L9 = lens[-1] - 1
    last_i = L - 1
    joined_exprs = []
    def add(operands):
        if joined_exprs:
            joined_exprs.append(sep)
        ## print("	add:", len(operands))
        joined_exprs.extend(operands)
        
    while(len(joined_exprs) < size - len(expressions[last_i]) - L0):
        operands = expressions[last_i]
        add(operands)
        last_i = (last_i - 5 + L) % L
        
    # add last by length
    need_more = size - len(joined_exprs)
    dist2index = [(abs(need_more - L), i) for i, L in enumerate(lens)]
    i = min(dist2index)[1]
    ## print('	last add', len(expressions[i]))
    add(expressions[i])
    
    ### print("joined_exprs size:", len(joined_exprs), 'of', size)
    
    return joined_exprs
    

def iterate_over_expr_chains(expressions: 'iterable of lists', preferred_step=20, sep=',') -> iter:
    # expressions = list(sorted(expressions))
    for n in range(preferred_step, len(expressions), preferred_step):
        yield make_expr_chain(expressions, n, sep=sep)


def load_all_test_items() -> list:
    paths = [
        r"c:\D\Work\YDev\CompPr\CompPrehension\src\test\resources\has-operand-test-data.json",
        r"c:\D\Work\YDev\CompPr\CompPrehension\src\test\resources\simple-ontology-test-data.json",
        r"c:\D\Work\YDev\CompPr\CompPrehension\src\test\resources\before-test-data.json",
    ]
    test_items = []
    for path in paths:
        test_items += load_test_items_from_file(path)
    return test_items
        
    
def load_test_items_from_file(filepath) -> list:
    with open(filepath) as file:
        return json.load(file)


def prepare_ontology(expr_chain, inject_swrl=False, iri='http://penskoy.n/expressions'):
        onto = get_ontology(iri)
        clear_ontology(onto, keep_tbox=False)
        inject_laws(onto, omit_swrl=not inject_swrl)
        write_expression(onto, expr_chain)
        return onto


def main():
    data = test_items_to_expressions(load_all_test_items())
    # from pprint import pprint
    # pprint(data)
    
    for i in range(10, 23 + 1):
	    print(i, '->', len(make_expr_chain(data, i)))
    
    # for chain in iterate_over_expr_chains(data[:], 1):
    #     L = len(chain)
    #     print(L)
    #     if L < 36:
    #         print('\t'*8, ' '.join(chain))
    #     else:
    #         break

if __name__ == '__main__':
    main()
