# import_algtr.py


""" Импорт алгоритмов и трасс из JSON-формата (из файлов, сгенерированных json2alg2tr), 
наполнение ими чистой онтологии,  
добавление SWRL-правил, определённых в ctrlstrct_swrl.py (используя import),
запуск рсширеного ризонинга с UpdOnto.
"""


import json
import re

# from owlready2 import *

from upd_onto import *
from transliterate import slugify
from trace_gen.txt2algntr import find_by_key_in, find_by_keyval_in


ONTOLOGY_maxID = 1

def prepare_name(s):
    return slugify(s) or s
    
            
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
    return iri


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

        # pprint(trace_data["trace"])
        # pprint(trace_data["algorithm"])
        # exit()
        
        # индекс всех объектов АЛГОРИТМА для быстрого поиска по id
        self.id2obj = self.data["algorithm"].get("id2obj", {})
        self.act_iris = []
        
        self._maxID = 1
        
    def newID(self, what=None):
        self._maxID += 1
        return self._maxID            
        
    def make_correct_trace(self):
        if "correct_trace" in self.data or "header_boolean_chain" not in self.data:
            print("make_correct_trace: aborting.")
            return
            
        self.data["correct_trace"] = []
        
        def _gen(states_str):
            for ch in states_str:
                yield bool(int(ch))
            while 1:
                yield False
                
        self.condition_value_generator = _gen(self.data["header_boolean_chain"])
        self.last_cond_tuple = (-1, False)
        self._maxID = max(self._maxID, max(self.id2obj.keys()) + 10)
        self.expr_id2values = {}
        
        def next_cond_value():
            i,_ = self.last_cond_tuple
            v = next(self.condition_value_generator)
            v = bool(v)
            self.last_cond_tuple = (i+1, v)
            return v
            
        # long "multi-entry" function
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
                value = next_cond_value()
                phase = "performed"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
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
                    
            if node["type"] in {"stmt"}:
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
                    
        
        alg_node = self.data["algorithm"]["entry_point"]
        
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
        
    def inject_to_ontology(self, onto, extra_act_entries=0):
        
        self.inject_algorithm_to_ontology(onto)
        
        self.make_correct_trace()
        self.prepare_act_candidates(onto, extra_act_entries=extra_act_entries)
        self.inject_trace_to_ontology(onto, self.data["trace"], (), "student_next")
        # self.inject_trace_to_ontology(onto, self.data["correct_trace"], ("correct_act",), "correct_next")
        # self.merge_traces(onto, self.data["student_act_iri_list"], self.data["correct_act_iri_list"])
        
    def inject_algorithm_to_ontology(self, onto):
        "Prepares self.id2obj and writes algorithm to ontology if it isn't there."
        with onto:
            alg_objects = list(find_by_type(self.data["algorithm"]))
            if not self.id2obj:
                # fill it once
                for d in alg_objects:
                    if "id" in d:
                        self.id2obj[ d["id"] ] = d
                # store to original algorithm dict
                self.data["algorithm"]["id2obj"] = self.id2obj
            
            if onto.algorithm_name and self.data["algorithm_name"] in [s for _,s in onto.algorithm_name.get_relations()]:
                # do nothing as the algorithm is in the ontology
                return
            
            # make algorithm classes and individuals
            for d in alg_objects:
                if "id" in d:
                    id_     = d.get("id")
                    type_   = d.get("type")
                    name    = d.get("name", "")
                    
                    assert type_, "Error in agrorithm object: "+str(d)
                    
                    id_         = int(id_)
                    clean_name  = prepare_name(name)
                    
                    class_ = onto[type_]
                    if not class_:
                        # make a new class in the ontology
                        class_ = types.new_class(type_, (Thing, ))
                        
                    # формируем имя экземпляра в онтологии
                    iri = "{}_{}".format(id_, clean_name)
                    
                    iri = uniqualize_iri(onto, iri)
                        
                    # сохраняем назад в наш словарь (для привязки к актам трассы) 
                    d["iri"] = iri
                    # создаём объект
                    obj = class_(iri)
                    # привязываем id
                    make_triple(obj, onto.id, id_)
                    # (имя не привязываем.)
                    
                    # make special string link identifying algorithm
                    if type_ == "algorithm":
                        prop = onto["algorithm_name"]
                        if not prop:
                            with onto:
                                # новое свойство по заданному имени
                                prop = types.new_class("algorithm_name", (Thing >> str, ))
                        make_triple(obj, prop, self.data["algorithm_name"])
                # else: raise "no id!"
                    
            for d in alg_objects:
                if "id" in d:
                    for k in d:  # ищем объекты среди полей словаря
                        v = d[k]
                        if isinstance(v, dict) and "id" in v and "iri" in v:
                            link_objects(onto, d["iri"], k, v["iri"], (Thing >> Thing, onto.parent_of,) )
                        elif isinstance(v, (list, set)):
                            # make an ordered sequence for list, unorederd for set
                            # print("check out list", k, "...")
                            # сделаем список, если в нём нормальные "наши" объекты
                            subobject_iri_list = [subv["iri"] for subv in v  if isinstance(subv, dict) and "id" in subv and "iri" in subv]
                            if not subobject_iri_list:
                                continue
                                
                            iri = d["iri"]
                            
                            # всякий список действий должен быть оформлен как sequence с полем body - списком.
                            if k == "body" and isinstance(v, list):
                                # делаем объект последовательностью (нужно для тел циклов, веток, функций)
                                onto[iri].is_a.append( onto.sequence )
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
                                    # первый / последний
                                    if i == 0:
                                        # mark as first elem of the list
                                        onto[subiri].is_a.append(onto.first_item)
                                    if i == len(subobject_iri_list)-1:
                                        # mark as last act of the list
                                        onto[subiri].is_a.append(onto.last_item)

        
    def prepare_act_candidates(self, onto, extra_act_entries=2):
        """Create all possible acts for each statement. 
        Maximum executon number will be exceeded by `extra_act_entries`.
        /* Resulting set of acts of size N will be repeated N times, each act to be possibly placed at each index of the trace, covering the set of all possible traces. */ """
        
        assert extra_act_entries >= 0, extra_act_entries
        
        alg_id2max_exec_n = {}  # executed stmt id to max exec_time in correct trace

        for act in self.data["correct_trace"]:
            executed_id = act["executes"]
            exec_n = act["n"]
            alg_id2max_exec_n[executed_id] = exec_n  # assume "n"s appear consequently in the trace
            
        # update the dict by adding extra_act_entries value for each stmt
        for st_id in self.id2obj.keys():
            alg_id2max_exec_n[st_id] = extra_act_entries + alg_id2max_exec_n.get(st_id, 0)
            
        # ensure that student's acts also exist
        for act in self.data["trace"]:
            executed_id = act["executes"]
            exec_n = act.get("n", "1")
            alg_id2max_exec_n[executed_id] = max(
                            int(exec_n),  # assume "n"s appear consequently in the trace
                            int(alg_id2max_exec_n[executed_id]))

        entry_stmt_id = self.data["correct_trace"][0]["executes"]
            
        max_act_ID = 1
        def set_id(act_obj):
            nonlocal max_act_ID
            max_act_ID += 1
            make_triple(act_obj, onto.id, max_act_ID)


        # make top-level act representing the trace
        iri = f'trace_{self.data["trace_name"]}_{"".join(map(str, map(int, self.data["header_boolean_chain"])))}'
        iri = uniqualize_iri(onto, iri)
        iri = prepare_name(iri)
        trace_obj = onto.trace(iri)
        trace_obj.is_a.append(onto.correct_act)
        make_triple(trace_obj, onto.executes, onto[self.data["algorithm"]["iri"]])
        set_id(trace_obj)
        make_triple(trace_obj, onto.index, 0)
        make_triple(trace_obj, onto.student_index, 0)
        make_triple(trace_obj, onto.exec_time, 0)  # set to 0 so next is 1
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
                    
                    for mark, class_ in [("b", onto.act_begin), ("e", onto.act_end)]:
                        iri = iri_template % mark
                        iri = uniqualize_iri(onto, iri)
                        
                        obj = class_(iri)
                        # obj.is_a.append(class_X)
                        make_triple(obj, onto.executes, onto[alg_elem["iri"]])
                        set_id(obj)
                        ### make_triple(obj, onto.index, index)
                        make_triple(obj, onto.exec_time, exec_n)
                        make_triple(obj, onto.in_trace, trace_obj)
                        
                        # connect "next_sibling"
                        if exec_n == 1:
                          make_triple(trace_obj, onto.next_sibling, obj)
                        else:
                          make_triple(mark2act_obj[mark], onto.next_sibling, obj)

                        # keep current value for next iteration
                        mark2act_obj[mark] = obj

                        
                        # attach expr value: for act Begin only!
                        if mark == "b" and alg_elem["type"] in {"expr"}:
                            values = self.expr_id2values[st_id] if st_id in self.expr_id2values else []
                            # if len(values) <= exec_n:
                            if exec_n <= len(values):
                                value = values[exec_n - 1]
                            else:
                                value = False
                            # print(obj, onto.expr_value, value)
                            make_triple(obj, onto.expr_value, value)
                        
                        # # connect trace begin and 1st act with "next"
                        # if mark == "b" and st_id == entry_stmt_id and index == exec_n == 1:
                        #     obj.is_a.append(onto.correct_act)
                        #     # obj.is_a.append(onto.current_act)
                        #     make_triple(trace_obj, onto.next_act, obj)
                            
                            
                    
                    
    def inject_trace_to_ontology(self, onto, trace, act_classnames=("act",), next_propertyname=None):
        "Writes specified trace to ontology."
        
        additional_classes = [onto[nm] for nm in act_classnames]
        assert all(additional_classes), (additional_classes, act_classnames, onto)
        
        # make trace acts as individuals

        def make_act(iri, onto_class, alg_iri, prop_class=onto.next_act, is_last=False):

            raise "Deprecated !"
            
            # nonlocal trace_acts_list
            iri = uniqualize_iri(onto, iri)
            
            trace_acts_list.append(iri)                 
            # создаём объект
            obj = onto_class(iri)
            # привязываем связанный элемент алгоритма
            make_triple(obj, onto.executes, onto[alg_elem["iri"]])
            
            # формируем последовательный список
            if prop_class and len(trace_acts_list) > 1:
                # привязываем next, если указано
                prev_iri = trace_acts_list[-2]
                make_triple(onto[prev_iri], prop_class, obj)
            elif len(trace_acts_list) == 1:
                # mark as first act of the list
                obj.is_a.append(onto.first_item)
            if is_last:
                # mark as last act of the list
                obj.is_a.append(onto.last_item)
            return obj

        def connect_next_act(obj):
            trace_acts_list.append(obj)                 
            # формируем последовательный список
            if prop_class and len(trace_acts_list) > 1:
                # привязываем next, если указано
                prev_obj = trace_acts_list[-2]
                obj = trace_acts_list[-1]
                # print(">>", prev_obj, obj)
                make_triple(prev_obj, prop_class, obj)
            if trace_acts_list:
              num = len(trace_acts_list)
              make_triple(obj, onto.student_index, num)



            
        def find_act(class_, executes: int, exec_time: int):
            for obj in class_.instances():
                # print(F"{obj}: ")
                if (obj.executes.id == executes and
                   obj.exec_time == exec_time):
                    return obj
            print(f"act not found: ex={executes}, n={exec_time}")

        prop_class = onto[next_propertyname]

        with onto:
            i = 0
            # act_index = 0
            trace_acts_list = []
            for d in trace:
                i += 1
                if "id" in d:
                    id_         = d.get("id")
                    executes    = d.get("executes")
                    # phase: (started|finished|performed)
                    phase       = d.get("phase")  # , "performed"
                    n           = d.get("n", None) or d.get("n_", None)
                    name        = d.get("name", None)  or  d.get("action", None)  # !  name <- action
                    text_line   = d.get("text_line", None)
                    
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
                        # act_index += 1
                        # iri = iri_template % "b"
                        # self.act_iris.append(iri)
                        # obj = make_act(iri, onto.act_begin, alg_elem["iri"], 
                        #     prop_class=onto[next_propertyname], 
                        #     is_last=False)
                        obj = find_act(onto.act_begin, executes, n or 1) 
                        if obj:
                            for class_ in additional_classes:
                                obj.is_a.append(class_)
                            # привязываем нужные свойства
                            make_triple(obj, onto.text_line, text_line)
                            connect_next_act(obj)
                        else:
                          print("  act name:", name)
                        # # НЕ привязываем id (т.к. может повторяться у начал и концов. TO FIX?)
                            # if "value" in d:
                        #     make_triple(obj, onto.expr_value, d["value"])
                    
                    if phase_mark in ("e", "p"):
                        # конец акта
                        # act_index += 1
                        # iri = iri_template % "e"
                        # self.act_iris.append(iri)
                        # obj = make_act(iri, onto.act_end, alg_elem["iri"], 
                        #     prop_class=onto[next_propertyname], 
                        #     is_last=(i==len(self.data["trace"])))
                        obj = find_act(onto.act_end, executes, n or 1) 
                        if obj:
                            for class_ in additional_classes:
                                obj.is_a.append(class_)
                            # привязываем нужные свойства
                            make_triple(obj, onto.text_line, text_line)
                            connect_next_act(obj)
                        
            # iri_list_key = act_classnames[0] + "_iri_list"
            # self.data[iri_list_key] = trace_acts_list
        
        
    def test_with_ontology_results(self, onto):
        pass
    
    

