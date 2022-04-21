# ctrlstrct_run.py


""" Импорт алгоритмов и трасс из текста (из файлов в handcrafted_traces/*),
наполнение ими чистой онтологии,
добавление SWRL-правил, определённых в ctrlstrct_swrl.py (используя import), сохранение исходной онтологии в файл,
запуск ризонинга (опционально).
"""


import io

# from pprint import pprint

# from owlready2 import *
from onto_helpers import *

from transliterate import slugify
from trace_gen.txt2algntr import get_ith_expr_value, find_by_key_in, find_by_keyval_in
from explanations import format_explanation, get_leaf_classes
from external_run import timer, run_swiprolog_reasoning, run_jena_reasoning, invoke_jena_reasoning_service, measure_stats_for_pellet_running, measure_stats_for_clingo_running, measure_stats_for_dlv_running, get_process_run_stats

from common_helpers import Uniqualizer, delete_file

onto_path.append(".")

# ONTOLOGY_maxID = 1
ONTOLOGY_IRI = 'http://vstu.ru/poas/code'

def prepare_name(s):
    """Transliterate given word is needed"""
    return slugify(s, "ru") or s


# наладим связи между элементами алгоритма
def link_objects(onto, iri_subj : str, prop_name : str, iri_obj : str, prop_superclasses=(Thing >> Thing, )):
    """Make a relation between two individuals that must exist in the ontology. The property, however, is created if does not exist (the `prop_superclasses` are applied to the new property)."""
    prop = onto[prop_name]
    if not prop:
        with onto:
            # новое свойство по заданному имени
            prop = types.new_class(prop_name, prop_superclasses)
    # связываем объекты свойством
    make_triple(onto[iri_subj], prop, onto[iri_obj])

def uniqualize_iri(onto, iri):
    """uniqualize individual's name"""
    n = 2; orig_iri = iri
    while onto[iri]:  # пока есть объект с таким именем
        # модифицировать имя
        iri = orig_iri + ("_%d" % n); n += 1
    # print(iri)
    return iri


def uniqualize_id(onto, id_:int):
    """uniqualize individual's id"""
    prop = onto.id
    existing = [o for s, o in prop.get_relations()]
    while id_ in existing:  # пока есть объект с таким ID
        # модифицировать ID
        id_ += 100
    return id_


