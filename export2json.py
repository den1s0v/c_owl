# export2json.py
# write algorithm examples to JSON as CompPrehension questions

from itertools import count

from owlready2 import *
import ctrlstrct_run
import trace_gen.styling as styling
import trace_gen.syntax as syntax
from explanations import get_leaf_classes
from trace_gen.txt2algntr import find_by_key_in, find_by_keyval_in

from pprint import pprint

# USER_LANGUAGE = 'en'
USER_LANGUAGE = 'ru'
USER_SYNTAX = 'C'

QUESTION_NAME_PREFIX = ''  # default: change nothing
# QUESTION_NAME_PREFIX = '[human]'  # mark manual questions


if USER_LANGUAGE == 'ru':
    from jena.rusify import replace_in_text as translate_en2ru

# some global setup, once imported from somewhere else
syntax.set_allow_hidden_buttons(False)


# # for buttons "data-tooltip" to translate correctly
# syntax.set_force_button_tooltips_in_english(True)


def export_algtr2dict(alg_tr, onto):
    """onto: modifiable ontology containing schema (TBox)"""
    ctrlstrct_run.clear_ontology(onto, keep_tbox=True)
    ctrlstrct_run.algorithm_only_to_onto(alg_tr, onto)

    statementFacts = []
    answerObjects = []
    tags = []
    concepts = set()

    answer_ids = count()  # infinite generator

    # "owl:NamedIndividual"
    # "xsd:int"
    # "xsd:string"
    # "xsd:boolean"
    # objectType
    # object
    # verb
    # subjectType
    # subject

    ### q_text = alg_tr['algorithm']['text']

    alg_data = alg_tr['algorithm']
    # pprint(alg_data)

    algorithm_tags = syntax.algorithm_to_tags(alg_data, USER_LANGUAGE, USER_SYNTAX)

    if USER_LANGUAGE == 'ru':
        # patch tags containing English
        key = "data-tooltip"
        for d in find_by_key_in(key, algorithm_tags):
            contents = d[key]
            assert len(contents) == 1, contents
            # print(contents[0], end=' -> ')
            contents[0] = translate_en2ru(contents[0])
        # print(contents[0])

    # pprint(algorithm_tags)
    # will be patched in make_answerObject
    question_html = styling.to_html(algorithm_tags)

    # pprint(question_html)

    # algorithm structure
    for ind in onto.individuals():
        # write type(s)
        for class_ in ind.is_a:
            statementFacts.append({
                'subjectType': "owl:NamedIndividual",
                'subject': ind.name,
                'verb': "rdf:type",
                'objectType': "owl:Class",
                'object': class_.name,
            })
        # write relations
        for prop in ind.get_properties():
            for subj, value in prop.get_relations():
                if ind == subj:
                    # print(ind, "\t >>>> .%s >>>>\t %s" % (prop.python_name, value))
                    statementFacts.append({
                        'subjectType': "owl:NamedIndividual",
                        'subject': ind.name,
                        'verb': prop.name,
                        **({
                               'objectType': "owl:NamedIndividual",
                               'object': value.name,
                           }
                           if isinstance(value, Thing) or isinstance(value, entity.ThingClass) else
                           {
                               'objectType': type_of(value),
                               'object': value,
                           })
                    })

    # expr_values
    for ind in onto.expr.instances():
        expr_name = ind.stmt_name
        values_list = alg_data["expr_values"].get(expr_name, None)
        if values_list:
            #
            # print("values_list:", values_list)
            #
            statementFacts.append({
                'subjectType': "owl:NamedIndividual",
                'subject': expr_name,
                'verb': "not-for-reasoner:expr_values",
                'objectType': "List<boolean>",
                'object': ",".join([{True: '1', False: '0'}.get(v, str(v)) for v in values_list]),
            })

    def make_answerObject(hyperText, phase, id_, concept, answer_id=None):
        if answer_id is None:
            answer_id = next(answer_ids)
        # make simple trace line without "nth time" tail
        # strip first word (begin/end/execute) and add phase (started/finished/performed)
        view_phase = {
            'started': 'began',
            'finished': 'ended',
            'performed': 'evaluated' if concept == 'expr' else 'executed',
        }[phase]
        trace_act = hyperText.split(maxsplit=1)[1] + " " + view_phase
        # trace_act_hypertext = trace_act
        trace_act_hypertext = styling.to_html(styling.prepare_tags_for_line(trace_act))

        if USER_LANGUAGE == 'ru':
            # print(hyperText, end=' -> ')
            hyperText = translate_en2ru(hyperText)
            # print(hyperText)
            trace_act_hypertext = translate_en2ru(trace_act_hypertext)

        # patch ids in HTML
        old_info = phase + ":" + str(id_)
        new_info = old_info + ":" + trace_act_hypertext
        nonlocal question_html
        question_html = question_html.replace(old_info, str(answer_id))

        ### print("domainInfo length:", len(new_info))

        return {
            "answerId": answer_id,
            "hyperText": hyperText,
            "domainInfo": new_info,
            "isRightCol": False,
            "concept": concept,
            "responsesLeft": [],
            "responsesRight": []
        }

    # actions to answerObjects
    action_classes = [*onto.action.descendants()]

    ### print(action_classes)

    for ind in sorted(onto.action.instances(), key=lambda a: a.name):
        if isinstance(ind, onto.algorithm):  # or use `ind.is_a`
            continue  # no buttons for whole algorithm

        action_class = [cl for cl in ind.is_a if cl in action_classes]
        assert action_class, (ind, ind.is_a, alg_tr)
        action_class = next(iter(get_leaf_classes(action_class)))  # must exist
        # print('action_classes for', ind, ':', [*ind.is_a])
        # print('action_classes for', ind, ':', action_class)
        concepts.add(action_class.name)
        # find (first) dict with `id`
        for obj_dict in find_by_keyval_in("id", ind.id, alg_data):
            break
        ### print(obj_dict)
        act_name = obj_dict["act_name"]
        if isinstance(act_name, dict):
            act_name = act_name["en"]  # "en" should not be changed here
        action_title = act_name
        # note: all one-click actions should be listed here! (TODO: add if introduced in future)
        if (onto.expr in ind.is_a or
                onto.stmt in ind.is_a or
                onto['return'] in ind.is_a or
                onto['break'] in ind.is_a or
                onto['continue'] in ind.is_a
        ):
            answerObjects.append(make_answerObject(
                ("execute" if onto.stmt in ind.is_a else "evaluate") + " " + action_title,
                "performed", ind.id, action_class.name,
            ))
        else:
            answerObjects.append(make_answerObject(
                ("begin") + " " + action_title,
                "started", ind.id, action_class.name,
            ))
            answerObjects.append(make_answerObject(
                ("end") + " " + action_title,
                "finished", ind.id, action_class.name,
            ))

    # show concepts
    print("\tconcepts:", concepts)

    # patch generated html ...
    question_html = question_html.replace("<i class=\"play small icon\"></i>",
                                          '<img src="https://icons.bootstrap-4.ru/assets/icons/play-fill.svg" alt="Play" width="22">')
    question_html = question_html.replace("<i class=\"stop small icon\"></i>",
                                          '<img src="https://icons.bootstrap-4.ru/assets/icons/stop-fill.svg" alt="Stop" width="20">')
    # data-toggle="tooltip" data-placement="top" title="Tooltip on top"
    question_html = question_html.replace("data-tooltip=", 'data-toggle="tooltip" title=')
    question_html = question_html.replace("data-position=\"top left\"", 'data-placement="top"')

    # # replace answer IDs with their positions among answerObjects
    # for i, answerObject in enumerate(answerObjects):
    #   pattern = "answer_" + answerObject["domainInfo"]
    #   new_str = "answer_" + str(i)
    #   question_html = question_html.replace(pattern, new_str)

    question_html += STYLE_HEAD
    concepts = sorted(concepts)

    ###
    mistakes = find_mistakes_for_task(concepts, alg_data)
    print("\tMistakes:", len(mistakes))
    # print(mistakes)

    return {
        "questionType": "ORDERING",
        "questionData": {
            "questionType": "ORDER",
            "questionDomainType": "OrderActs",
            "questionName": QUESTION_NAME_PREFIX + alg_tr["algorithm_name"],
            "questionText": question_html,
            "areAnswersRequireContext": False,
            "options": {
                "metadata": {},
            },
            "answerObjects": answerObjects,
            "statementFacts": statementFacts,
        },
        "concepts": [  # ???
            "trace",
            "mistake",
            *concepts,
        ],
        "negativeLaws": [
            *mistakes,
        ],
        "tags": [  # ????
            "C++",
            # *concepts,
            # "basics",
            # "operators",
            # "order",
            # "evaluation"
        ],
        "metadata": {},
        ###>
        # "_alg_name": alg_tr["algorithm_name"],
        ###<
    }