def init_persistent_structure(onto):
        # types.new_class(temp_name, (domain >> range_, ))  # , Property
        
    with onto:    
        # Статические определения
        
        # новое свойство id
        if not onto["id"]:
            id_prop = types.new_class("id", (Thing >> int, FunctionalProperty, ))
        # ->
        class act(Thing): pass  # Thing - временно?
        # -->
        class act_begin(act): pass
        # --->
        class trace(act_begin): pass
        # -->
        class act_end(act): pass
        # # -->
        # class student_act(act): pass
        # -->
        class correct_act(act): pass
        # # -->
        # class current_act(act): pass
        
        # ->
        class sequence(Thing): pass
        
        # признак first
        class first_item(Thing, ): pass
        # признак last
        class last_item(Thing, ): pass

        # ->
        class loop(Thing): pass
        
        if loop:  # hide a block under code folding
            # classes that regulate a loop execution start (which act should be first)
            #
            # start with cond
            preconditional_loop = types.new_class("pre_conditional_loop", (loop,))
            # start with body
            postconditional_loop = types.new_class("post_conditional_loop", (loop,))
            # start with init
            loop_with_initialization = types.new_class("loop_with_initialization", (loop,))
            
            AllDisjoint([preconditional_loop, postconditional_loop, loop_with_initialization])
            
            # classes that regulate the use of condition in a loop
            #
            # normal condition effect (false->stop, true->start a body) like in while, do-while, for loop types
            conditional_loop = types.new_class("conditional_loop", (loop,))
            # inverse condition effect (false->start a body, true->stop) like in do-until loop
            inverse_conditional_loop = types.new_class("inverse_conditional_loop", (loop,))
            # no condition at all: infinite loop like while(true){...}. The only act executed is the loop body.
            unconditional_loop = types.new_class("unconditional_loop", (loop, postconditional_loop))  # "postconditional_loop" parent here is a lifehack: the loop starts with body just like "do-while", "postconditional_loop" causes the body to be first act whthin a loop act.
            
            AllDisjoint([conditional_loop, inverse_conditional_loop, unconditional_loop])
            
            # classes that regulate the use of "update" step in a for-like loop (both subclasses of "loop_with_initialization" as that loop have "update" step too)
            #
            # update first, then the body, like in foreach loop type
            pre_update_loop = types.new_class("pre_update_loop", (loop_with_initialization,))
            # body first, then the update, like in for(;;) loop type
            post_update_loop = types.new_class("post_update_loop", (loop_with_initialization,))
            
            AllDisjoint([pre_update_loop, post_update_loop])
            
            
            # classes that indicate whether condition and body follow each other instantly or not (note that: these classes are not disjointed; these classes are to be inferred from another defined features via equivalent_to definition so no direct inheritance required for known loops)
            class _body_then_cond(loop):
                equivalent_to = [inverse_conditional_loop | (conditional_loop & (Not(post_update_loop)))]
            class _cond_then_body(loop):
                equivalent_to = [conditional_loop & (Not(pre_update_loop))]
                
            # classes that define well-known loops as subclasses of the above defined loop-feature classes. These classes are to be used publicly
            class while_loop(conditional_loop, preconditional_loop): pass
            
            # class do_while_loop(conditional_loop, postconditional_loop): pass
            types.new_class("do_while_loop", (conditional_loop, postconditional_loop,))
            
            # class do_until_loop(inverse_conditional_loop, postconditional_loop): pass
            types.new_class("do_until_loop", (inverse_conditional_loop, postconditional_loop,))
            
            class for_loop(conditional_loop, post_update_loop): pass
            class foreach_loop(conditional_loop, pre_update_loop): pass
            class infinite_loop(loop):  
                equivalent_to = [unconditional_loop]  # reduce an inheritance level: use "equivalent_to" instead of inheritance
              
        

        # make algorithm elements classes
        for class_name in [
            "func", "alternative", "alt_branch", "expr", 
        ]:
            types.new_class(class_name, (Thing,))

        for class_name in [
            "if", "else-if", "else", 
        ]:
            types.new_class(class_name, (onto.alt_branch,))

        # make algorithm elements properties
        for prop_name in ("body", "branches_item", "cond", ):
            if not onto[prop_name]:
                types.new_class(prop_name, (Thing >> Thing,))
           
        # новое свойство executes
        prop_executes = types.new_class("executes", (Thing >> Thing, FunctionalProperty, ))

        # новое свойство expr_value
        prop_expr_value = types.new_class("expr_value", (DataProperty, FunctionalProperty, ))

        # новое свойство next
        types.new_class("next", (Thing >> Thing, ))
        types.new_class("next_act", (correct_act >> correct_act, FunctionalProperty, InverseFunctionalProperty))
        types.new_class("student_next", (Thing >> Thing, ))

        # новое свойство student_next
        prop_student_next = types.new_class("student_next", (act >> act, ))

        # новое свойство next_sibling -- связывает акты, соседние по номеру раза выполнения (причём, начальные и конечные акты - раздельно)
        next_sibling = types.new_class("next_sibling", (Thing >> Thing, ))

        # новое свойство before
        # prop_before = types.new_class("before", (Thing >> Thing, TransitiveProperty))

        # новое свойство in_trace
        prop_in_trace = types.new_class("in_trace", (act >> trace, ))
        
        # свойство index
        types.new_class("index", (Thing >> int, FunctionalProperty, ))
        types.new_class("student_index", (Thing >> int, FunctionalProperty, ))

        # новое свойство exec_time
        prop_exec_time = types.new_class("exec_time", (Thing >> int, FunctionalProperty, ))
        # # новое свойство depth
        # prop_depth = types.new_class("depth", (Thing >> int, FunctionalProperty, ))
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
        
        # новое свойство corresponding_end
        class corresponding_end(act_begin >> act_end, ): pass
        class student_corresponding_end(act_begin >> act_end, ): pass
    
        # # новое свойство target - цель подсчёта числа связей
        # class target(Counter >> Thing, AsymmetricProperty): pass
    
        # новое свойство parent_of
        # class parent_of(act_begin >> act, InverseFunctionalProperty): pass
        class parent_of(Thing >> Thing, InverseFunctionalProperty): pass
        class student_parent_of(Thing >> Thing, InverseFunctionalProperty): pass

        # # новое свойство contains_act < contains_child
        # class contains_child(Thing >> Thing, ): pass
        # class contains_act(act_begin >> act, contains_child): pass
        
       # объекты, спровоцировавшие ошибку
        if not onto["Erroneous"]:
            Erroneous = types.new_class("Erroneous", (Thing,))
            
            # make Erroneous subclasses
            for class_name in [
                # Sequence mistakes ...
                "CorrespondingEndMismatched",
                "CorrespondingEndPerformedDifferentTime",
                "WrongExecTime",
                # "AfterTraceEnd",
                # "DuplicateActInSequence",
                "WrongExecTime",
                "WrongContext",
                "ExtraAct",
                ("DuplicateOfAct", ["ExtraAct"]), # act was moved somewhere
                "MissingAct",
                "TooEarly", # right after missing acts
                ("DisplacedAct", ["TooEarly","ExtraAct","MissingAct"]),
                # Alternatives mistakes ...
                "NoFirstCondition",
                ("BranchOfFalseCondition", ["ExtraAct"]),
                ("ConditionAfterBranch", ["ExtraAct"]),
                ("AnotherExtraBranch", ["ExtraAct"]),
                ("NoBranchWhenConditionIsTrue", ["MissingAct"]),
                "AllFalseNoElse",
                "NoNextCondition",
                "AllFalseNoEnd",
            ]:
                if isinstance(class_name, str):
                    types.new_class(class_name, (Erroneous,))
                elif isinstance(class_name, tuple):
                    class_name, base_names = class_name
                    bases = tuple(onto[base_name] if type(base_name) is str else base_name for base_name in base_names)
                    # print(bases)
                    types.new_class(class_name, bases)
            
        for prop_name in ("cause", "cause2", "should_be", "should_be_before", "context_should_be"):
            if not onto[prop_name]:
                types.new_class(prop_name, (onto["Erroneous"] >> Thing,))

        # make correct_act subclasses
        for class_name in [
            "FunctionBegin",
            "FunctionEnd",
            "FunctionBodyBegin",
            "GlobalCodeBegin",
            "SequenceBegin",
            "SequenceNext",
            "SequenceEnd",
            "StmtEnd",
            "ExprEnd",
            # "DebugObj",
            "AltBegin",  # 1st condition
            "NextAltCondition",
            "AltBranchBegin",
            "AltElseBranchBegin",
            "AltEndAfterBranch",
            "AltEndAllFalse",
            "PreCondLoopBegin",
        ]:
            # types.new_class(class_name, (Thing,))
            types.new_class(class_name, (correct_act,))
            
        # for prop_name in ("reason", ):  # for correct acts !
        #     if not onto[prop_name]:
        #         types.new_class(prop_name, (correct_act >> Thing,))