class TraceTester():
    def __init__(self, trace_data):
        """trace_data: dict like
         {
            "trace_name"    : str,
            "algorithm_name": str,
            "trace"         : list,
            "algorithm"     : dict,
            "header_boolean_chain" : list of bool - chain of conditions results
         }
        """
        self.data = trace_data
        # pprint(trace_data)
        # pprint(trace_data["trace"])
        # pprint(trace_data["algorithm"])
        # exit()

        # индекс всех объектов АЛГОРИТМА для быстрого поиска по id
        self.id2obj = self.data["algorithm"].get("id2obj", {})

        self.initial_repair_data()

        self.act_iris = []

        self._maxID = 1


    def initial_repair_data(self):
        '''patch data if it is not connected properly but is replicated instead (ex. after JSON serialization)'''

        # repair dicts' "id" values that are str, not int
        k = 'id'
        for d in find_by_key_in(k, self.data):
            if isinstance(d[k], str):
                d[k] = int(d[k])
        # repair dicts keys that are str, not int
        for k in list(self.id2obj.keys()):
            if isinstance(k, str):
                self.id2obj[int(k)] = self.id2obj[k]
                del self.id2obj[k]

        data = self.data["algorithm"]  # data to repair
        roots = data["global_code"], data["functions"]  # where actual data to be stored

        # referers = data["entry_point"], data["id2obj"]  # these should only refer to some nodes within roots.

        k = 'id'
        for d in find_by_keyval_in(k, data["entry_point"][k], roots):
            data["entry_point"] = d  # reassign the approriate node from roots (global_code or main function)
            break

        for ID in list(self.id2obj.keys()):
            for d in find_by_keyval_in(k, ID, roots):
                self.id2obj[ID] = d  # reassign the approriate node from roots
                break


    def newID(self, what=None):
        while True:
            self._maxID += 1
            if self._maxID not in self.id2obj:
                break
        return self._maxID

    def alg_entry(self):
        if "entry_point" in self.data["algorithm"]:
            alg_node = self.data["algorithm"]["entry_point"]
        else:
            raise "Cannot resolve 'entry_point' from algorithm's keys: " + str(list(self.data["algorithm"].keys()))
        return alg_node

    def make_correct_trace(self, noop=False):

        self.data["correct_trace"] = []
        self.expr_id2values = {}

        if noop:
            # !!!
            return

        def _gen(states_str):
            for ch in states_str:
                yield bool(int(ch))
            while 1:
                yield None

        self.last_cond_tuple = (-1, False)

        self._maxID = max(self._maxID, max(map(int, self.id2obj.keys())) + 10)

        # decide where to read expr values from
        self.values_source = None
        if self.data["header_boolean_chain"]:
            # source №1: the boolean chain attached to the trace
            self.values_source = "boolean_chain"
            self.condition_value_generator = _gen(self.data["header_boolean_chain"])
        elif self.data["algorithm"]["expr_values"]:
            # source №2: the values defined beside algorithm lines (this is used for 1-1 case when no boolean chain specified)
            self.values_source = "algorithm"
        else:
            # source №3: the values defined beside trace lines
            #  (this is less preffered as the trace may contain errors)
            self.values_source = "trace"

        # print(f'Trace {self.data["trace_name"]}: values_source detected:', self.values_source)

        def next_cond_value(expr_name=None, executes_id=None, n=None, default=False):

            i, _ = self.last_cond_tuple
            v = None

            if self.values_source == "boolean_chain":
                v = next(self.condition_value_generator)
            else:
                assert n is not None, str(n)

                if self.values_source == "algorithm":
                    assert expr_name is not None, str(expr_name)
                    expr_values_dict = self.data["algorithm"]["expr_values"]
                    if expr_name in expr_values_dict:
                        expr_values = expr_values_dict[expr_name]
                    else:
                        raise ValueError(f"Algorithm processing error: No values of condition expression '{expr_name}' are provided.\nConsider example of how to specify values [true, true, false] for this condition as if it belongs to a loop:\n <pre>while {expr_name} -> 110  // loop_name</pre>")
                    v = get_ith_expr_value(expr_values, i=n - 1)

                if self.values_source == "trace":
                    # find act with appropriate name and exec_time (phase is defaulted to "finished" as values are attached to these only)
                    assert expr_name is not None or executes_id is not None, str((expr_name, executes_id))
                    # print(self.data["trace"])
                    acts = [
                        act for act in
                        find_by_keyval_in("n", str(n), self.data["trace"])
                        # act["n"] == n and
                        if act["phase"] in ("finished", 'performed')
                            and (
                                # act["name"] == expr_name or
                                act["executes"] == executes_id
                            )
                        ]
                    if acts:
                        assert len(acts) == 1, "Expected 1 act to be found, but got:\n " + str(acts)
                        act = acts[0]
                        v = act.get("value", None)
                    else:
                        print("Warning: cannot find student_act: %s" % (dict(expr_name=expr_name, executes_id=executes_id, n=n)))

            if v is None:
                v = default
                print("next_cond_value(): defaulting to", default)
            # v = bool(v)
            self.last_cond_tuple = (i+1, v)
            # print(f"next_cond_value: {v}")
            return v

        # long recursive function
        def make_correct_trace_for_alg_node(node):
            # copy reference
            result = self.data["correct_trace"]

            if node["type"] in {"func"}:

                phase = "started"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["body"]["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })

                for body_node in node["body"]["body"]:
                    make_correct_trace_for_alg_node(body_node)

                phase = "finished"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["body"]["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })

            if node["type"] in {"sequence", "else"}:

                # do not wrap 'global_code'
                if node["name"] != 'global_code':
                    phase = "started"
                    ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                    result.append({
                          "id": self.newID(),
                          "name": node["name"],
                          "executes": node["id"],
                          "phase": phase,
                          "n": ith,
                          # "text_line": None,
                          # "comment": None,
                    })

                for body_node in node["body"]:
                    make_correct_trace_for_alg_node(body_node)

                # do not wrap 'global_code'
                if node["name"] != 'global_code':
                    phase = "finished"
                    ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                    result.append({
                          "id": self.newID(),
                          "name": node["name"],
                          "executes": node["id"],
                          "phase": phase,
                          "n": ith,
                          # "text_line": None,
                          # "comment": None,
                    })

            if node["type"] in {"alternative"}:

                phase = "started"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })

                for branch in node["branches"]:
                    make_correct_trace_for_alg_node(branch)
                    if self.last_cond_tuple[1] == True:
                        break

                phase = "finished"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })

            if node["type"] in {"if", "else-if"}:
                make_correct_trace_for_alg_node(node["cond"])
                _,cond_v = self.last_cond_tuple
                if cond_v:
                    phase = "started"
                    ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                    result.append({
                          "id": self.newID(),
                          "name": node["name"],
                          "executes": node["id"],
                          "phase": phase,
                          "n": ith,
                          # "text_line": None,
                          # "comment": None,
                    })

                    for body_node in node["body"]:
                        make_correct_trace_for_alg_node(body_node)

                    phase = "finished"
                    ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                    result.append({
                          "id": self.newID(),
                          "name": node["name"],
                          "executes": node["id"],
                          "phase": phase,
                          "n": ith,
                          # "text_line": None,
                          # "comment": None,
                    })


            if node["type"] in {"expr"}:
                phase = "performed"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                value = next_cond_value(node["name"], node["id"], ith)
                self.expr_id2values[node["id"]] = self.expr_id2values.get(node["id"], []) + [value]
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "value": value,
                      "executes": node["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })

            if node["type"] in {"stmt", "break", "continue", "return"}:
                phase = "performed"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })
                if node["type"] in {"break", "continue", "return"}:
                    return  # just stupidly stop current sequence

            if node["type"] in {"while_loop", "do_while_loop", "do_until_loop", "for_loop", "foreach_loop", "infinite_loop", }:

                phase = "started"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })

                inverse_cond = node["type"] == "do_until_loop"
                stop_cond_value = True == inverse_cond

                def _loop_context():  # wrapper for return
                    # loop begin
                    if node["type"] in {"for_loop", "foreach_loop"}:
                        make_correct_trace_for_alg_node(node["init"])

                    if node["type"] in {"while_loop", "for_loop", "foreach_loop"}:
                        make_correct_trace_for_alg_node(node["cond"])
                        if self.last_cond_tuple[1] == stop_cond_value:
                            return

                    # loop cycle

                    while(True):

                        if node["type"] in {"foreach_loop"}:
                            make_correct_trace_for_alg_node(node["update"])

                        # итерация цикла!
                        make_correct_trace_for_alg_node(node["body"])
                        # как обрабатывать break из цикла?

                        if node["type"] in {"for_loop"}:
                            make_correct_trace_for_alg_node(node["update"])

                        if node["type"] not in {"infinite_loop"}:
                            make_correct_trace_for_alg_node(node["cond"])
                            if self.last_cond_tuple[1] == stop_cond_value:
                                return


                _loop_context()  # make a loop

                phase = "finished"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
                result.append({
                      "id": self.newID(),
                      "name": node["name"],
                      "executes": node["id"],
                      "phase": phase,
                      "n": ith,
                      # "text_line": None,
                      # "comment": None,
                })


        alg_node = self.alg_entry()

        name = "программа"
        phase = "started"
        self.data["correct_trace"].append({
              "id": self.newID(),
              "name": name,
              "executes": alg_node["id"],
              "phase": phase,
              "n": 1,
              # "text_line": None,
              # "comment": None,
        })
        make_correct_trace_for_alg_node(alg_node)
        phase = "finished"
        self.data["correct_trace"].append({
              "id": self.newID(),
              "name": name,
              "executes": alg_node["id"],
              "phase": phase,
              "n": 1,
              # "text_line": None,
              # "comment": None,
        })

        # print(self.data["trace"])
        # print()
        # print(self.data["correct_trace"])
        # exit()

    def inject_to_ontology(self, onto):

        self.inject_algorithm_to_ontology(onto)

        self.make_correct_trace(noop=True)
        self.prepare_act_candidates(onto)
        self.inject_trace_to_ontology(onto, self.data["trace"], (), "student_next")
        # self.inject_trace_to_ontology(onto, self.data["correct_trace"], ("correct_act",), "correct_next")
        # self.merge_traces(onto, self.data["student_act_iri_list"], self.data["correct_act_iri_list"])

    def prepare_id2obj(self):
        alg_objects = list(find_by_type(self.data["algorithm"]))
        if not self.id2obj:
            # fill it once
            for d in alg_objects:
                if "id" in d:
                    self.id2obj[ d["id"] ] = d
            # store to original algorithm dict
            self.data["algorithm"]["id2obj"] = self.id2obj


    def inject_algorithm_to_ontology(self, onto):
        "Prepares self.id2obj and writes algorithm to ontology if it isn't there."

        if "entry_point" not in self.data["algorithm"]:
            alg_node = self.data["algorithm"]["global_code"]
            # polyfill entry_point to be global_code
            self.data["algorithm"]["entry_point"] = alg_node

        self.prepare_id2obj()

        with onto:
            if onto.algorithm_name and self.data["algorithm_name"] in [s for _,s in onto.algorithm_name.get_relations()]:
                # do nothing as the algorithm is in the ontology
                return

            alg_objects = list(find_by_type(self.data["algorithm"]))

            written_ids = set()

            # make algorithm classes and individuals
            for d in alg_objects:
                if "id" not in d:
                    continue
                id_ = d.get("id")

                # (once more) protection from objects cloned via JSON serialization
                if id_ in written_ids:
                    continue
                else:
                    written_ids.add(id_)

                type_ = d.get("type")
                name  = d.get("name", "")

                assert type_, "Error: No 'type' in agrorithm object: " + str(d)

                id_        = int(id_)
                clean_name = prepare_name(name)

                class_ = onto[type_]
                if not class_:
                    # make a new class in the ontology
                    class_ = types.new_class(type_, (Thing, ))

                # формируем имя экземпляра в онтологии
                iri = "{}_{}".format(id_, clean_name)

                iri = uniqualize_iri(onto, iri)

                # сохраняем назад в наш словарь (для привязки к актам трассы)
                d["iri"] = iri
                ### print('### saving iri back to dict:', iri)
                # создаём объект
                obj = class_(iri)
                # привязываем id
                make_triple(obj, onto.id, id_)
                # привязываем имя
                make_triple(obj, onto.stmt_name, name)

                # make special string link identifying algorithm
                if type_ == "algorithm":
                    prop = onto["algorithm_name"]
                    if not prop:
                        with onto:
                            # новое свойство по заданному имени
                            prop = types.new_class("algorithm_name", (Thing >> str, ))
                    make_triple(obj, prop, self.data["algorithm_name"])
                elif True:  # new experimental feature
                    # connect begin & end
                    class_ = onto.boundary
                    for prop_name in ("begin_of", "end_of"):
                        bound = class_(prop_name + "_" + iri)
                        make_triple(bound, onto[prop_name], obj)


            # link the instances: repeat the structure completely
            for d in alg_objects:
                if "id" not in d:
                    continue
                for k in d:  # ищем объекты среди полей словаря
                    v = d[k]
                    if isinstance(v, dict) and "id" in v and "iri" in v:
                        # connect all the properties of the instance
                        link_objects(onto, d["iri"], k, v["iri"], (Thing >> Thing, onto.parent_of,) )
                    elif isinstance(v, (list, set)):
                        # make an ordered linked_list for list, unorederd for set
                        # print("check out list", k, "...")
                        # сделаем список, если в нём нормальные "наши" объекты
                        subobject_iri_list = [subv["iri"] for subv in v  if isinstance(subv, dict) and "id" in subv and "iri" in subv]
                        if not subobject_iri_list:
                            continue

                        iri = d["iri"]

                        # всякий список (действий, веток, ...) должен быть оформлен как linked_list.
                        if k == "body" and isinstance(v, list):
                            # делаем объект последовательностью (нужно для тел циклов, веток, функций)
                            onto[iri].is_a.append( onto.linked_list )
                        # else:  # это нормально для других списков
                        #     print("Warning: key of sequence is '%s' (consider using 'body')" % k)


                        subelem__prop_name = k+"_item"
                        for i, subiri in enumerate(subobject_iri_list):
                            # главная связь
                            link_objects(onto, iri, subelem__prop_name, subiri, (Thing >> Thing, onto.parent_of,) )
                            if isinstance(v, list):  # for list only
                                # последовательность
                                if i >= 1:
                                    prev_iri = subobject_iri_list[i-1]
                                    link_objects(onto, prev_iri, "next", subiri)
                                # set the index of elem in the list
                                onto[subiri].item_index = i
                                # первый / последний
                                if i == 0:
                                    # mark as first elem of the list
                                    onto[subiri].is_a.append(onto.first_item)
                                if i == len(subobject_iri_list)-1:
                                    # mark as last act of the list
                                    onto[subiri].is_a.append(onto.last_item)


    def prepare_act_candidates(self, onto, extra_act_entries=0):
        """Create all possible acts for each statement.
        Maximum executon number will be exceeded by `extra_act_entries`.
        /* Resulting set of acts of size N will be repeated N times, each act to be possibly placed at each index of the trace, covering the set of all possible traces. */ """

        assert extra_act_entries == 0, f"extra_act_entries={extra_act_entries}"  # TODO: remove parameter (it is deprecated now)

        alg_id2max_exec_n = {st_id:0 for st_id in self.id2obj.keys()}  # executed stmt id to max exec_time of the act
        for act in self.data["correct_trace"]:
            executed_id = act["executes"]
            exec_n = act["n"]
            alg_id2max_exec_n[executed_id] = exec_n  # assume "n"s appear consequently in the trace

        # ensure that student's acts exist
        for act in self.data["trace"]:
            executed_id = act["executes"]
            exec_n = act.get("n", "1")
            alg_id2max_exec_n[executed_id] = max(
                            int(exec_n),  # assume "n"s appear consequently in the trace
                            int(alg_id2max_exec_n[executed_id]))

        entry_stmt_id = self.alg_entry()["id"]

        max_act_ID = 1000
        def set_id(act_obj):
            nonlocal max_act_ID
            max_act_ID += 1
            make_triple(act_obj, onto.id, max_act_ID)


        # make top-level act representing the trace ...
        iri = f'trace_{self.data["trace_name"]}'
        if self.data["header_boolean_chain"]:
            iri += f'_c{"".join(map(str, map(int, self.data["header_boolean_chain"])))}'

        iri = iri.replace(" ", "_").strip("_")

        iri = prepare_name(iri)
        iri = uniqualize_iri(onto, iri)
        trace_obj = onto.trace(iri)
        self.trace_obj = trace_obj  # remember for trace injection
        trace_obj.is_a.append(onto.correct_act)
        make_triple(trace_obj, onto.executes, onto[self.data["algorithm"]["iri"]])
        set_id(trace_obj)
        make_triple(trace_obj, onto.index, 0)
        make_triple(trace_obj, onto.student_index, 0)
        make_triple(trace_obj, onto.exec_time, 0)  # set to 0 so next is 1
        make_triple(trace_obj, onto.depth, 0)  # set to 0 so next is 1
        make_triple(trace_obj, onto.in_trace, trace_obj)  # each act belongs to trace


        # N = sum(alg_id2max_exec_n.values()) * 2  # as each stmt has begin & end!
        # print(F"N of layers and N acts on layer: {N}")
        for st_id, max_n in alg_id2max_exec_n.items():

            alg_elem = self.id2obj[st_id]
            if alg_elem["type"] in {"algorithm"}:
                continue

            # prepare data
            name = alg_elem.get("name", "unkn")
            clean_name  = prepare_name(name)

            mark2act_obj = {}  # executed stmt id to list of act iri's can be consequently used in trace

            # for index in range(1, N + 1):
            for exec_n in range(1, max_n + 1):

                    # make instances: act_begin, act_end
                    number_mark = "" if max_n <=1 else ("_n%02d" % exec_n)
                    iri_template = f"%s_{clean_name}{number_mark}"  # _i{index:02}

                    for mark, class_, boundary_prop in [("b", onto.act_begin, onto.begin_of), ("e", onto.act_end, onto.end_of)]:
                        iri = iri_template % mark
                        iri = uniqualize_iri(onto, iri)

                        obj = class_(iri)
                        # obj.is_a.append(class_X)

                        boundary = get_relation_subject(boundary_prop, onto[alg_elem["iri"]])
                        # print("boundary:", boundary)
                        make_triple(obj, onto.executes, boundary)

                        set_id(obj)
                        ### make_triple(obj, onto.index, index)
                        make_triple(obj, onto.exec_time, exec_n)
                        make_triple(obj, onto.in_trace, trace_obj)

                        # # connect "next_sibling"
                        # if exec_n == 1:
                        #   make_triple(trace_obj, onto.next_sibling, obj)
                        # else:
                        #   make_triple(mark2act_obj[mark], onto.next_sibling, obj)

                        # keep current value for next iteration
                        mark2act_obj[mark] = obj


                        # attach expr value: for act_end only!
                        if mark == "e" and alg_elem["type"] in ("expr",):
                            values = self.expr_id2values[st_id] if st_id in self.expr_id2values else []
                            # if len(values) <= exec_n:
                            if exec_n <= len(values):
                                value = values[exec_n - 1]
                            else:
                                value = False
                                print("attach expr value: defaulting to False...")
                            # print(obj, onto.expr_value, value)
                            make_triple(obj, onto.expr_value, value)

                        # # connect trace begin and 1st act with "next"
                        # if mark == "b" and st_id == entry_stmt_id and index == exec_n == 1:
                        #     obj.is_a.append(onto.correct_act)
                        #     # obj.is_a.append(onto.current_act)
                        #     make_triple(trace_obj, onto.next_act, obj)


    def inject_trace_to_ontology(self, onto, trace, act_classnames=("act",), next_propertyname=None):
        "Writes specified trace to ontology assigning properties to pre-created acts."

        additional_classes = [onto[nm] for nm in act_classnames]
        assert all(additional_classes), f"additional_classes={additional_classes}, {act_classnames}, {onto}"

        # make trace acts as individuals

        prop_class = onto[next_propertyname]

        def connect_next_act(obj):
            trace_acts_list.append(obj)
            # формируем последовательный список
            if prop_class and len(trace_acts_list) > 1:
                # привязываем next, если указано
                prev_obj = trace_acts_list[-2]
                obj = trace_acts_list[-1]
                # print(">>", prev_obj, "-<-", obj)
                make_triple(prev_obj, prop_class, obj)
            if trace_acts_list:
                num = len(trace_acts_list)
                make_triple(obj, onto.student_index, num)


        def find_act(class_, executes: int, exec_time: int, **fields: dict):
            for obj in class_.instances():
                # print(F"{obj}: ")
                if ((
                    # an act executes a boundary while trace executes algorithm itself
                    obj.executes.INDIRECT_boundary_of or obj.executes
                    ).id == executes and
                    ((obj.exec_time == exec_time) or (exec_time is None)) and
                    (self.trace_obj in obj.in_trace) and
                    all((getattr(obj, k, None) == v) or (v is None)  for k,v in fields.items())):
                    return obj
            print(f"act not found: ex={executes}, {', '.join([f'n={exec_time}'] + [f'{k}={v}' for k,v in fields.items()])}")
            return None


        with onto:
            i = 0
            # act_index = 0
            trace_acts_list = []
            trace_acts_list.append(find_act(onto.trace, self.data["algorithm"]["id"], 0))
            for d in trace:
                i += 1
                if "id" in d:
                    id_         = d.get("id")
                    executes    = d.get("executes")
                    # phase: (started|finished|performed)
                    phase       = d.get("phase")  # , "performed"
                    n           = d.get("n", None) or d.get("n_", None)
                    iteration_n = d.get("iteration_n", None)
                    name        = d.get("name", None)  or  d.get("action", None)  # !  name <- action
                    text_line   = d.get("text_line", None)
                    expr_value  = d.get("value", None)

                    id_         = int(id_)
                    clean_name  = prepare_name(name)
                    phase_mark  = {"started":"b", "finished":"e", "performed":"p",}[phase]
                    n           = n and int(n)  # convert if not None (n cannot be 0)
                    number_mark = "" if not n else ("_n%d" % n)

                    # find related algorithm element
                    assert executes in self.id2obj, (self.id2obj, d)
                    alg_elem = self.id2obj[executes]


                    # iri_template = "{}%s_{}{}".format(text_line or id_, clean_name, number_mark)

                    if phase_mark in ("b", "p"):
                        # начало акта
                        obj = find_act(onto.act_begin, executes, n or None)
                        if obj:
                            for class_ in additional_classes:
                                obj.is_a.append(class_)
                            # привязываем нужные свойства
                            make_triple(obj, onto.text_line, text_line)
                            make_triple(obj, onto.id, id_)  # ID могут быть не уникальны, но должны соответствовать id актов из GIU
                            if iteration_n:
                                make_triple(obj, onto.student_iteration_n, iteration_n)

                            connect_next_act(obj)
                        else:
                            print("  act name:", name)
                        # # НЕ привязываем id (т.к. может повторяться у начал и концов. TO FIX?)
                            # if "value" in d:
                        #     make_triple(obj, onto.expr_value, d["value"])

                    if phase_mark in ("e", "p"):
                        # конец акта
                        obj = find_act(onto.act_end, executes, n or None)
                        if obj:
                            for class_ in additional_classes:
                                obj.is_a.append(class_)
                            # привязываем нужные свойства
                            make_triple(obj, onto.text_line, text_line)
                            make_triple(obj, onto.id, id_)  # ID могут быть не уникальны, но должны соответствовать id актов из GIU
                            if expr_value is not None:
                                make_triple(obj, onto.expr_value, expr_value)
                            if iteration_n:
                                make_triple(obj, onto.student_iteration_n, iteration_n)

                            connect_next_act(obj)
                        else:
                            print("  act name:", name)

            # iri_list_key = act_classnames[0] + "_iri_list"
            # self.data[iri_list_key] = trace_acts_list


    def test_with_ontology_results(self, onto):
        pass


