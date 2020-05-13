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


ONTOLOGY_maxID = 1

def prepare_name(s):
    return slugify(s) or s


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
        # наполняем онтологию с нуля сущностями с теми именами, который найдём в загруженных json-словарях
        
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
        
        # ->
        class sequence(Thing): pass
        
        # признак first
        class first_item(Thing, ): pass
        # признак last
        class last_item(Thing, ): pass

        # новое свойство executes
        prop_executes = types.new_class("executes", (Thing >> Thing, FunctionalProperty, ))
        # новое свойство next
        prop_next = types.new_class("next", (Thing >> Thing, FunctionalProperty, ))
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
    
        # новое свойство parent_of
        # class parent_of(act_begin >> act, InverseFunctionalProperty): pass
        class parent_of(Thing >> Thing, InverseFunctionalProperty): pass
        # новое свойство contains_act < contains_child
        class contains_child(Thing >> Thing, ): pass
        class contains_act(act_begin >> act, contains_child): pass
    

def load_swrl_rules(onto, rules_dict):
    
    with onto:
    
        # -->
        # Создать класс ошибки
        class trace_error(Thing): pass
        
        if not onto["message"]:
            message_prop = types.new_class("message", (trace_error >> str, FunctionalProperty, ))
        # объекты, спровоцировавшие ошибку
        for prop_name in ("arg", ):
            if not onto[prop_name]:
                types.new_class(prop_name, (Thing >> Thing,))
           
            rule = rules_dict[k]
            try:
                Imp().set_as_rule(rule)
            except Exception as e:
                print("Error in SWRL rule: \t", k)
                print(e)
                raise e
            
    return onto
        

def extact_mistakes(onto, as_objects=False) -> dict:
    properties_to_extract = ("name", onto.message, onto.arg, )

    mistakes = {}

    for inst in onto.trace_error.instances():
        for prop in properties_to_extract:
            values = []
            if isinstance(prop, str):
                prop_name = prop
                values.append(getattr(inst, prop))
            else:
                prop_name = prop.name
                for o,s in prop.get_relations():
                    if o == inst:
                        if not as_objects:
                            s = s.name if hasattr(s, "name") else s
                        values.append(s)
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
        print("Extended reasoning finished.", "Success:", str(success) + ","," Pellet run times:", n_runs)

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

def find_by_type(dict_or_list, types=(dict,)):
    "plain list of dicts or objects of specified type"
    if isinstance(dict_or_list, types):
        yield dict_or_list
    if isinstance(dict_or_list, dict):
        for v in dict_or_list.values():
            yield from find_by_type(v, types)
    elif isinstance(dict_or_list, (list, tuple, set)):
        for d in dict_or_list:
            yield from find_by_type(d, types)

            
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