def type_of(literal):
    if isinstance(literal, bool):
        return "xsd:boolean"
    if isinstance(literal, str):
        return "xsd:string"
    # "xsd:int"
    return "xsd:" + str(type(literal).__name__)


_MISTAKES_MAP = None


def find_mistakes_for_task(concepts, alg_data=None):
    global _MISTAKES_MAP
    if not _MISTAKES_MAP:
        _MISTAKES_MAP = read_mistakes_map()
    concepts = [*concepts, *_analyze_sequences_length(alg_data), *_analyze_alternatives(alg_data)]
    mistakes = []
    for name, mapping in _MISTAKES_MAP.items():
        price = 0
        for feature, cost in mapping.items():
            if _match_against_features(feature, concepts):
                price += cost
        if price >= 1:
            mistakes.append(name)
    pass
    return mistakes


def _analyze_sequences_length(alg_data) -> tuple('of features'):
    nontrivial_sequence_exists = False
    for d in find_by_keyval_in("type", "sequence", alg_data):
        if len(d["body"]) > 1:
            nontrivial_sequence_exists = True
            break
    return () if nontrivial_sequence_exists else ('seq-of-1-max',)


def _analyze_alternatives(alg_data) -> tuple('of features'):
    if_without_else_exists = False
    for d in find_by_keyval_in("type", "alternative", alg_data):  # "type": "alternative"
        if 'else' not in (b["type"] for b in d["branches"]):
            if_without_else_exists = True
            break
    return ('!else',) if if_without_else_exists else ()