def make_trace_for_algorithm(alg_dict):
    'just a wrapper for TraceTester.make_correct_trace() method'
    try:
        trace_data = {
            "algorithm": alg_dict,
            "header_boolean_chain": None,
        }
        tt = TraceTester(trace_data)
        tt.prepare_id2obj()
        tt.make_correct_trace()

        # Очистить словарь alg_dict["id2obj"] от рекурсивной ссылки на сам alg_dict
        for key in alg_dict["id2obj"]:
            if alg_dict["id2obj"][key] is alg_dict:
                del alg_dict["id2obj"][key]
                break

        return tt.data["correct_trace"]
    except Exception as e:
        print("Error !")
        print("Error making correct_trace:")
        print(" ", e)
        # raise e  # useful for debugging
        return str(e)


def algorithm_only_to_onto(alg_tr, onto):
    '''just a wrapper for TraceTester.inject_algorithm_to_ontology() method:
        inject only the algorithm, omit any trace-related triples'''
    try:
        alg_dict = alg_tr["algorithm"]
        trace_data = {
            "algorithm": alg_dict,
            "algorithm_name": alg_tr["algorithm_name"],
            "header_boolean_chain": None,
        }
        tt = TraceTester(trace_data)
        tt.prepare_id2obj()
        tt.inject_algorithm_to_ontology(onto)

        # Очистить словарь alg_dict["id2obj"] от рекурсивной ссылки на сам alg_dict
        for key in alg_dict["id2obj"]:
            if alg_dict["id2obj"][key] is alg_dict:
                del alg_dict["id2obj"][key]
                break

        return tt.data["algorithm"]
    except Exception as e:
        print("Error !")
        print("Error injecting algorithm:")
        print(" ", e)
        raise e  # useful for debugging
        return str(e)



