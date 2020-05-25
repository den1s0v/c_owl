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
        
        def next_cond_value(self):
            i,_ = self.last_cond_tuple
            v = next(self.condition_value_generator)
            v = bool(v)
            self.last_cond_tuple = (i+1, v)
            return v
            
        
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
                    branch.accept(self)
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
                value = self.next_cond_value()
                phase = "performed"
                ith = 1 + len([x for x in find_by_keyval_in("name", node["name"], result) if x["phase"] == phase])
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
              "n": None,
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
              "n": None,
              # "text_line": None,
              # "comment": None,
        })
        
        # print(self.data["correct_trace"])
        # exit()
        

        
    def inject_to_ontology(self, onto):
        
        self.inject_algorithm_to_ontology(onto)
        
        self.inject_trace_to_ontology(onto, self.data["trace"], ("student_act",), "next")
        self.inject_trace_to_ontology(onto, self.data["correct_trace"], ("correct_act",), "correct_next")
        
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
                    
                    # uniqualize individual's name
                    n = 2; orig_iri = iri
                    while onto[iri]:  # пока есть объект с таким именем
                        # модифицировать имя
                        iri = orig_iri + ("_%d" % n); n += 1
                        
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

        
    def inject_trace_to_ontology(self, onto, trace, act_classnames=("act",), next_propertyname=None):
        "Writes specified trace to ontology."
        
        additional_classes = [onto[nm] for nm in act_classnames]
        assert all(additional_classes), (additional_classes, act_classnames)
        
        # make trace acts as individuals

        def make_act(iri, onto_class, alg_iri, prop_class=onto.next, is_last=False):
            # nonlocal trace_acts_iri_list
            
            # uniqualize individual's name
            n = 2; orig_iri = iri
            while onto[iri]:  # пока есть объект с таким именем
                # модифицировать имя
                iri = orig_iri + ("_%d" % n); n += 1
            
            trace_acts_iri_list.append(iri)                 
            # создаём объект
            obj = onto_class(iri)
            # привязываем связанный элемент алгоритма
            make_triple(obj, onto.executes, onto[alg_elem["iri"]])
            
            # формируем последовательный список
            if prop_class and len(trace_acts_iri_list) > 1:
                # привязываем next, если указано
                prev_iri = trace_acts_iri_list[-2]
                make_triple(onto[prev_iri], prop_class, obj)
            elif len(trace_acts_iri_list) == 1:
                # mark as first act of the list
                obj.is_a.append(onto.first_item)
            if is_last:
                # mark as last act of the list
                obj.is_a.append(onto.last_item)
            return obj

        with onto:
            i = 0
            trace_acts_iri_list = []
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


                    iri_template = "{}%s_{}{}".format(text_line or id_, clean_name, number_mark)
                    
                    if phase_mark in ("b", "p"):
                        # начало акта
                        iri = iri_template % "b"
                        # d["iris"] = d.get("iris", ()) + (iri, )  # save iri back to dict
                        self.act_iris.append(iri)
                        obj = make_act(iri, onto.act_begin, alg_elem["iri"], 
                            prop_class=onto[next_propertyname], 
                            is_last=False)
                        for class_ in additional_classes:
                            obj.is_a.append(class_)
                        # НЕ привязываем id (т.к. может повторяться у начал и концов. TO FIX?)
                        # привязываем нужные свойства
                        make_triple(obj, onto.text_line, text_line)
                    
                    if phase_mark in ("e", "p"):
                        # конец акта
                        iri = iri_template % "e"
                        # d["iris"] = d.get("iris", ()) + (iri, )  # save iri back to dict
                        self.act_iris.append(iri)
                        obj = make_act(iri, onto.act_end, alg_elem["iri"], 
                            prop_class=onto[next_propertyname], 
                            is_last=(i==len(self.data["trace"])))
                        for class_ in additional_classes:
                            obj.is_a.append(class_)
                        # привязываем нужные свойства
                        make_triple(obj, onto.text_line, text_line)
                        
            iri_list_key = act_classnames[0] + "_iri_list"
            self.data[iri_list_key] = trace_acts_iri_list
        
        
    def test_with_ontology_results(self, onto):
        pass
    
    

