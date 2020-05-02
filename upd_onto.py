"""

Auto-augmenting ontology (wrapper for OwlReadу2 ontology).
Enables support for changing ontology via SWRL by iteratively ru reasoner and make changes directly in the ontology.


# ========================== #

Используем простые property для выполнения модификации онтологии

* Удаление связи prop1

UNLINK_prop1(?x, ?y)


* Добавление связи prop1  (позже)

LINK_prop1(?x, ?y)


* Удаление объекта (экземпляра) ?x

DESTROY_INSTANCE(?x)   # назначение объекту спец. класса DESTROY_INSTANCE


* Добавление объектов (экземпляров) класса Class1

CREATE(INSTANCE , "Class1{prop1=value1; prop2=value2}")  # назначение свойства глобальному спец. экземпляру со строкой

# если prop - DataProperty, то оставляем так
# если prop - ObjectProperty, то в условной части вытаскиваем id (поле-идентификатор) объекта и заменяем value на id.


"""

import re
from owlready2 import *


class AugmentingOntology(object):
	"""docstring for AugmentingOntology"""
	def __init__(self, src_onto, no_init=False):
		super(AugmentingOntology, self).__init__()
		self.onto = src_onto

		if not no_init:
			self.init()

	def init(self):
		_patch_ontology(self.onto)



""" How to cause ontology agmentation: Examples

# create on ontology
onto1 = get_ontology("my-test-onto")

# ...

# mark to remove an instance ("a1" here)
onto1["a1"].is_a.append(onto1.DESTROY_INSTANCE)

# mark to create new ClsA instance with two properties assigned (note passing other instances as ontology name strings)
create_instance(onto1, "ClsA{hasProp=instB; hasFuncProp=instA}")


# mark to assert a relation
with onto1:
    make_triple(a, onto1.LINK_hasProp, b)

# mark to retract a relation
with onto1:
    make_triple(a, onto1.UNLINK_hasProp, b)


# ...

# run automatic augmentation which removing all the tool artifacts
augment_ontology(onto1)


"""


# injected property prefices
_special_prefixes =  [
	"LINK_", "UNLINK_",  # prefixes for properties replicated existiong properties
	"CREATE", "IRI"  # full names of properties
]



def _patch_ontology(onto, ignore_properties=None):
    """
    Run once after an ontology init.

    ignore_properties=None : TODO (skip some properties)
    """

    with onto:
        # создаём новые property
        for p in onto.properties():
            name = p.name
            if any(name.startswith(px) for px in _special_prefixes):
                continue

            domain = p.domain[0]  if isinstance(p.domain, list) else p.domain
            range_ = p.range[0]  if isinstance(p.range, list) else p.range

            temp_name = "LINK_"+name
            if not onto[temp_name]:  # не было создано ранее
                types.new_class(temp_name, (domain >> range_, ))  # , Property

            temp_name = "UNLINK_"+name
            if not onto[temp_name]:  # не было создано ранее
                types.new_class(temp_name, (domain >> range_, ))


        # создаём новый class
        if not onto["DESTROY_INSTANCE"]:
            class DESTROY_INSTANCE(Thing): pass

        # новый глоб. экземпляр
        if not onto["INSTANCE"]:
            Thing("INSTANCE")

        # новое глоб. свойство (цепляется только к INSTANCE)
        if not onto["CREATE"]:
            class CREATE(Thing >> str):
                domain = [OneOf([onto["INSTANCE"]])]

        # новое свойство (name в owlready2 для того, чтобы ссылаться на объекты строками)
        if not onto["IRI"]:
            class IRI(Thing >> str, FunctionalProperty): pass

    return onto


def make_triple(subj, prop, obj):
    prop[subj].append(obj)


def remove_triple(subj, prop, obj):
    if obj in prop[subj]:
        prop[subj].remove(obj)
    # "not removed" workaround
    if FunctionalProperty in prop.is_a:
        setattr(subj, prop.python_name, None)



# global / persistent
_regexes = {}

def create_instance(onto, str_formatted):
    """
    str_formatted example: "Class1{prop1=value1; prop2=value2}"
    """
    if "class_fields" not in _regexes:
        _regexes["class_fields"] = re.compile(r"([\w\d_#~/&%$@()+=-]+)\s*(?:\{(.*)\})?", re.I)
        _regexes["keyvalue_pairs"] = re.compile(r"([\w\d_#~/&%$@()+=-]+)\s*=\s*([\w\d_#~/&%$@()+=-]+);?\s*", re.I)

    m = _regexes["class_fields"].match(str_formatted)
    assert m
    class_name, fields_str = m.groups()