def _match_against_features(key: str, features: list) -> bool:
    if key in features:
        return True
    if " & " in key:
        keys = key.split(" & ")
        return all(_match_against_features(k, features) for k in keys)
    if key.startswith("*"):
        key = key.lstrip("*")
        for f in features:
            if f.endswith(key):
                return True
    if key.startswith("!"):
        key = key.lstrip("!")
        return key not in features
    ### print("  *** Unknown feature key:", key)
    return False


def read_mistakes_map():
    S = '\t'  # separator
    mistakes_mapping = {}
    import os, os.path
    _dir_path = os.path.dirname(os.path.realpath(__file__))  # dir of current .py file
    filepath = os.path.join(_dir_path, 'jena/mistakes-map.txt')
    with open(filepath) as f:
        for i, line in enumerate(f.readlines()):
            if i == 0: continue
            if i == 1:
                # read useful header
                assert line.startswith(S), line
                features = line.strip().strip(S).split(S)
                continue
            # read mistake lines (table body)
            line = line.strip().strip(S)
            name, *cells = line.strip(S).split(S)
            mapping = {f: float(c.strip()) for f, c in zip(features, cells) if c.strip() and c != "-"}
            if mapping:  # is not empty
                mistakes_mapping[name] = mapping

    return mistakes_mapping


STYLE_HEAD = '''<style type="text/css" media="screen">
    .comp-ph-question-text {
      font-family: courier; font-size: 10pt;
    }
    span.string { color: #555; font-style: italic }
    span.atom { color: #f08; font-style: italic; font-weight: bold; }
    span.comment { color: #262; font-style: italic; line-height: 1em; }
    span.meta { color: #555; font-style: italic; line-height: 1em; }
    span.variable { color: #700; text-decoration: underline; }
    span.variable-2 { color: #b11; }
    span.struct { color: #07c; font-weight: bold; }
    span.number { color: #f00; font-weight: bold; }
    span.program { color: #f70; font-weight: bold; }
    span.function { color: #707; font-weight: bold; }
    span.action { color: #077; font-weight: bold; }
    span.qualifier { color: #555; }
    span.keyword { color: #00a; font-weight: bold; }
    span.builtin { color: #30a; }
    span.link { color: #762; }

    span.warning { background-color: #ff9; }
    span.error { background-color: #fdd; }
    span.button { background-color: #add; }
    span.alg_button { color: #111; cursor: pointer; }

</style>
'''


def main():
    # debug it!
    print(find_mistakes_for_task(["if", "else"]))


if __name__ == '__main__':
    main()