def make_up_ontology(alg_json_str, trace_json_str, iri=None):
    """ -> Owlready2 ontology object """
    
    global ONTOLOGY_maxID

    def catch_obj(x):
        nonlocal objects
        objects.append(x)
        return x

    if isinstance(alg_json_str, str) and isinstance(trace_json_str, str):
        objects = []
        alg = json.loads(alg_json_str, object_hook=catch_obj)
        alg_objects = objects

        # objects = []
        tr = json.loads(trace_json_str) # , object_hook=catch_obj)
        # tr_objects = objects
        
        # делаем иерархический список плоским без потери порядка
        tr = list(plain_list(tr))
    
    elif isinstance(alg_json_str, dict) and isinstance(trace_json_str, list):
        alg = alg_json_str
        tr = trace_json_str
        
        alg_objects = list(find_by_type(alg))
        
    else:
        raise TypeError(f"alg & trace msut be either JSON strings, either dict and list, but got: {type(alg_json_str)}, {type(trace_json_str)}")
        

    id2obj = {}  # индекс всех объектов АЛГОРИТМА для быстрого поиска по id
    for d in alg_objects:
        if "id" in d:
            id2obj[ d["id"] ] = d
            
    my_iri = iri or ('http://vstu.ru/poas/ctrl_structs_2020-05_v%d' % ONTOLOGY_maxID)
    ONTOLOGY_maxID += 1
    onto = get_ontology(my_iri)

    with onto:
        # наполняем онтологию с нуля сущностями с теми именами, которые найдём в загруженных json-словарях
        
        init_persistent_structure(onto)
        
        id_prop = onto["id"]
        first_item = onto["first_item"]
        last_item = onto["last_item"]
        act = onto["act"]
        act_begin = onto["act_begin"]
        act_end = onto["act_end"]
        prop_executes = onto["executes"]
        prop_next = onto["next"]
        prop_text_line = onto["text_line"]
        # prop_executes = onto["executes"]

        
        # создадим классы алгоритма и объекты в них
        for d in alg_objects:
            if "id" in d:
                id_     = d.get("id")
                type_   = d.get("type")
                name    = d.get("name", "")
                
                assert type_, "Error in agrorithm object: "+str(d)
                
                id_         = int(id_)
                # clean_name    = re.sub(r"\s+", "", name)
                clean_name  = prepare_name(name)
                
                class_ = onto[type_]
                if not class_:
                    # создаём в онтологии новый класс
                    class_ = types.new_class(type_, (Thing, ))
                    
                # формируем имя экземпляра в онтологии
                iri = "{}_{}".format(id_, clean_name)
                # сохраняем назад в наш словарь (для привязки к актам трассы) 
                d["iri"] = iri
                # создаём объект
                obj = class_(iri)
                # привязываем id
                make_triple(obj, id_prop, id_)
                # (имя не привязываем.)
            # else: raise "no id!"
                
        # наладим связи между элементами алгоритма
        def link_objects(iri_subj, prop_name, iri_obj, prop_superclasses=()):
            prop = onto[prop_name]
            if not prop:
                # новое свойство по заданному имени
                prop = types.new_class(prop_name, (Thing >> Thing, *prop_superclasses))
            # связываем объекты свойством
            make_triple(onto[iri_subj], prop, onto[iri_obj])
            
        
        for d in alg_objects:
            if "id" in d:
                for k in d:  # ищем объекты среди полей словаря
                    v = d[k]
                    if isinstance(v, dict) and "id" in v and "iri" in v:
                        link_objects(d["iri"], k, v["iri"], (onto.parent_of,) )
                    elif isinstance(v, list):
                        # print("check out list", k, "...")
                        # сделаем список, если в нём нормальные "наши" объекты
                        subobject_iri_list = [subv["iri"] for subv in v if isinstance(subv, dict) and "id" in subv and "iri" in subv]
                        if not subobject_iri_list:
                            continue
                            
                        iri = d["iri"]
                        
                        # всякий список действий должен быть оформлен как sequence с полем body - списком.
                        if k == "body":
                            # делаем объект последовательностью (нужно для тел циклов, веток, функций)
                            onto[iri].is_a.append( onto.sequence )
                        # else:  # это нормально для других списков
                        #     print("Warning: key of sequence is '%s' (consider using 'body')" % k)
                        
                        
                        subelem__prop_name = k+"_item"
                        for i, subiri in enumerate(subobject_iri_list):
                            # главная связь
                            link_objects(iri, subelem__prop_name, subiri, (onto.parent_of,) )
                            # последовательность
                            if i >= 1:
                                prev_iri = subobject_iri_list[i-1]
                                link_objects(prev_iri, "next", subiri)
                            # первый / последний
                            if i == 0:
                                # mark as first elem of the list
                                onto[subiri].is_a.append(first_item)
                            if i == len(subobject_iri_list)-1:
                                # mark as last act of the list
                                onto[subiri].is_a.append(last_item)
                            
                    
        
        # создадим классы трассы и объекты в них

        def make_act(iri, onto_class, alg_iri, is_last=False):
            nonlocal trace_acts_iri_list
            n = 2; orig_iri = iri
            while onto[iri]:  # пока есть объект с таким именем
                # модифицировать имя
                iri = orig_iri + ("_%d" % n); n += 1
            
            trace_acts_iri_list.append(iri)                 
            # создаём объект
            obj = onto_class(iri)
            # привязываем связанный элемент алгоритма
            make_triple(obj, prop_executes, onto[alg_elem["iri"]])
            
            # формируем последовательный список
            if len(trace_acts_iri_list) > 1:
                # привязываем next
                prev_iri = trace_acts_iri_list[-2]
                make_triple(onto[prev_iri], prop_next, obj)
            elif len(trace_acts_iri_list) == 1:
                # mark as first act of the list
                obj.is_a.append(first_item)
            if is_last:
                # mark as last act of the list
                obj.is_a.append(last_item)
            return obj

        i = 0
        trace_acts_iri_list = []
        for d in tr:
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
                # clean_name    = re.sub(r"\s+", "", name)
                clean_name  = prepare_name(name)
                phase_mark  = {"started":"b", "finished":"e", "performed":"p",}[phase]
                n           = n and int(n)  # convert if not None
                number_mark = "" if not n else ("_n%d" % n)
                
                # находим связанный элемент алгоритма
                assert executes in id2obj, (id2obj, d)
                alg_elem = id2obj[executes]


                iri_template = "{}%s_{}{}".format(text_line or id_, clean_name, number_mark)
                
                if phase_mark in ("b", "p"):
                    # начало акта
                    iri = iri_template % "b"
                    # print("iri: ", iri)
                    obj = make_act(iri, act_begin, alg_elem["iri"], False)
                    # НЕ привязываем id (т.к. может повторяться у начал и концов. TO FIX?)
                    # make_triple(obj, id_prop, id_)
                    # привязываем нужные свойства
                    make_triple(obj, prop_text_line, text_line)
                
                if phase_mark in ("e", "p"):
                    # конец акта
                    iri = iri_template % "e"
                    obj = make_act(iri, act_end, alg_elem["iri"], i==len(tr))
                    # привязываем нужные свойства
                    make_triple(obj, prop_text_line, text_line)

                
    return onto

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
        # -->
        class act_end(act): pass
        # -->
        class student_act(act): pass
        # -->
        class correct_act(act): pass
        
        # ->
        class sequence(Thing): pass
        
        # признак first
        class first_item(Thing, ): pass
        # признак last
        class last_item(Thing, ): pass

        # создаём новый class - для создания n-арной ассоциации для подсчёта числа связей
        if not onto["Counter"]:
            class Counter(Thing): pass

        # новое свойство executes
        prop_executes = types.new_class("executes", (Thing >> Thing, FunctionalProperty, ))
        # новое свойство next
        prop_next = types.new_class("next", (Thing >> Thing, FunctionalProperty, ))
        # новое свойство correct_next
        correct_next = types.new_class("correct_next", (Thing >> Thing, FunctionalProperty, ))
        # новое свойство before
        prop_before = types.new_class("before", (Thing >> Thing, ))
        
        # новое свойство depth
        prop_depth = types.new_class("depth", (Thing >> int, FunctionalProperty, ))
        # новое свойство text_line
        prop_text_line = types.new_class("text_line", (Thing >> int, FunctionalProperty, ))
        # # новое свойство same_level
        # prop_same_level = types.new_class("same_level", (Thing >> Thing, SymmetricProperty))
        # # новое свойство child_level
        # prop_child_level = types.new_class("child_level", (Thing >> Thing, SymmetricProperty))
        
        # новое свойство corresponding_end
        class corresponding_end(act_begin >> act_end, FunctionalProperty, InverseFunctionalProperty): pass
    
        # новое свойство target - цель подсчёта числа связей
        class target(Counter >> Thing, AsymmetricProperty): pass
    
        # новое свойство parent_of
        # class parent_of(act_begin >> act, InverseFunctionalProperty): pass
        class parent_of(Thing >> Thing, InverseFunctionalProperty): pass
        # новое свойство contains_act < contains_child
        class contains_child(Thing >> Thing, ): pass
        class contains_act(act_begin >> act, contains_child): pass
        
        # -->
        # Создать класс ошибки
        class trace_error(Thing): pass

        if not onto["message"]:
            message_prop = types.new_class("message", (trace_error >> str, FunctionalProperty, ))
        # объект-агрумент, на который делается ссылка
        for prop_name in ("arg", ):
            if not onto[prop_name]:
                types.new_class(prop_name, (Thing >> Thing,))
           
       # объекты, спровоцировавшие ошибку
        if not onto["Erroneous"]:
            types.new_class("Erroneous", (Thing,))
        for prop_name in ("cause", ):
            if not onto[prop_name]:
                types.new_class(prop_name, (Thing >> onto["Erroneous"],))


