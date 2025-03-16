# bases.py

"""
    Наброски классов данных для представления и анализа алгоритмов с точки зрения свойств и поведения алгоритмических структур.

    Что изменить в текущем "дизайне":
    • направление порта — не выделять отдельно, сделать функцией роли (input - единственая роль для входа).
    • CFG_Transition — корректный переход между портами описываемых структур. Но возможны и произвольные прыжки (GFG_Jump), о которых мы тоже можем что-то знать (какие ошибки  порождает некорректный прыжок)
    • ...
    
"""

import enum
from typing import Iterable

from adict import adict
from attrs import define, field

from domain.helpers import CallWrapper, recursive_dive_along_attribute

try:
    from domain.helpers import allowed
except ImportError:
    from helpers import allowed
    



### Abstract Domain logic. ### 

### Meta-domain layer. ### 

@define
class Domain:
    name: str
    # features: adict[str, 'DomainFeature'] = field(factory=adict)
    features: adict[str, 'type'] = field(factory=adict)
    # definitions: adict[str, 'DomainDef'] = field(factory=adict)
    # rules: adict[str, DomainRule] = field(factory=adict)

    def register_feature(self, feature: 'DomainFeature'):
        name = feature.name
        if name in self.features:
            # raise KeyError
            print(f"Feature with name '{name}' has been already registered!")
            return
        self.features[name] = feature
        print(type(feature), feature, 'registered in domain as', name)
        
    def register_feature_class(self, feature_class: type):
        # print(1, feature_class)
        # print(2, repr(feature_class))
        # print(3, type(feature_class))
        
        # feature = feature_class.__call__()  # !!!!!!!!!!!! ←←←← `TypeError: object.__new__(): not enough arguments`
        # ??????????????? ↑
        
        feature = feature_class
        # if not isinstance(feature, DomainFeature):
        #     raise TypeError(f'{feature_class} is not a subclass of DomainFeature!')
        self.register_feature(feature)
        return feature
        
    def get_tbox(self, require: Iterable['DomainFeature']=(), deny: Iterable['DomainFeature']=()) -> 'DefinitionContent':
        dc = DefinitionContent()
        for feat in self.features.values():
            dc += feat.get_tbox(require, deny)
        return dc    
    
    
@define
class DomainFeature:
    """Abstract domain element having related definitions & statements describing it."""

    name: str = None  # unique key
    definition: 'DefinitionContent' = None
    depends_on_features: set['DomainFeature'] = field(factory=set)
    incompatible_with_features: set['DomainFeature'] = field(factory=set)
    comment: str = None

    _full_set_depends_on_features: set['DomainFeature'] = None
    _full_set_incompatible_with_features: set['DomainFeature'] = None
    
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) and self.name == other.name

    def __str__(self) -> str:
        return f"DomainFeature<{self.name}>"
    
    __repr__ = __str__

    def get_base_classes(self) -> Iterable['DomainFeature']:
        return self.__class__.mro()

    def all_required_features(self) -> set['DomainFeature']:
        if not self._full_set_depends_on_features:
            # note: infinite recurseion is not checked.
            self._full_set_depends_on_features = {*recursive_dive_along_attribute(self, 'depends_on_features')}
        return self._full_set_depends_on_features

    def all_incompatible_features(self) -> set['DomainFeature']:
        if not self._full_set_incompatible_with_features:
            # note: infinite recurseion is not checked.
            self._full_set_incompatible_with_features = {*recursive_dive_along_attribute(self, 'incompatible_with_features')}
        return self._full_set_incompatible_with_features
            
    def is_needed_for(self, require: Iterable['DomainFeature']=(), deny: Iterable['DomainFeature']=()) -> bool:
        # check if lookup sets are filled
        if set(deny) & self.all_required_features():
            return False
        if set(require) & self.all_incompatible_features():
            return True
        return False  # Not denied but not required as well.
        
    def get_tbox(self, require: Iterable['DomainFeature']=(), deny: Iterable['DomainFeature']=()) -> 'DefinitionContent':

        if not self.is_needed_for(require, deny):
            return None
        
        dc = DefinitionContent()
        
        if self.definition:
            dc += self.definition
        
        # for base in self.get_base_classes():  ## ???
        for base in self.all_required_features():
            dc += base.get_tbox()
        return dc


# @define
class DomainElement(DomainFeature):
    """ A domain object that may be 'instantiated', i.e. it may present as holistic domain object, not as 'transparent' feature of such. """
    # name: str = None
    pass
    




@define
class DomainSituation:
    name: str
    elements: list['SituationElement'] = None
    
    def get_abox(self) -> 'DefinitionContent':
        dc = DefinitionContent()

        for elt in self.elements or ():
            dc += elt.get_abox()
        return dc


