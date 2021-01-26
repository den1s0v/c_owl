# rule_converter.py

import re


import ctrlstrct_swrl


### PROLOG ###

RE_q2upper = re.compile(r'\?([\w\d]+)', flags=re.I)
def q2upper_replace(m):
    s = m[1].upper()
    if s.startswith('_'):
        s = 'Tmp' + s
    return s

def convert_varnames(s):
    return RE_q2upper.sub(q2upper_replace, s)
    
    
RE_predicate = re.compile(r'([\w\d]+)\(((?:[^)]|"\)|\)")+)\)')  # 1: name, 2: args in braces

def lower_first_char(s):
    return f"{s[0].lower()}{s[1:]}" if s else s

def getting_datatype_property(varname):
    #     ^^(IB,_)
    return f'^^({varname},_)'

RE_DatatypeProp = re.compile(r'id|\w*index|exec_time|\w*iteration_n|text_line|step|text|precedence')

def using_boolean_literal(literal):
    if literal in ('true', 'false'):
        return f'"{literal}"^^xsd:boolean'
    return literal
        
def getting_property(propname, varname):
    if RE_DatatypeProp.match(propname):
        return getting_datatype_property(varname)
    else:
        return (varname)


def predicate2lowerfirst_replace(pred_match):
    name, args_str = pred_match[1], pred_match[2]
    args = [s.strip() for s in args_str.split(", ")]
    if len(args) == 2:
        args[1] = getting_property(name, args[1])
        args_str = ", ".join(args)
    return f"{lower_first_char(name)}({args_str})"


def convert_predicate_calls_prolog(s):
    return RE_predicate.sub(predicate2lowerfirst_replace, s)
    

IRI_type = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
IRI_prefix = 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#'

# rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#index', IB) ,
# rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#SequenceBegin') ,

def convert_rulehead(s):
    body, head = list(s.split(" -> "))
    body = body.rstrip(' \t\n,')
    new_head = []
    head_predicates = RE_predicate.finditer(head)
    for pred_match in head_predicates:
        # new_head.append(f"% -> {pred_match[0].strip()}")
        name, args_str = pred_match[1], pred_match[2]
        args = [s.strip() for s in args_str.split(",")]
        if len(args) == 2:
            args[1] = using_boolean_literal(args[1])
            prolog_call = f"rdf_assert({args[0]}, '{IRI_prefix}{name}', {args[1]})"
        elif len(args) == 1:
            prolog_call = f"rdf_assert({args[0]}, '{IRI_type}', '{IRI_prefix}{name}')"
        else:
            raise pred_match
        new_head.append(prolog_call)
    rule = "\t" + (',\n\t'.join([body, *new_head, 'fail.'])) + '\n'
    return rule

    
def swrl2prolog(swrl, name=None):
    rule = convert_predicate_calls_prolog(convert_rulehead(convert_varnames(swrl))).replace('# ', '% ')
    if not name:
        title = '% Rule\n'
    else:
        title = f'% Rule: {name}\n'
    debug_print_rulename = f"writeln('\t{name},')," if 0 else ""
    return f'''{title}swrl_rule() :- {debug_print_rulename}\n{rule}'''


def to_prolog(rules, out_path='from_swrl.pl', iri_prefix=None):
    if iri_prefix:
        set_IRI_prefix(iri_prefix)
        
    with open(out_path, 'w') as file:
        for rule in rules:
            # swrl = rule._original_swrl
            swrl = rule.swrl
            prolog = swrl2prolog(swrl, f'{rule.name} [{" & ".join(rule.tags)}]')
            file.write('\n')
            file.write(prolog)


def set_IRI_prefix(iri_prefix):
    global IRI_prefix
    IRI_prefix = iri_prefix


### JENA ###
        
LOCAL_PREFIX = "my:"
RDF_TYPE = "rdf:type"
RE_SWRL_builtins = re.compile(r'lessThan|greaterThan|notEqual|equal|add|matches')
RE_boolean_value = re.compile(r'^(?:true|false)$')
# varnames conflicting with classnames
RE_conflicting_varnames = re.compile(r'\b(?:loop|cond|body)\b')