def load_swrl_rules(onto, rules_dict, rules_filter=None):
    """ rules_filter: None or callable hat receives name of rule and returns boolean """
    
    with onto:
        for k in rules_dict:
            if rules_filter and not rules_filter(k):
                print("Ignoring SWRL rule:", k)
                continue
                
            rule = rules_dict[k]
            try:
                Imp(k).set_as_rule(rule)
            except Exception as e:
                print("Error in SWRL rule: \t", k)
                print(e)
                raise e
            
    return onto
        

def extact_mistakes(onto, as_objects=False) -> dict:
    """Searches for instances of trace_error class and constructs a dict of the following form:
        "<error_instance1_name>": {
            "classes": ["list", "of", "class", "names", ...],
            "<property1_name>": ["list", "of", "property", "values", ...],
            "<property2_name>": [onto.iri_1, "reference", "can present", "too", ...],
            ...
        },
        "<error_instance2_name>": {},
        ... 
    
     """
    error_classes = onto.Erroneous.descendants()  # a set of the descendant Classes (including self)

    properties_to_extract = ("name", onto.cause, onto.should_be, onto.should_be_before, onto.context_should_be, onto.text_line, )
    mistakes = {}

    # The .instances() class method can be used to iterate through all Instances of a Class (including its subclasses). It returns a generator.
    for inst in onto.Erroneous.instances():
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
                        
            d = mistakes.get(inst.name, {})
            d[prop_name] = values
            mistakes[inst.name] = d
        classes = {class_ for class_ in inst.is_a if class_ in error_classes}
        base_classes = set([sup for cl in classes for sup in cl.is_a])
        # print(classes, "-" ,base_classes)
        classes -= base_classes  # remove less precise bases
        mistakes[inst.name]["classes"] = [class_.name for class_ in classes]
    
    return mistakes