class SituationElement(adict):
    name: str  # unique key; must not match any other names
    definition: DomainElement = None
    components: adict = None
    
    def get_abox(self) -> 'DefinitionContent':
        """Obtain "dynamic" definitions (ABox) for this specific instance. This can also include related productional rules, but this is not recommended."""
        dc = DefinitionContent()
        # TODO return name assertion, at least
        ...
        return dc



# ========================================== #


### Generalized domain component kinds. ###

# # @define
# class __DomainConcept(DomainElement):
#     # name: str = None
#     requires_concepts: Iterable['DomainConcept' | str] = None

#     structure : 'StructureModel' = None
#     # behaviour : 'BehaviourModel' = None
    
#     def possible_reasons(self) -> Iterable['Reason']:
#         return ()
#     def possible_violations(self) -> Iterable['Violation']:
#         return ()

#     @property
#     def depends_on_features(self) -> set['DomainFeature']:
#         'unsafe recursion over "bases" '
#         return {self} | {
#             dc.depends_on_features
#             for dc in self.requires_concepts or ()
#         }
#     # @property def incompatible_with_features() ...?
    

# class StructureModel:
#     elements: adict[str, 'StructureElement'] = field(factory=adict)

# class StructureElement:
#     parent_element : 'StructureElement'

# class StructuralRelation:
#     domain_class: type
#     range_class: type


# class BehaviourModel:
#     # elements: adict[str, 'StructureElement'] = field(factory=adict)
#     pass


class Reason:
    """I.e. positive Law"""
    name: str

class Violation:
    """I.e. negative Law"""
    name: str




# ... ### Перенести в конкретную реализацию домена ###  ??


class DomainAssertion(tuple):
    """ Container for a single triple. """
    
    def __init__(self, s_or_t, p=None, o=None):
        # unpack tuple if needed
        if p and o is not None:
            s = s_or_t
        elif isinstance(s_or_t, tuple) and len(s_or_t) == 3:
            t = s_or_t
            s, p, o = t
        else:
            raise ValueError(f"incompatible tuple for DomainAssertion: {(s_or_t, p, o)}")
        
        # expand/convert shortcuts
        if p == 'a':
            p = 'rdf:type'
        
        # init tuple
        super().__init__(s, p, o)
    
    @property
    def subject(self): return self[0]
    s = subject

    @property
    def predicate(self): return self[1]
    p = predicate

    @property
    def object(self): return self[2]
    o = object

    def apply(ontology_or_graph):
        raise NotImplementedError()
    # triple: list = field(factory=list)
    # def get_tbox(self) -> DefinitionContent:
    #     """Obtain static definitions (TBox) for this concept/feature/etc. This can include related productional rules."""
    #     raise NotImplementedError()


@define
class DomainRule:
    name: str = None
    formulation: str = None
    backend: str = field(default='Jena')
    role: str = None  # for grouping rules by purpose
    salience: int = 0
    comment: str = None


@define
class DefinitionContent:
    key: str = None
    assertions: list['DomainAssertion'] = field(factory=list)
    # assertions: rdflib.Graph = None # ???
    rules: list[DomainRule] = field(factory=list)
    user_data: adict = None # field(factory=adict)

    # def __init__(self, key: str, assertions: list=None, rules: list=None, **kwargs):
    #     self.key = key
    #     self.assertions = assertions or []
    #     self.rules = rules or []
    #     self.user_data = adict(kwargs)

    def __add__(self, other: 'DefinitionContent') -> 'DefinitionContent':
        return DefinitionContent(
            f"{self.key}+{other.key}",
            self.assertions + other.assertions,
            self.rules + other.rules,
            **(self.user_data | other.user_data),
        )
        
    def __iadd__(self, other: 'DefinitionContent'):
        if not other:
            # ignore if empty
            return self
        if (other.key): 
            self.key += other.key
        if (other.assertions): 
            self.assertions += other.assertions
        if (other.rules): 
            self.rules += other.rules
        if (other.user_data): 
            self.user_data |= other.user_data
        return self
        
    ### ... 



# @define
# class DomainDef:
#     name: str
#     # features: adict = field(factory=adict)
#     user_data: adict = field(factory=adict)
#     # rules: adict = field(factory=adict)

#     def get_tbox(self) -> DefinitionContent:
#         """Obtain static definitions (TBox) for this concept/feature/etc. This can include related productional rules."""
#         raise NotImplementedError()

#     def get_rules(self) -> DomainRule:
#         """Obtain productional rules for this concept/feature/etc. """
#         raise NotImplementedError()
        
    # @classmethod
    # def register_in_domain(cls, domain: Domain):
    #     """ Этот статический метод обязателен для каждого подкласса фичи домена. Должен быть вызван вскоре после объявления класса (чтобы к моменту обработки пользовательских данных домен был готов к этому). """
    #     feature_instance = cls()
    #     domain.register_feature(feature_instance)
    #     pass
    