def convert_builtin(name: str, args: list):
    if name == 'add':
        # change the order (result is first in SWRL but last in Jena)
        args = [args[1], args[2], args[0]]
        name = 'sum'
    if name == 'matches':
        name = 'regex'
    args_str = ", ".join(args)
    return f"{name}({args_str})"

def convert_argument(plain: str):
    plain = fix_conflicting_variable(plain)
    plain = convert_literal(plain)
    return plain
    
def convert_literal(plain: str):
    if RE_boolean_value.match(plain):
        # "true"^^xsd:boolean
        return f'"{plain}"^^xsd:boolean'
    return plain

def fix_conflicting_variable(plain: str):
    if RE_conflicting_varnames.search(plain):
        # add a couple of underscores
        return plain + '__'
    return plain
    

def predicate2triple_replace(pred_match):
    name, args_str = pred_match[1], pred_match[2]
    args = [convert_argument(s.strip()) for s in args_str.split(", ")]
    if len(args) == 1:
        # type checking
        return f"({args[0]} {RDF_TYPE} {LOCAL_PREFIX}{name})"
    
    # args[1:] = map(convert_argument, args[1:])
    if RE_SWRL_builtins.match(name):
        return convert_builtin(name, args)
    else:
        assert len(args) == 2, f"{len(args)}, in {name}"
        # args[1] = args[1].replace('"', "'")  # " -> ' (Jena accepts single-quoted strings by docs, both types actually)
        return f"({args[0]} {LOCAL_PREFIX}{name} {args[1]})"

def convert_predicate_calls_jena(s):
    return RE_predicate.sub(predicate2triple_replace, s)
    
    
def swrl2jena(swrl, name=None):
    rule = convert_predicate_calls_jena(swrl)
    if not name:
        title = '# Rule'
    else:
        title = f'# Rule: {name}'
    return f'''{title}\n[{rule}]'''
    

def to_jena(rules, out_path='from_swrl.jena_rules'):
    with open(out_path, 'w') as file:
        for rule in rules:
            # swrl = rule._original_swrl
            swrl = rule.swrl
            jena = swrl2jena(swrl, f'{rule.name} [{" & ".join(rule.tags)}]')
            file.write('\n' * 2)
            file.write(jena)


### SPARQL ###

RULE_END_PUNCT = " . "
RE_predicate_with_comma = re.compile(r'([\w\d]+)\(((?:[^)]|"\)|\)")+)\)\s*,?\s*')  # 1: name, 2: args in braces

def convert_builtin2sparql(name: str, args: list):
    if name == 'add':
        # BIND(?ia + 1 as ?ib)
        return f"BIND( {args[1]} + {args[2]} as {args[0]} )"
    if name == 'matches':
        # FILTER (regex(?var, 'regex-patern'))
        return f"FILTER (regex ( {args[0]}, {args[1]} ))"
    op = {
        'lessThan' : '<',
        'greaterThan' : '>',
        'notEqual' : '!=',
        'equal' : '=',
         }.get(name, "==!No op!==")
    return f"FILTER ( {args[0]} {op} {args[1]} )"

def predicate2sparql_triple_replace(pred_match):
    name, args_str = pred_match[1], pred_match[2]
    args = [s.strip() for s in args_str.split(", ")]
    if len(args) == 1:
        # type checking
        return f"{args[0]} {RDF_TYPE} {LOCAL_PREFIX}{name}" + RULE_END_PUNCT
    if RE_SWRL_builtins.match(name):
        return convert_builtin2sparql(name, args) + RULE_END_PUNCT
    else:
        assert len(args) == 2, len(args)
        return f"{args[0]} {LOCAL_PREFIX}{name} {args[1]}" + RULE_END_PUNCT

def convert_predicate_calls_sparql(s):
    return RE_predicate_with_comma.sub(predicate2sparql_triple_replace, s)