def process_algtraces(trace_data_list, debug_rdf_fpath=None, verbose=1, 
                      mistakes_as_objects=False, extra_act_entries=0, 
                      rules_filter=None, reasoning="stardog", on_done=None) -> "onto, mistakes_list":
    """Write number of algorithm - trace pair to an ontology, perform extended reasoning and then extract and return the mistakes found.
      reasoning: None or "stardog" or "pellet"
    """
    
    global ONTOLOGY_maxID
    
    # создание онтологии
    my_iri = ('http://vstu.ru/poas/ctrl_structs_2020-05_v%d' % ONTOLOGY_maxID)
    ONTOLOGY_maxID += 1
    onto = get_ontology(my_iri)

    with onto:
        # каркас онтологии
        init_persistent_structure(onto)
        
    # наполняем онтологию с нуля сущностями с теми именами, которые найдём в загруженных json-словарях
    for tr_data in trace_data_list:
        tt = TraceTester(tr_data)
        tt.inject_to_ontology(onto, extra_act_entries=extra_act_entries)

    # обёртка для расширенного логического вывода:
     # при создании наполняет базовую онтологию вспомогательными сущностями
    # wr_onto = AugmentingOntology(onto)
    

    # после наложения обёртки можно добавлять SWRL-правила
    if True:
        from ctrlstrct_swrl import RULES_DICT as swrl_rules_dict
        load_swrl_rules(onto, swrl_rules_dict, rules_filter=rules_filter)
    
    if debug_rdf_fpath:
        onto.save(file=debug_rdf_fpath, format='rdfxml')
        print("Saved RDF file: {} !".format(debug_rdf_fpath))

    if reasoning == "stardog":
        seconds = sync_stardog(debug_rdf_fpath, ontology_prefix=my_iri + "#")
        
    # exit()
        
    if reasoning == "pellet":
        # if not verbose:
        #     print("Extended reasoning started ...",)

        # # расширенное обновление онтологии и сохранение с новыми фактами
        # success,n_runs = wr_onto.sync(runs_limit=5, verbose=verbose)
        
        with onto:
            # запуск Pellet
            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=0)
        
        seconds = -2

        # if not verbose:
        #     print("Extended reasoning finished.", f"Success: {success}, Pellet run times: {n_runs}")

        if debug_rdf_fpath:
            onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
            print(f"Saved RDF file: {debug_rdf_fpath}_ext.rdf !")
            
    if on_done:
        on_done(seconds)
        
    # return onto, []  ### Debug exit
    # exit()
        
    mistakes = extact_mistakes(onto, as_objects=mistakes_as_objects)
    
    return onto, list(mistakes.values())


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


