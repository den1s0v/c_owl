# rule_converter.py

import re


import ctrlstrct_swrl


RE_q2upper = re.compile(r'\?([\w\d]+)', flags=re.I)
def q2upper_replace(m):
    s = m[1].upper()
    if s.startswith('_'):
        s = 'Tmp' + s
    return s

def convert_varnames(s):
    return RE_q2upper.sub(q2upper_replace, s)
    
    
RE_predicate = re.compile(r'([\w\d]+)\(([^)]+?)\)')  # 1: name, 2: args in braces

def lower_first_char(s):
    return f"{s[0].lower()}{s[1:]}" if s else s

def getting_datatype_property(varname):
    #     ^^(IB,_)
    return f'^^({varname},_)'

RE_DatatypeProp = re.compile(r'id|\w*index|exec_time|\w*iteration_n|text_line')

def getting_property(propname, varname):
    if RE_DatatypeProp.match(propname):
        return getting_datatype_property(varname)
    else:
        return varname


def predicate2lowerfirst_replace(pred_match):
    name, args_str = pred_match[1], pred_match[2]
    args = [s.strip() for s in args_str.split(",")]
    if len(args) == 2:
        args[1] = getting_property(name, args[1])
        args_str = ", ".join(args)
    return f"{lower_first_char(name)}({args_str})"

def convert_predicate_calls(s):
    return RE_predicate.sub(predicate2lowerfirst_replace, s)
    


IRI_type = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
IRI_prefix = 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#'

# rdf_assert(B, 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#index', IB) ,
# rdf_assert(B, 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type', 'http://vstu.ru/poas/ctrl_structs_2020-05_v1#SequenceBegin') ,

def convert_rulehead(s):
    body, head = list(s.split("->"))
    body = body.rstrip(' \t\n,')
    new_head = []
    head_predicates = RE_predicate.finditer(head)
    for pred_match in head_predicates:
        new_head.append(f"% -> {pred_match[0].strip()}")
        name, args_str = pred_match[1], pred_match[2]
        args = [s.strip() for s in args_str.split(",")]
        if len(args) == 2:
            prolog_call = f"rdf_assert({args[0]}, '{IRI_prefix}{name}', {args[1]})"
        elif len(args) == 1:
            prolog_call = f"rdf_assert({args[0]}, '{IRI_type}', '{IRI_prefix}{name}')"
        else:
            raise pred_match
        new_head.append(prolog_call)
    rule = "\t" + (',\n\t'.join([body, *new_head, 'fail.'])) + '\n'
    return rule

    
def swrl2prolog(swrl, name=None):
    rule = convert_predicate_calls(convert_rulehead(convert_varnames(swrl))).replace('# ', '% ')
    if not name:
        title = '% Rule\n'
    else:
        title = f'% Rule: {name}\n'
    debug_print_rulename = f"writeln('\t{name},')," if 0 else ""
    return f'''{title}swrl_rule() :- {debug_print_rulename}\n{rule}'''



def to_prolog(rules, out_path='from_swrl.pl'):
	with open(out_path, 'w') as file:
		for rule in rules:
			# swrl = rule._original_swrl
			swrl = rule.swrl
			prolog = swrl2prolog(swrl, f'{rule.name} [{" & ".join(rule.tags)}]')
			file.write('\n')
			file.write(prolog)


def main():
	RULES = ctrlstrct_swrl.RULES
	to_prolog(RULES)


if __name__ == '__main__':
	main()