def swrl2sparql(swrl, name=None):
    s = convert_predicate_calls_sparql(swrl)
    body, head = list(s.split(" -> "))
    if not name:
        title = '# Rule'
    else:
        title = f'# Rule: {name}'
    return f'''{title}
INSERT
  {{ {head.strip()} }}
WHERE
  {{
    {body.strip()}
  }}'''


def to_sparql(rules, out_path='sparql_from_swrl.ru', heading_path='sparql/rdfs4core.ru', base_iri=None):
    with open(out_path, 'w') as file:
        with open(heading_path) as heading_file:
            heading_text = heading_file.read()
            
            if base_iri:
                # ensure it ends with '#'
                base_iri = base_iri.rstrip('#') + '#'
                # replace PREFIX my:  <IRI>
                heading_text = re.sub(r'PREFIX my: .+?\n', 'PREFIX my:  <%s>\n' % base_iri, heading_text)
                
            file.write(heading_text)
        for rule in rules:
            # swrl = rule._original_swrl
            swrl = rule.swrl
            sparql = swrl2sparql(swrl, f'{rule.name} [{" & ".join(rule.tags)}]')
            file.write(sparql)
            file.write(' ;\n\n')  # ';' is a query separator




### ASP: Clingo, DLV ###

def convert_builtin_asp(name: str, args: list):
    if name == 'add':
        # Note the order (result is first in SWRL)
        # return f'{args[1]} + {args[2]} = {args[0]}'
        return f'{args[0]} = {args[1]} + {args[2]}'
    # if name == 'matches':
    #     name = 'regex'
    op = {
        'lessThan' : '<',
        'greaterThan' : '>',
        'notEqual' : '!=',
        'equal' : '=',
         }.get(name, "==!No op!==")
    return f"{args[0]} {op} {args[1]}"


def predicate2lowerfirst_replace_asp(pred_match):
    name, args_str = pred_match[1], pred_match[2]
    name = lower_first_char(name)
    args = [s.strip() for s in args_str.split(", ")]
    if RE_SWRL_builtins.match(name):
        return convert_builtin_asp(name, args)
    if len(args) == 2:
        args = (args[0], name, args[1])
    elif len(args) == 1:
        args = (args[0], 'type', name)  # use 'type' in place of 'rdf:type'
    args_str = ", ".join(args)
    return f"t({args_str})"


def convert_predicate_calls_clingo(s):
    return RE_predicate.sub(predicate2lowerfirst_replace_asp, s)
    

def convert_rulehead(s):
    body, head = list(s.split(" -> "))
    body = body.rstrip(' \t\n,')
    new_rules = []
    head_predicates = RE_predicate.finditer(head)
    # Размножаем правило, оставляя в head по одному утверждению за раз
    for pred in head_predicates:
        rule = ("\t" + pred[0] + ':-' + body + '.\n')
        new_rules.append(rule)
    return ''.join(new_rules)

    
def swrl2clingo(swrl, name=None):
    rule = convert_predicate_calls_clingo(convert_rulehead(convert_varnames(swrl))).replace('# ', '% ')
    if not name:
        title = '% Rule\n'
    else:
        title = f'% Rule: {name}\n'
    debug_print_rulename = f"writeln('\t{name},')," if 0 else ""
    return f'''{title}{rule}'''


def to_clingo(rules, out_path='from_swrl.asp', iri_prefix=None):
    if iri_prefix:
        set_IRI_prefix(iri_prefix)
        
    with open(out_path, 'w') as file:
        for rule in rules:
            # swrl = rule._original_swrl
            swrl = rule.swrl
            clingo = swrl2clingo(swrl, f'{rule.name} [{" & ".join(sorted(rule.tags))}]')
            file.write('\n')
            file.write(clingo)



def main():
    RULES = ctrlstrct_swrl.RULES
    # to_prolog(RULES)
    # to_jena(RULES)
    # to_sparql(RULES)
    to_clingo(RULES)


if __name__ == '__main__':
    main()