from pprint import pprint
from stardog_credentails import *


def sync_stardog(ontology_path, save_as_path=None, ontology_prefix=None):
  # DEBUG
  # return
  
  import stardog
  
  # conn_details = {
  #   'endpoint': 'http://localhost:5820',
  #   'username': 'admin',
  #   'password': 'admin'
  # }
  # dbname = "ctrlstrct_db"
  # # graphname = "urn:graph_data"
  # # schema_graphname = "urn:graph_schema"
  
  ontology_file = stardog.content.File(ontology_path)
  
  schema_file = stardog.content.File("stgd_schema.ttl")
  
  save_as = save_as_path or (ontology_path + "_ext")

  try:
    with stardog.Admin(**conn_details) as admin:
      print("creating database ...")
      # print(*(d.name for d in admin.databases()))
      if dbname not in (d.name for d in admin.databases()):
        db = admin.new_database(dbname)
      else:
        db = admin.database(dbname)

      with stardog.Connection(dbname, **conn_details) as conn:
        conn.begin()  # reasoning=True)
        conn.clear()
        print("uploading database ...")
        conn.add(ontology_file)  ###, graph_uri=graphname)
        # print("uploading schema ...")
        # conn.add(schema_file)  ###, graph_uri=schema_graphname)
        conn.commit()
        # print("upload OK")
        
        if 0:  # !!!
            # BASE <http://vstu.ru/poas/ctrl_structs_2020-05_v1#>;
              
            print("running query ...")
            # OK!
            # results = conn.select('''SELECT * WHERE {?a  rdf:type <http://vstu.ru/poas/ctrl_structs_2020-05_v1#current_act> }''', reasoning=True)
            results = conn.select('''PREFIX onto: <http://vstu.ru/poas/ctrl_structs_2020-05_v1#>
              
              SELECT * WHERE {?a a onto:correct_act }''', reasoning=True)
            pprint(results)

            print("downloading database ...")
            contents = conn.export()

            # запись в файл
            ext = '.ttl'
            if not save_as.endswith(ext):
                save_as += ext
            print("writing to file: " + save_as[-50:])
            with open(save_as, 'wb') as f:
                f.write(contents)
                
        print("saved.")
        
        # run query defined in another file ...
        from stardog_test import main as run_stardog_query
        
        seconds = run_stardog_query(ontology_prefix)
        return seconds
  
  except Exception as e:
      print(e)
      return -1
  
  finally:
      pass
      # db.drop()
      # print("dropped the db.")
      # return -1
      


            
if __name__ == '__main__':
    
    print("Please run *_test.py script instead!")
    exit()
    