def load_swrl_rules(onto, rules_dict):
    
    with onto:
        for k in rules_dict:
            rule = rules_dict[k]
            try:
                Imp(k).set_as_rule(rule)
            except Exception as e:
                print("Error in SWRL rule: \t", k)
                print(e)
                raise e
            
    return onto
        

def extact_mistakes(onto, as_objects=False) -> dict:

    properties_to_extract = ("name", onto.message, onto.arg, onto.cause, )
    mistakes = {}

    for inst in onto.trace_error.instances():
        for prop in properties_to_extract:
            values = []
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
    
    return mistakes


def process_algtr(alg_json, trace_json, debug_rdf_fpath=None, verbose=1, mistakes_as_objects=False) -> "onto, mistakes_list":
    # каркас онтологии, наполненный минимальными фактами об алгоритме и трассе
    onto = make_up_ontology(alg_json, trace_json)

    # обёртка для расширенного логического вывода:
     # при создании наполняет базовую онтологию вспомогательными сущностями
    wr_onto = AugmentingOntology(onto)
    

    # после наложения обёртки можно добавлять SWRL-правила
    from ctrlstrct_swrl import RULES_DICT as swrl_rules_dict
    load_swrl_rules(onto, swrl_rules_dict)
    
    if debug_rdf_fpath:
        onto.save(file=debug_rdf_fpath, format='rdfxml')
        # print("Saved RDF file: {} !".format(ontology_file))
        
    if not verbose:
        print("Extended reasoning started ...",)

    # расширенное обновление онтологии и сохранение с новыми фактами
    success,n_runs = wr_onto.sync(runs_limit=5, verbose=verbose)

    if not verbose:
        print("Extended reasoning finished.", f"Success: {success}, Pellet run times: {n_runs}")

    if debug_rdf_fpath:
        onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
        # print("Saved RDF file: {} !".format(ontology_file))
        
    mistakes = extact_mistakes(onto, as_objects=mistakes_as_objects)
    
    return onto, list(mistakes.values())