#     print(class_name, fields_str)

    # создаём объект
    class_ = onto[class_name]
    assert class_ , (class_name)
    obj = class_()
    print("Instance of {} created : {}".format(class_name, obj.name))

    if fields_str:
        fields = _regexes["keyvalue_pairs"].findall(fields_str)
    else:
        fields = []

    for prop_name, value in fields:
        # получаем Property
        prop = onto[prop_name]
        assert prop , (prop_name)

        if DataProperty in prop.is_a:
            # скалярный тип данных  -  преобразуем значение из строки
            range_class = prop.range[0]
            value_actual = range_class(value)
        else:
            # объект онтологии - получаем его по IRI как есть (без проверки типов и пр.)
            value_actual = onto[value]
            assert value_actual , ("instance name: "+value)

        # создаём триплет (см. также make_triple())
        prop[obj].append(value_actual)


def augment_ontology(onto, autoremove=True):
    """ When `autoremove` == True (the default), remove special
    properties asserted/inferred after use. Leave them untouched otherwise (if possible).
    returns report of found (and used) special properties.
    """
    report = []

    with onto:
        # удаляем объекты, которые подцеплены к классу DESTROY_INSTANCE
        for o in onto.DESTROY_INSTANCE.instances():
            destroy_entity(o)
            print("DESTROY_INSTANCE: \t", o.name)
            report += [(onto.DESTROY_INSTANCE.name, o.name)]
            # информацию об указании удалить нельзя оставить, т.к. удаляется её носитель.

        # создаём и разрываем указанные связи (LINK_ , UNLINK_)

        for p in onto.properties():
            if p.name.startswith("LINK_"):
                real_p = onto[ p.name.replace("LINK_", "") ]
                for s,o in p.get_relations():
                    make_triple(s, real_p, o)
                    report += [(s.name, p.name, getattr(o,"name",o))]
                    if autoremove:
                        remove_triple(s, p, o)

            if p.name.startswith("UNLINK_"):
                real_p = onto[ p.name.replace("UNLINK_", "") ]
                for s,o in p.get_relations():
                    remove_triple(s, real_p, o)
                    report += [(s.name, p.name, getattr(o,"name",o))]
                    if autoremove:
                        remove_triple(s, p, o)

        # создаём новые объекты
        for str_formatted in onto.INSTANCE.CREATE:
            print("INSTANCE.CREATE : str_formatted: {}".format(str_formatted))
            create_instance(onto, str_formatted)
            report += [(onto.INSTANCE.name, onto.CREATE.name, str_formatted)]
            if autoremove:
                remove_triple(onto.INSTANCE, onto.CREATE, str_formatted)

    return report


def prepare_ontology_for_reasoning(onto):
    """ Ensure all instances have an IRI property assigned """
    with onto:
        prop = onto.IRI
        for o in onto.individuals():
#             print(o.name)
            if not o.IRI:
                o.IRI = o.name



def sync_pellet_cycle(onto, runs_limit=15):  ### , dest_onto=None):
    """
     Put result to the same ontology if `onto` is None (the default).
    """
#     if not dest_onto:
#         dest_onto = onto

    with onto:
        prev_specials_set = None
        # Для предотвращения опосредованного закцикливания следует вести полную историю спец. команд ...
        i = 0
        while True:
            i+=1; print("sync_pellet_cycle: iteration",i,"began ...")
            prepare_ontology_for_reasoning(onto)

            sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)

            print("sync_pellet_cycle: augmenting ontology ...")
            specials_used = augment_ontology(onto)
            specials_used = set(specials_used)
            print("sync_pellet_cycle: specials_used:")
            print(specials_used)
#             print(prev_specials_set)

            if prev_specials_set is not None:
                if specials_used.issubset(prev_specials_set):
                    # вывод закончен, новых вещей не появится.
                    print("sync_pellet_cycle: iteration",i,"is a final one. Finished successfully!")
                    return True
                    # break

            prev_specials_set = specials_used
            print("sync_pellet_cycle: iteration",i,"completed.")
            if runs_limit > 0 and i >= runs_limit:
                print("sync_pellet_cycle: max iteration count reached:",runs_limit,", stopping.")
                return False
                # break