def init_persistent_structure(onto):
    # types.new_class(temp_name, (domain >> range_, ))  # , Property

    skos = onto.get_namespace("http://www.w3.org/2004/02/skos/core#")

    with onto:
        # Статические определения

        # skos:Concept
        class Concept(Thing):
            namespace = skos

        # class related_to_concept(DatatypeProperty): pass

        # новое свойство id
        if not onto["id"]:
            id_prop = types.new_class("id", (Thing >> int, FunctionalProperty, ))
        # ->
        class act(Concept): pass
        # -->
        class act_begin(act): pass
        # --->
        class trace(act_begin): pass
        # -->
        class act_end(act): pass
        # -->
        class implicit_act(act):
            'act that skipped by student but added instead by rules'
            pass
        # # -->
        # class student_act(act): pass
        # -->
        class correct_act(act): pass
        # # -->
        class normal_flow_correct_act(correct_act): pass
        # hide so far
        # class breaking_flow_correct_act(correct_act): pass
        # AllDisjoint([
        #   normal_flow_correct_act,
        #   breaking_flow_correct_act
        # ])

        # ->
        class linked_list(Thing): pass

        # ->
        class action(Concept): pass
        class algorithm(Concept): pass

        class entry_point(algorithm >> action, FunctionalProperty): pass

        ##### Граф между действиями алгоритма
        class boundary(Thing): pass  # begin or end of an action
        class boundary_of(boundary >> action, FunctionalProperty): pass
        class begin_of(boundary_of): pass
        class   end_of(boundary_of): pass
        class  halt_of(boundary_of): pass  # interrupted_end_of
        class interrupt_origin(boundary >> boundary): pass
        # class statement_begin(Thing): pass
        # class statement_end  (Thing): pass

        # hide so far
        # class hide_boundaries(action):
        #     """tells a complex action no to show (to skip) begin/end acts in not-collapsed mode."""
        #     pass

        # helper
        class gathered_child_exec_till(act >> act): pass
        # helper
        class gather_child_exec_till(gathered_child_exec_till): pass
        # helper
        class child_executes(act >> boundary): pass

        # новое свойство consequent - ребро графа переходов, заменяющего правильную трассу
        class consequent(Thing >> Thing, ): pass

        # class verbose_consequent(consequent): pass
        # class visible_consequent(consequent): pass

        # окрестность - ближайшее будущее, до условия
        class has_upcoming(boundary >> boundary, TransitiveProperty): pass

        # class interrupting_consequent(consequent): pass
        # + subclasses
        class normal_consequent(consequent): pass
        class always_consequent(normal_consequent, has_upcoming): pass
        class on_true_consequent(normal_consequent): pass
        class on_false_consequent(normal_consequent): pass
        ##### Граф связей между действиями алгоритма


        # ->
        class sequence(action): pass

        # признак first
        class first_item(Thing, ): pass
        # признак last
        class last_item(Thing, ): pass
        # индекс в списке
        class item_index(Thing >> int, FunctionalProperty): pass

        # ->
        class loop(action): pass

        if loop:  # hide a block under code folding
            # classes that regulate the use of condition in a loop

            # normal condition effect (false->stop, true->start a body) like in while, do-while, for loop types
            class conditional_loop(loop): pass

            # no condition at all: infinite loop like while(true){...}. The only act endlessly executed is the loop body.
            class unconditional_loop(loop): pass
            # # inverse condition effect (false->start a body, true->stop) like in do-until loop
            # inverse_conditional_loop = types.new_class("inverse_conditional_loop", (loop,))

            # The constraint is not useful so far
            # AllDisjoint([conditional_loop, unconditional_loop])

            class infinite_loop(unconditional_loop): pass
            class ntimes_loop(unconditional_loop): pass


            # classes that regulate a loop execution start (which act should be first)
            #
            # start with cond
            class start_with_cond(conditional_loop): pass
            # start with body
            class start_with_body(loop): pass
            # start with init
            class start_with_init(conditional_loop): pass

            # The constraint is not useful so far
            # AllDisjoint([start_with_cond, start_with_body, start_with_init])


            # classes that regulate the use of "update" step in a for-like loop (both subclasses of "loop_with_initialization" as that loop have "update" step too)
            #
            # update first, then the body, like in foreach loop type
            class pre_update_loop(conditional_loop): pass
            # body first, then the update, like in for(;;) loop type
            class post_update_loop(conditional_loop): pass

            AllDisjoint([pre_update_loop, post_update_loop])


            # classes that indicate whether condition and body follow each other instantly or not (note that: these classes are not disjointed; these classes are to be inferred from another defined features via equivalent_to definition so no direct inheritance required for known loops)
            # class body_then_cond(loop):
            #     equivalent_to = [inverse_conditional_loop | (conditional_loop & (Not(post_update_loop)))]
            # class cond_then_body(loop):
            #     equivalent_to = [conditional_loop & (Not(pre_update_loop))]

            # workaround: do not use the inference, declare explicitly
            class cond_then_body(conditional_loop): pass
            class body_then_cond(conditional_loop): pass

            # classes that define well-known loops as subclasses of the above defined loop-feature classes. These classes are to be used publicly
            class while_loop(start_with_cond): pass
            while_loop.is_a += [cond_then_body, body_then_cond]  # workaround
            while_loop.label = ["WHILE"]

            class do_while_loop(start_with_body): pass
            do_while_loop.is_a += [cond_then_body, body_then_cond]  # workaround
            do_while_loop.label = ["DO-WHILE"]

            # class do_until_loop(inverse_conditional_loop, postconditional_loop): pass
            # do_until_loop.is_a += [body_then_cond]  # workaround
            # do_until_loop.label = ["DO-UNTIL"]

            class for_loop(post_update_loop, start_with_init): pass
            for_loop.is_a += [cond_then_body]  # workaround
            for_loop.label = ["FOR"]

            class foreach_loop(pre_update_loop, start_with_cond): pass
            foreach_loop.is_a += [body_then_cond]  # workaround
            foreach_loop.label = ["FOREACH"]



        # -->
        class alt_branch(sequence): pass
        class func(action): pass
        # class func(sequence): pass
        class alternative(action): pass

        # # make algorithm elements classes
        # for class_name in [
        #     "alternative",
        # ]:
        #     types.new_class(class_name, (action,))

        for class_name in [
            "expr", "stmt", "interrupt_action",
        ]:
            types.new_class(class_name, (action, ))  ### hide_boundaries

        for class_name in [
            "return", "break", "continue",  # have `interrupt_target`
        ]:
            cls = types.new_class(class_name, (onto['interrupt_action'], ))
            # add annotation name: rdfs:label
            cls.label = [class_name]

        for class_name in [
            "if", "else-if", "else",
        ]:
            types.new_class(class_name, (alt_branch,))

        # make some properties
        for prop_name in ("body", "cond", "init", "update", "wrong_next_act", "interrupt_target", ):
            if not onto[prop_name]:
                types.new_class(prop_name, (Thing >> Thing,))

        # новое свойство executes
        prop_executes = types.new_class("executes", (Thing >> Thing, FunctionalProperty, ))
        class executes_id(act >> int, FunctionalProperty): pass

        # новое свойство expr_value
        prop_expr_value = types.new_class("expr_value", (DataProperty, FunctionalProperty, ))

        # новое свойство stmt_name
        prop_stmt_name = types.new_class("stmt_name", (Thing >> str, DataProperty, FunctionalProperty))

        # новое свойство next
        types.new_class("next", (Thing >> Thing, ))
        types.new_class("next_act", (correct_act >> correct_act, FunctionalProperty, InverseFunctionalProperty))

        # новое свойство student_next
        types.new_class("student_next", (act >> Thing, ))
        types.new_class("student_next_latest", (act >> act, onto.student_next))

        # новое свойство next_sibling -- связывает акты, соседние по номеру раза выполнения (причём, начальные и конечные акты - раздельно)
        next_sibling = types.new_class("next_sibling", (Thing >> Thing, ))

        # новое свойство before
        # prop_before = types.new_class("before", (Thing >> Thing, TransitiveProperty))

        # новое свойство in_trace
        prop_in_trace = types.new_class("in_trace", (act >> trace, ))

        # свойство index
        types.new_class("index", (Thing >> int, FunctionalProperty, ))
        types.new_class("student_index", (Thing >> int, FunctionalProperty, ))
        # номер итерации
        types.new_class("student_iteration_n", (act >> int, FunctionalProperty, ))
        types.new_class("iteration_n", (act >> int, FunctionalProperty, ))

        types.new_class("after_act", (Thing >> act, ))

        # новое свойство exec_time
        prop_exec_time = types.new_class("exec_time", (Thing >> int, FunctionalProperty, ))
        # новое свойство depth
        class depth(Thing >> int, FunctionalProperty, ): pass
        # # новое свойство correct_depth
        # prop_correct_depth = types.new_class("correct_depth", (Thing >> int, FunctionalProperty, ))

        # новое свойство text_line
        prop_text_line = types.new_class("text_line", (Thing >> int, FunctionalProperty, ))

        # prop_has_student_act = types.new_class("has_student_act", (Thing >> act, ))
        # prop_has_correct_act = types.new_class("has_correct_act", (Thing >> act, ))
        # # новое свойство same_level
        # prop_same_level = types.new_class("same_level", (Thing >> Thing, SymmetricProperty))
        # # новое свойство child_level
        # prop_child_level = types.new_class("child_level", (Thing >> Thing, SymmetricProperty))

        # make string_placeholder properties
        class string_placeholder(Thing >> str): pass
        for suffix in (
            "A", # "B", "C", "D", "EX",
            "kind_of_loop",
            "kind_of_action",
            "TrueFalse",
            "BEGIN",  # для CorrespondingEndMismatched
            "EXTRA",  # для NotNeighbour
            "MISSING",  # пропущены перед текущим
            "COND",     # любое условие (общий случай)
            "INNER",    # для CorrespondingEndMismatched: несоответствующее начало, которое явл. вложенным действием несоответствующего конца
            "CONTEXT",    # (неверный) родитель (по трассе)
            "PARENT",   # верный родитель
            "PREVIOUS", # TooLateInSequence: тот, что должен быть после, но он перед текущим
            "LOOP",
            "LOOP_COND",
            "INIT",
            "UPDATE",
            "ALT",
            "ALT_COND", # любое из условий (перечисляет все условия)
            "CURRENT_ALT_COND", # текущее условие
            # "PREV_ALT_COND",
            "LATEST_ALT_COND", # выполн. последним, но не текущее условие
            "EXPECTED_ALT_COND", # ожидаемое, но отсутствующее
            "REQUIRED_COND", # условие, которое не вычислено
            "UNEXPECTED_ALT_COND", # не ожидаемое, но присутствующее
            "BRANCH",  # уже выполнилась
            "BRANCH2",
            "EXPECTED_BRANCH", "UNEXPECTED_BRANCH",
            # "ELSE_BRANCH", # "BRANCHES"
            "SEQ",
            "NEXT",
            "NEXT_COND",
        ):
            prop_name = "field_" + suffix
            if not onto[prop_name]:
                types.new_class(prop_name, (string_placeholder, ))

        class fetch_kind_of_loop(act >> action, ): pass
        class reason_kind(boundary >> Thing, ): pass
        class to_reason(Thing >> Thing, ): pass
        class from_reason(Thing >> Thing, ): pass

        # новое свойство corresponding_end
        class corresponding_end(act_begin >> act_end, ): pass
        class student_corresponding_end(act_begin >> act_end, ): pass

        class hasPartTransitive(Thing >> Thing, TransitiveProperty): pass
        # новое свойство parent_of
        # class parent_of(act_begin >> act, InverseFunctionalProperty): pass
        class parent_of(hasPartTransitive, InverseFunctionalProperty): pass
        class student_parent_of(Thing >> Thing, InverseFunctionalProperty): pass

        class branches_item(parent_of): pass
        class body(parent_of): pass
        class body_item(parent_of): pass

        # объекты, спровоцировавшие ошибку
        if not onto["Erroneous"]:
            Erroneous = types.new_class("Erroneous", (Thing,))

            # category2priority = None  # declare it later
            # class error_priority(Thing >> int): pass

            # class-level properties (called Annotations)
            class involves_concept(AnnotationProperty): pass
            class principal_violation(AnnotationProperty): pass

            # reason node can be associated with violations poassible at the step of solution
            class possible_violation(ObjectProperty): pass

            # make Erroneous subclasses
            # (class, [bases])
            for class_spec in [
                # (name, [bases], err_level, {related, concepts})

                # Sequence mistakes ...
                ("CorrespondingEndMismatched", (), "trace_structure", {'action'}),
                ("WrongNext", (), "general_wrong", {'action'}),

                # "CorrespondingEndPerformedDifferentTime",
                # "WrongExecTime",
                # "ActStartsAfterItsEnd", "ActEndsWithoutStart",
                # "AfterTraceEnd",
                # "DuplicateActInSequence",
                ("ConditionMisuse", ["WrongNext"], "general_wrong", {'expr'}),

                ("WrongContext", (), "wrong_context", {'action'}),
                # ("MisplacedBefore", ["WrongContext"]),
                # ("MisplacedAfter", ["WrongContext"]),
                ("MisplacedDeeper", ["WrongContext"], "wrong_context", {'action'}),
                ("EndedDeeper", ["WrongContext", ], "wrong_context", {'action'}),  # +
                ("EndedShallower", ["WrongContext", "CorrespondingEndMismatched"], "wrong_context", {'action'}), # не возникнет для первой ошибки в трассе.
                ("OneLevelShallower", ["WrongContext"], "concrete_wrong_context", {'action'}), # +

                ("NeighbourhoodError", ["WrongNext"], "general_wrong", {'action'}),  # check that one of the following is determined
                ("UpcomingNeighbour", ["NeighbourhoodError"], "missing", {'action'}), #
                ("NotNeighbour", ["NeighbourhoodError"], "extra", {'action'}), # disjoint with UpcomingNeighbour
                ("WrongCondNeighbour", ["NotNeighbour", "ConditionMisuse"], "by_different_cond", {'action'}), #

                # interrupted flow
                ("UnexpectedWhenInterrupting", ["NotNeighbour", ], "extra", {'action'}), #
                ("TooEarlyWhenInterrupting", ["UpcomingNeighbour", ], "missing", {'action'}), #

                # ("ExtraAct", ["WrongNext"]),
                ("DuplicateOfAct", [], "extra", {'sequence'}),
                # "MissingAct",
                # "TooEarly", # right after missing acts
                # ("DisplacedAct", ["TooEarly","ExtraAct","MissingAct"]), # act was moved somewhere
                ("TooLateInSequence", ["WrongNext"], "extra", {'sequence'}), # +
                ("TooEarlyInSequence", ["WrongNext"], "missing", {'sequence'}), # +
                ("SequenceFinishedNotInOrder", (), "extra", {'sequence'}),  # выполнены все действия, но в конце не последнее; не возникнет для первой ошибки в трассе.
                ("SequenceFinishedTooEarly", ["SequenceFinishedNotInOrder"], "missing", {'sequence'}), # +

                # Alternatives mistakes ...
                ("NoFirstCondition", (), "missing", {'alternative', 'if', 'expr'}), # +
                ("NoAlternativeEndAfterBranch", (), "missing", {'alternative', 'alt_branch'}), # +
                ("CondtionNotNextToPrevCondition", (), "extra", {'alternative', 'else-if', 'expr'}), # +
                ("ConditionAfterBranch", ["NoAlternativeEndAfterBranch", "CondtionNotNextToPrevCondition"], "extra", {'alternative', 'alt_branch', 'expr'}), # ~
                ("DuplicateOfCondition", ["CondtionNotNextToPrevCondition", "ConditionAfterBranch"], "extra", {'alternative', 'if', 'else-if', 'expr'}),  # +
                # ("WrongBranch", ["ExtraAct"]),
                ("BranchOfFalseCondition", ["ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'expr'}),
                ("AnotherExtraBranch", ["NoAlternativeEndAfterBranch"], "extra", {'alternative', 'alt_branch'}), # +
                ("BranchWithoutCondition", (), "extra", {'alternative', 'alt_branch', 'expr'}), # +
                ("BranchNotNextToCondition", ["BranchWithoutCondition"], "missing", {'alternative', 'alt_branch', 'expr'}), # +
                ("ElseBranchNotNextToLastCondition", ["BranchWithoutCondition"], "extra", {'alternative', 'alt_branch', 'else', 'expr'}), # +
                ("ElseBranchAfterTrueCondition", ["BranchWithoutCondition", "ElseBranchNotNextToLastCondition", "ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'else', 'expr'}), # ~
                ("NoBranchWhenConditionIsTrue", ["ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'expr'}), # +
                ("LastConditionIsFalseButNoElse", (), "missing", {'alternative', 'alt_branch', 'else', 'expr'}), # +
                ("NoNextCondition", (), "missing", {'alternative', 'expr'}), # ~
                ("ConditionTooLate", ["NoNextCondition", "CondtionNotNextToPrevCondition"], "extra", {'alternative', 'expr'}), # - skip for now
                ("ConditionTooEarly", ["NoFirstCondition", "NoNextCondition", "CondtionNotNextToPrevCondition"], "extra", {'alternative', 'expr'}), # +
                ("LastFalseNoEnd", (), "missing", {'alternative', 'expr'}), # +
                ("AlternativeEndAfterTrueCondition", ["ConditionMisuse"], "by_different_cond", {'alternative', 'alt_branch', 'expr'}),  # +

                # Loops mistakes ...
                # a general Loop
                ("NoLoopEndAfterFailedCondition", (), "missing", {'loop', 'expr'}),  # +
                ("LoopContinuedAfterFailedCondition", ["NoLoopEndAfterFailedCondition", "ConditionMisuse"], "by_different_cond", {'loop', 'expr'}), # +
                ("IterationAfterFailedCondition", ["LoopContinuedAfterFailedCondition"], "extra", {'loop', 'expr'}), # +
                ("LoopEndsWithoutCondition", (), "extra", {'loop', 'expr'}),  # +
                # start_with_cond
                ("LoopStartIsNotCondition", (), "missing", {'while_loop', 'expr'}), # +
                # start_with_body
                ("LoopStartIsNotIteration", (), "missing", {'do_while_loop'}), # +
                # cond_then_body (-> true)
                ("NoIterationAfterSuccessfulCondition", (), "missing", {'while_loop', 'do_while_loop', 'for_loop', 'expr'}),  # +
                ("LoopEndAfterSuccessfulCondition", ["NoIterationAfterSuccessfulCondition", "ConditionMisuse"], "by_different_cond", {'while_loop', 'do_while_loop', 'for_loop', 'expr'}), # +
                # body_then_cond
                ("NoConditionAfterIteration", (), "missing", {'while_loop', 'do_while_loop', 'expr'}), # +
                ("NoConditionBetweenIterations", ["NoConditionAfterIteration"], "missing", {'while_loop', 'do_while_loop', 'expr'}), # +
                # ForLoop
                ("LoopStartsNotWithInit", (), "missing", {'for_loop', }),
                ("InitNotAtLoopStart", (), "extra", {'for_loop', }),
                ("NoConditionAfterForInit", (), "missing", {'for_loop', 'expr'}),
                ("IterationAfterForInit", ["NoConditionAfterForInit"], "extra", {'for_loop', }),
                ("NoUpdateAfterIteration", (), "missing", {'for_loop', }),
                ("UpdateNotAfterIteration", (), "extra", {'for_loop', }),
                ("ForConditionAfterIteration", ["UpdateNotAfterIteration"], "extra", {'for_loop', 'expr'}),
                ("NoConditionAfterForUpdate", (), "missing", {'for_loop', }),
                # ForeachLoop
                ("NoForeachUpdateAfterSuccessfulCondition", (), "missing", {'foreach_loop', }),
                ("ForeachUpdateNotAfterSuccessfulCondition", (), "extra", {'foreach_loop', }),
                ("NoIterationAfterForeachUpdate", (), "missing", {'foreach_loop', }),
                ("IterationNotAfterForeachUpdate", (), "extra", {'foreach_loop', }),
            ]:
                if isinstance(class_spec, str):
                    types.new_class(class_spec, (Erroneous,))
                elif isinstance(class_spec, tuple):
                    class_name, base_names = class_spec[:2]
                    bases = tuple((onto[base_name] if type(base_name) is str else base_name) for base_name in base_names)
                    # print(bases)
                    created_class = types.new_class(class_name, bases or (Erroneous,))
                    related_concepts = class_spec[3]
                    created_class.involves_concept = list(map(onto.__getattr__, sorted(related_concepts)))

                    ## if len(class_spec) >= 3:
                    ##     category = class_spec[2]
                    ##     if not category2priority:
                    ##         category2priority = {n:i for i,n in enumerate([
                    ##             "trace_structure",
                    ##             "general_wrong",
                    ##             "wrong_context",
                    ##             "concrete_wrong_context",
                    ##             "extra",
                    ##             "by_different_cond",
                    ##             "missing",
                    ##             # "",
                    ##         ])}
                    ## assert category in category2priority, (category, class_name)
                    ## priority = category2priority[category]
                    ## # set error_priority
                    ## ## ??????
                    ## make_triple(created_class, error_priority, priority)


        for prop_name in ("precursor", "cause", "has_causing_condition", "should_be", "should_be_before", "should_be_after", "context_should_be"):
            if not onto[prop_name]:
                types.new_class(prop_name, (onto["Erroneous"] >> Thing,))

        # make consequent subproperties (always_consequent is default base)
        for class_spec in [
            #: (name, [base], [principal_violations])
            # "DebugObj",
            # "FunctionBegin",
            # "FunctionEnd",
            # "FunctionBodyBegin",
            "StmtEnd",
            "ExprEnd",

            ("Interrupted", 0, []),  #  [??]
            ("GlobalCodeBegin", 0, ['TooEarlyInSequence', 'SequenceFinishedTooEarly']),
            ("SequenceBegin", 0, ['TooEarlyInSequence', 'SequenceFinishedTooEarly']),
            ("SequenceNext", 0, ['DuplicateOfAct', 'TooEarlyInSequence', 'SequenceFinishedTooEarly']),
            ("SequenceEnd", 0, ['DuplicateOfAct']),

            ("AltBegin", 0, ['NoFirstCondition']),  # 1st condition
            ("AltBranchBegin", on_true_consequent, ['NoBranchWhenConditionIsTrue']),  # ElseBranchAfterTrueCondition (enabled by ELSE branch) - not included directly; see special rule from that whose process algorithms
            ("NextAltCondition", on_false_consequent, ['BranchOfFalseCondition']),
            ("AltElseBranchBegin", on_false_consequent, ['LastConditionIsFalseButNoElse', 'BranchOfFalseCondition']),
            ("AltEndAllFalse", on_false_consequent, ['LastFalseNoEnd']),
            ("AltEndAfterBranch", 0, ['NoAlternativeEndAfterBranch']),

            ("PreCondLoopBegin", 0, ['LoopStartIsNotCondition']),
            ("PostCondLoopBegin", 0, ['LoopStartIsNotIteration']),
            ("IterationBeginOnTrueCond", on_true_consequent, ['NoIterationAfterSuccessfulCondition']),
            # "IterationBeginOnFalseCond",
            ("LoopUpdateOnTrueCond", on_true_consequent, ['NoForeachUpdateAfterSuccessfulCondition']),
            ("IterationAfterUpdate", 0, ['NoIterationAfterForeachUpdate']),
            ("LoopEndOnFalseCond", on_false_consequent, ['NoLoopEndAfterFailedCondition']),
            # "LoopEndOnTrueCond",  # no rule yet?
            ("LoopCondBeginAfterIteration", 0, ['NoConditionAfterIteration']),
            ("LoopWithInitBegin", 0, ['LoopStartsNotWithInit']),
            ("LoopCondBeginAfterInit", 0, ['NoConditionAfterForInit']),
            ("LoopUpdateAfterIteration", 0, ['NoUpdateAfterIteration']),
            ("LoopCondAfterUpdate", 0, ['NoConditionAfterForUpdate']),
        ]:
            # types.new_class(class_name, (correct_act,))
            if isinstance(class_spec, str):
                types.new_class(class_spec, (always_consequent,))
            elif isinstance(class_spec, tuple):
                class_name, base_names = class_spec[:2]
                bases = tuple((onto[base_name] if type(base_name) is str else base_name) for base_name in [base_names] if base_name)
                # print(bases)
                created_class = types.new_class(class_name, bases or (always_consequent,))
                if len(class_spec) >= 3:
                    violations = class_spec[2]
                    created_class.principal_violation = list(map(onto.__getattr__, violations))

        for prop_name in ("reason", ):  # for correct acts !
            if not onto[prop_name]:
                types.new_class(prop_name, (correct_act >> Thing,))


def load_swrl_rules(onto, rules_list, rules_filter=None):
    """ rules_filter: None or callable hat receives name of rule and returns boolean """
    with onto:
        for r in rules_list:
            if rules_filter and not rules_filter(r):
                print("Ignoring SWRL rule:", r)
                continue

            try:
                Imp(r.name).set_as_rule(r.swrl)
            except Exception as e:
                print("Error in SWRL rule: \t", r.name)
                print(e)
                raise e

    return onto


def extact_mistakes(onto, as_objects=False, group_by=("text_line",), filter_by_level=False) -> dict:
    """Searches for instances of trace_error class and constructs a dict of the following form:
        "<error_instance1_name>": {
            "classes": ["list", "of", "class", "names", ...],
            "explanations": ["list", "of", "messages", ...],
            "<property1_name>": ["list", "of", "property", "values", ...],
            "<property2_name>": [onto.iri_1, "reference", "can present", "too", ...],
            ...
        },
        "<error_instance2_name>": {},
        ...

     """
    error_classes = onto.Erroneous.descendants()  # a set of the descendant Classes (including self)

    ### print("Erroneous descendants:", error_classes)

    properties_to_extract = ("id", "name", onto.precursor, onto.cause, onto.should_be, onto.should_be_before, onto.should_be_after, onto.context_should_be, onto.text_line, )

    # remove absent properties
    group_by = [pnm for pnm in group_by if onto[pnm]]
    # set default if empty so far
    group_by = group_by or ("name",)

    def inst_keys(inst):
        values = []
        for prop_name in group_by:
            values.append(getattr(inst, prop_name) if hasattr(inst, prop_name) else None)
        return tuple(values)

    if filter_by_level:
        categories = [
            onto.UpcomingNeighbour,
            onto.WrongCondNeighbour,
            onto.NotNeighbour,
            onto.Erroneous
        ]
    else:
        categories = [onto.Erroneous]

    mistakes = {}

    for error_class in categories:
        # The .instances() class method can be used to iterate through all Instances of a Class (including its subclasses). It returns a generator.
        for inst in error_class.instances():

            ###
            print("Erroneous instance:", inst.name)
            key = inst_keys(inst)
            d = mistakes.get(key, {})
            mistakes[key] = d

            for prop in properties_to_extract:
                values = []
                # fill values ...
                if isinstance(prop, str):
                    prop_name = prop
                    values.append(getattr(inst, prop_name))
                else:
                    prop_name = prop.name
                    for s,o in prop.get_relations():
                        if s == inst:
                            if not as_objects:
                                o = o.name if hasattr(o, "name") else o
                            values.append(o)

                d[prop_name] = values

            classes = get_leaf_classes((set(inst.is_a) | set(d.get("classes", {}))) & error_classes)
            d["classes"] = [class_.name for class_ in classes]
            expanded_explanations = format_explanation(onto, inst)
            explanations = [d["explanation"] for d in expanded_explanations]
            d["explanations"] = sorted(set(d.get("explanations", []) + explanations))
            d["mistakes"] = expanded_explanations
        if mistakes:
            break

    return mistakes


def create_ontology_tbox() -> "onto":
    # global ONTOLOGY_maxID

    # создание онтологии
    onto = get_isolated_ontology(ONTOLOGY_IRI)
    clear_ontology(onto, keep_tbox=False)  # True

    with onto:
        # каркас онтологии
        init_persistent_structure(onto)
    return onto


###
from common_helpers import Checkpointer


def process_algtraces(trace_data_list, debug_rdf_fpath=None, verbose=1,
                      mistakes_as_objects=False, filter_by_level=False, extra_act_entries=0,
                      rules_filter=None, reasoning="jena", on_done=None, _eval_max_traces=None) -> "onto, mistakes_list":
    """Write number of algorithm - trace pair to an ontology, perform extended reasoning and then extract and return the mistakes found.
      reasoning: None or "stardog" or "pellet" or "prolog" or "jena" or "sparql" or "clingo" or "dlv"
    """

    ch = Checkpointer()

    onto = create_ontology_tbox()

    ch.hit("create ontology tbox")

    if verbose: print("... TBox created")

    # наполняем онтологию с нуля сущностями с теми именами, которые найдём в загруженных json-словарях

    if _eval_max_traces is not None:
        # adjust the list size
        if _eval_max_traces <= len(trace_data_list):
            trace_data_list = trace_data_list[0:_eval_max_traces+1]
        else:
            from itertools import cycle
            cycled = cycle(trace_data_list)
            for trace in cycled:
                trace_data_list.append(trace)
                if len(trace_data_list) == _eval_max_traces:
                    break

    ### trace_data_list = ()  # debug!

    for tr_data in trace_data_list:
        tt = TraceTester(tr_data)
        tt.inject_to_ontology(onto)
        if verbose: print(end=".")

    ch.hit("fill ontology data")

   # после наложения обёртки можно добавлять SWRL-правила
    if reasoning == "pellet":  # incorporating of SWRL is only necessary for Pellet
        from ctrlstrct_swrl import filtered_rules
        # hardcode so far >
        tags_enabled = set("""
            helper correct mistake entry function sequence alternative loop
            """.split())
        load_swrl_rules(onto, filtered_rules(tags_enabled), rules_filter=rules_filter)

    if debug_rdf_fpath:
        onto.save(file=debug_rdf_fpath, format='rdfxml')
        print("Saved RDF file: {} !".format(debug_rdf_fpath))

    # exit()


    if reasoning == "pellet":
        print(">_ running Pellet ...")

        if _eval_max_traces is not None:
            measure_stats_for_pellet_running()

        start = timer()

        with onto:
            # запуск Pellet
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=0)

        end = timer()
        seconds = end - start
        time_report = "   Time elapsed: %.3f s." % seconds
        print(">_ Pellet finished")
        print(time_report)

        if _eval_max_traces is not None:
            run_stats = get_process_run_stats()
            run_stats.update({"wall_time": seconds})
            return run_stats

        if debug_rdf_fpath:
            onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
            print(f"Saved RDF file: {debug_rdf_fpath}_ext.rdf !")


    if reasoning in ("clingo", "dlv"):
        print(f">_ running {reasoning} ...")

        import asp_helpers

        measure_f, run_f = {
            "clingo": (measure_stats_for_clingo_running, asp_helpers.run_clingo_on_ontology),
            "dlv": (measure_stats_for_dlv_running, asp_helpers.run_DLV_on_ontology),
        }.get(reasoning)

        if _eval_max_traces is not None:
            measure_f()

        start = timer()

        # запуск Clingo / DLV
        onto, elapsed_times = run_f(onto, stats=True)

        end = timer()
        seconds = end - start
        time_report = "   Time elapsed: %.3f s." % seconds
        print(f">_ {reasoning} finished")
        print(time_report)

        if _eval_max_traces is not None:
            run_stats = get_process_run_stats()
            run_stats.update(elapsed_times)  # add data from dict
            return run_stats

        if debug_rdf_fpath:
            onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
            print(f"Saved RDF file: {debug_rdf_fpath}_ext.rdf !")


    if reasoning == "prolog":
        name_in = "pl_in.rdf"
        name_out = "pl_out.rdf"
        onto.save(file=name_in, format='rdfxml')

        eval_stats = run_swiprolog_reasoning(name_in, name_out, verbose=0)

        if _eval_max_traces is not None:
            return eval_stats

        # ! TODO: use delete_ontology & get_isolated_ontology
        clear_ontology(onto, keep_tbox=True)
        onto = get_ontology("file://" + name_out).load()
        seconds = eval_stats['wall_time']

    # invoke through jenaService:
    if reasoning == 'jena':
        # save ontology to buffer in memory
        # TODO: check if NTRIPLES will be processed faster!
        stream = io.BytesIO()
        onto.save(file=stream, format='rdfxml')
        result_rdf_bytes = invoke_jena_reasoning_service(rdfData=stream.getvalue())

        # Clear curent ontology data
        delete_ontology(onto)

        # read from byte stream
        # use isolated worlds (keep concurrent threads in mind)
        onto = get_isolated_ontology(ONTOLOGY_IRI).load(
            fileobj=io.BytesIO(result_rdf_bytes),
            reload=True, only_local=True)


    # old way: invoke jar directly, communicate via files.
    if reasoning in ('sparql', '--OLD--jena'):
        # Jena is main option (the other options are not maintained)
        name, uniq_n = Uniqualizer.get(reasoning)
        name_in = f"{name}_in.rdf"
        name_out = f"{name}_out.n3"
        onto.save(file=name_in, format='rdfxml')

        if 1:  # if 0, do not perform reasoning (rerun in debug)
            eval_stats = run_jena_reasoning(name_in, name_out, reasoning_mode=reasoning, verbose=False)
        else:
            eval_stats = {"wall_time": 0}

        if _eval_max_traces is not None:
            # print('   Jena elapsed:', eval_stats['wall_time'])  ###
            return eval_stats

        # Clear curent ontology data
        ### clear_ontology(onto, keep_tbox=True)  # previous variant
        onto.destroy()

        # read from file in force reload mode
        # ! use get_isolated_ontology
        onto = get_ontology("file://" + name_out).load(reload=True, only_local=True)

        ### print("New base_iri:", onto.base_iri)
        ### print("=== Ontology size ===:", len(onto.get_triples()))

        delete_file(name_in)
        delete_file(name_out)
        Uniqualizer.free(reasoning, uniq_n)  # allow reusing of names since correct reload of the ontology works!

        seconds = eval_stats['wall_time']

    if on_done:
        on_done(seconds)

    # return onto, []  ### Debug exit
    # exit()

    ch.hit("reasoning completed")

    mistakes = extact_mistakes(onto, as_objects=mistakes_as_objects, filter_by_level=filter_by_level)
    ch.hit("mistakes extracted")

    return onto, list(mistakes.values())


def sync_jena(onto, rules_path=None, reasoning='jena', verbose=1) -> 'new onto':
    name_in = f"{reasoning}_in.rdf"
    name_out = f"{reasoning}_out.n3"
    onto.save(file=name_in, format='rdfxml')

    eval_stats = run_jena_reasoning(name_in, name_out, reasoning_mode=reasoning, verbose=verbose, rules_path=rules_path)

    clear_ontology(onto, keep_tbox=False)

    ## onto = get_ontology("file://" + name_out).load()
    # namespace cached so not overwritten workaround:
    # new_world = World()
    # onto = new_world.get_ontology
    onto = get_isolated_ontology("file://" + name_out).load()
    ### print("New base_iri:", onto.base_iri)

    return onto


def clear_ontology(onto, keep_tbox=False):
    if not keep_tbox:
        for cls in onto.classes():
            destroy_entity(cls)
    for ind in onto.individuals():
        destroy_entity(ind)


def plain_list(list_of_lists):
    " -> generator"
    for x in list_of_lists:
        if isinstance(x, list):
            yield from plain_list(x)
        else:
            yield x

def find_by_type(dict_or_list, types=(dict,), _not_entry=None):
    "plain list of dicts or objects of specified type"
    _not_entry = _not_entry or set()
    if isinstance(dict_or_list, types):
        yield dict_or_list
        _not_entry.add(id(dict_or_list))
    if isinstance(dict_or_list, dict):
        for v in dict_or_list.values():
            if id(v) not in _not_entry:
                yield from find_by_type(v, types, _not_entry)
    elif isinstance(dict_or_list, (list, tuple, set)):
        for v in dict_or_list:
            if id(v) not in _not_entry:
                yield from find_by_type(v, types, _not_entry)


def save_schema(file_path='jena/control-flow-statements-domain-schema.rdf'):
    create_ontology_tbox().save(file_path)

    print("Saved as:\t", file_path)
    print()
    print("Don't forget to copy the result to:")
    print(r"c:\D\Work\YDev\CompPr\CompPrehension\src\main\resources\org\vstu\compprehension\models\businesslogic\domains" '\\')


def _play_with_classes():
    onto = create_ontology_tbox()
    descendants = [*onto.action.descendants()]
    # print(descendants)
    showable = get_leaf_classes(descendants)
    print(showable)
    showable = [n.name for n in showable]
    print("as strings:", showable)



if __name__ == '__main__':

    if 0:
        print("Special run mode activated:")
        print("Saving schema only to file.")
        save_schema()
        exit()

    if 1:
        print("Special run mode activated:")
        print("_play_with_classes()")
        _play_with_classes()
        exit()

    print("Please run *_test.py script instead!")
    exit()