def process_algtraces(trace_data_list, debug_rdf_fpath=None, verbose=1, mistakes_as_objects=False) -> "onto, mistakes_list":
    """Write number of algorithm - trace pair to an ontology, perform extended reasoning and then extract and return the mistakes found."""
    
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
        tt.inject_to_ontology(onto)

    # обёртка для расширенного логического вывода:
     # при создании наполняет базовую онтологию вспомогательными сущностями
    wr_onto = AugmentingOntology(onto)
    

    # после наложения обёртки можно добавлять SWRL-правила
    from ctrlstrct_swrl import RULES_DICT as swrl_rules_dict
    load_swrl_rules(onto, swrl_rules_dict)
    
    if debug_rdf_fpath:
        onto.save(file=debug_rdf_fpath, format='rdfxml')
        # print("Saved RDF file: {} !".format(ontology_file))
        
    if not verbose:
        print("Extended reasoning started ...",)

    # расширенное обновление онтологии и сохранение с новыми фактами
    success,n_runs = wr_onto.sync(runs_limit=5, verbose=verbose)

    if not verbose:
        print("Extended reasoning finished.", f"Success: {success}, Pellet run times: {n_runs}")

    if debug_rdf_fpath:
        onto.save(file=debug_rdf_fpath+"_ext.rdf", format='rdfxml')
        # print("Saved RDF file: {} !".format(ontology_file))
        
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

            
if __name__ == '__main__':
    # -a
    alg_filepath = r"c:\D\Нинь\учёба\10s\Quiz\Дистракторы\tr-gen\alg_out_2.json"
    # -t
    tr_filepath  = r"c:\D\Нинь\учёба\10s\Quiz\Дистракторы\tr-gen\tr_out_err.json"
    # -r
    rdf_filename = "algtr_simple.rdf"
    # -o , -e
    mistakes_out_filename = "algtr_mistakes.json"

    with open(alg_filepath, encoding="utf8") as f:
        alg = f.read()

    with open(tr_filepath, encoding="utf8") as f:
        tr = f.read()

    # Запуск !  
    onto, mistakes = process_algtr(alg, tr, verbose=0)
    
    with open(mistakes_out_filename, "w", encoding="utf8") as f:
        json.dump(mistakes, f, indent=2)
        
    print("Saved mistakes ({}) as json: {}".format(len(mistakes), mistakes_out_filename))
    

    ontology_file2 = rdf_filename.replace(".", "_ext.")
    onto.save(file=ontology_file2, format='rdfxml')
    print("Saved RDF file: {} !".format(ontology_file2))

