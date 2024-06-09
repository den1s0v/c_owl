# cf_classes.py

import enum
from adict import adict
from attrs import define, field

# from bases import *
from domain.bases import DomainFeature, DomainSituation, SituationElement
from domain.helpers import UID


# !!! from contextvars import ContextVar


# ======================== #
#  General domain section  #
# ======================== #

class Algorithm(DomainSituation):
    pass

class AlgorithmElement(SituationElement):
    algorithm: Algorithm = None
    parent: 'AlgorithmElement' = None
    data: dict = None

    def get_cfg(self) -> 'ControlFlowGraph':
        pass

    
    
@define
class ComponentInfo:
    field_name : str
    element_class: type
    onto_relation : str
    type : str = 'SINGLE' # 'SINGLE' or 'SEQUENCE'
    optional : bool = False




# @define
class ControlFlowStructure(DomainFeature):
    """
    Что и для каких целей хранит этот класс:
    
    - структура: компоненты (дочерние атомы и другие алг. структуры)
    - поведение (CFG): переходы между компонентами (для анализа путей через алгоритм)
    - ошибочные переходы (принципиально возможные, допустимые) для аннотирования вопросов
    
    - для ризонинга на данных вопроса:
        ○ статическя схема (структура классов и связей)
        ○ продукционные правила для вычисления CFG
        ○ продукционные правила для вычисления ошибок в частичном ответе
    """
    
    # : inherited properties :
    # name: str  # unique key
    # definition: 'DefinitionContent' = None
    # depends_on_features: set['DomainFeature'] ### = field(factory=set)
    # incompatible_with_features: set['DomainFeature'] ### = field(factory=set)
    # comment: str = None

    components_info : list[ComponentInfo] = None
    # _structure: 'StructureModel' = None
    
    def get_cfg(self) -> 'ControlFlowGraph':
        pass

    def init_situation_instance(self, obj: AlgorithmElement = None) -> AlgorithmElement:
        """Make / prepare AlgorithmElement instance"""
        if not obj:
            obj = AlgorithmElement(self.name + '_inst_' + next(UID))

        obj.definition = self

        # init components ...
        if not obj.components:
            obj.components = adict(
                {ci.field_name: None for ci in self.components_info}
            )
        ...
        pass
        
    def make_sample_situation_instance(self) -> AlgorithmElement:
        pass

    # @property
    # def structure(self):
    #     if not self._structure:
    #         if not self.structure_model:
    #             raise ValueError(f"{self.name} has no structure_model set.")
    #         self._structure = self.structure_model()
    #     return self._structure
        
    #     # 'StructureModel' = None

    
# class __very_draft:
    
#     # static
#     class_name = 'ControlFlowStructure'
#     base_classes = ()

    
#     # dynamic
#     name: str # = field(init=False, default='noname')
#     prepared: bool # = field(init=False, default=False)
#     parent: 'ControlFlowStructure' # = None
#     meta: type # = field(init=False, default=None)  # class
#     # alg_data: adict # = field(init=False, factory=adict)
    
#     _inner: adict[str, 'ControlFlowStructure'] = field(init=False, factory=adict)
#     features: adict[str, DomainFeature] = field(init=False, factory=adict)

#     def __init__(self, parent):
#         super().__init__()
#         self._inner = adict()
#         self.prepared = False
#         self.parent = None
#         self.meta = self.__class__
#         # self.features = adict()
#     # def __attrs_post_init__(self):
#     #     self.prepare()

#     def required_components(self) -> tuple:
#         # Should be redefined in child classes to return actual tuple of strusture's components.
#         return ()

#     def register_component(self, key, value) -> 'ControlFlowStructure':
#         self._inner[key] = value
#         if set(self._inner.keys()) == set(self.required_components()):
#             # all components were assigned, init them.
#             self.prepare()
#         return self

#     def __setattr__(self, key, value):
#         # allow access to a component via attribute: `instance.name = ...`
#         if key in self.required_components():
#             self.register_component(key, value)
#         else:
#             super().__setattr__(key, value)

#     def __getattr__(self, key):
#         if key in self.required_components():
#             return self.inner(key)
#         else:
#             super().__getattr__(key)

#     def prepare(self) -> bool:
#         if self.prepared:
#             return True
#         if self.prepare_components():
#             ...
#             self.prepared = True
#             return True
#         # still cannot be completely prepared.
#         return False
        
           
#     def inner(self, name) -> 'ControlFlowStructure':
#         """ Get existing inner structure and raise KeyError if it is not in self._inner.
#             If passed 'this' or falsy value, self will be returned.
#         """
#         if isinstance(name, ControlFlowStructure):
#             return name
#         if name == 'this' or not name:
#             return self
#         component = self._inner.get(name)
#         if not component:
#             print(f":WARN: component {name} of {self.class_name} is not assigned.")
#         return component

#     # def __getattr__(self, field):
#     #     return self._inner[field]

        
#     ####

#     def make_consequent(self, transition_id: str, spec: tuple[4]):
#         ### not-TODO: указать направление порта: вход/выход !!!!!!!!
#         from_, role_from, to, role_to = spec
#         s_from = self.inner(from_) if from_ else self
#         s_to = self.inner(to) if to else self
#         ...

#     def register_feature_maker(self, name: str, call: CallWrapper) -> None:
#         if name in self.features:
#             raise ValueError(f'feature with key "{name}" has already been registered.')
#         self.features[name] = call

#     # def connect_inner_in_parent_classes(self, black_list=None, white_list=None):
#     #     try:
#     #         super().connect_inner(black_list, white_list)
#     #     except Exception as e: ## TODO: method\attribute not found Exception
#     #         pass
#     #         ###
#     #         print(" :::exception in connect_inner_in_parent_classes():::", e.__class__.__name__, e)
#     #         ###

#     def apply_features(self, black_list=None, white_list=None):
#         """ Внести/записать в объект фичи, определяемые этим классом. Возможно отключить некоторые из фич через чёрный и белый списки. """
#         for name in self.features.keys():
#             if allowed(name, black_list, white_list):
#                 self.apply_feature(name)

#     def apply_feature(self, name):
#         """ Внести/записать в объект фичу, определяемую этим классом. """
#         func = self.features[name]
#         try:
            
#             func()  ### ...TODO!

#         except Exception as e:
#             print(f'Error appying feature "{name}" for class {self.__class__.__name__}: {e.__class__,__name__} — {e}.')

#     def connect_inner_in_parent_classes(self, black_list=None, white_list=None):
#         try:
#             super().connect_inner(black_list, white_list)
#         except Exception as e: ## TODO: method\attribute not found Exception
#             pass
#             ###
#             print(" :::exception in connect_inner_in_parent_classes():::", e.__class__.__name__, e)
#             ###

#     def connect_inner(self, black_list=None, white_list=None):
#         """ создать структуру внутренних объектов/структур, соединяя начало и конец этой структуры """
#         # TODO: implement in subclassses.
#         # raise NotImplementedError()
        
#         self.connect_inner_in_parent_classes()
#         pass

#     pass




class CorrectTransitionFeature():
    pass

class WrongJumpFeature():
    pass


class CFG_Node(adict):
    """ A node of a CFG (Control Flow Graph). 
    Normally, contains one input port and at least one output port. """
    
    # _port_in: 'CFG_Port' = None
    _ports: dict[str, 'CFG_Port'] = dict()

    def __init__(self):
        self._ports = adict()
        
    def input(self):
        """Get or create an input port (with 'input' role) """
        if 'input' not in self._ports:
            self._ports['input'] = CFG_Port.make_with_role(role='input', structure=self).with_IN_direction()
            ### debug.
            print(f'Added port with role="input" for structure {self.__class__.__name__}')
            ###

        return self._ports[input]

    def output(self, role='normal'):
        """Get or create an output port with provided role ('normal' is the default) """
        if role not in self._ports:
            self._ports[role] = CFG_Port.make_with_role(role=role, structure=self).with_OUT_direction()
            ### debug.
            if role != 'normal':
                print(f'Added port with role="{role}" for structure {self.__class__.__name__}')
            ###

        return self._ports[role]

    def outputs(self):
        """ Get a list of all not-input ports """
        return [p for role, p in self._ports.items() if role != 'input']

    # def add_port(self, role='normal', direction: 'PortDirection' = None):
    #     pass

### CFG ###

class ControlFlowGraph:
    pass




class CFG_Transition(adict):
    # kind of transition
    _kind = 'consequent'
    
    port_src: 'CFG_Port'
    port_dst: 'CFG_Port'

    @property
    def kind(self):
        return self.__class__._kind
    
    
    

## PORTS for CFG ###
    
class PortDirection(enum.Enum):
    IN = 0
    OUT = 1
    NOT_SET = 99

class CFG_Port(adict):
    "abstract ?? "

    direction: PortDirection # in|out — 0: in, 1: out
    role = "any"  # static ??
    structure: ControlFlowStructure = None
    
    role2class = adict()
    
    @classmethod   ### ???
    def register_port_class(cls, role: str):
        CFG_Port.role2class[role] = cls;   ### , cls: type
    
    @classmethod   ### ???
    def make_with_role(cls, role: str, *args, **kw):
        return CFG_Port.role2class[role](*args, **kw)

    def __init__(self, structure: ControlFlowStructure = None, role = None):
        self.direction = PortDirection.NOT_SET
        self.structure = structure
        if role:
            self.role = role

        self.outgoing_transitions = []
        self.incoming_transitions = []
        self._connected_ports = []  # all linked ports, both IN & OUT
    
    def with_IN_direction(self):
        self.direction = PortDirection.IN
        return self
    
    def with_OUT_direction(self):
        self.direction = PortDirection.OUT
        return self
    
    def connect_to_port_with_transition(self, other: 'CFG_Port', transition: CFG_Transition):
        # no.> # assert other.direction != self.direction, f"Expected inequal directions: {other.direction} != {self.direction}"
        if other not in self._connected_ports:
            # ensure correct config of transition ...
            # connect
            transition.port_src = self
            transition.port_dst = other
            self. outgoing_transitions.append(transition)
            other.incoming_transitions.append(transition)
            # remember to not to add this one twice
            self._connected_ports.append(transition)
        return self


class CFG_Port_for_NormalFlow(CFG_Port):
    role = "normal"
    # self.register_port_class(role, )

class CFG_Port_for_Condition(CFG_Port):
    "abstract"
    role = "condition"
class CFG_Port_for_TrueCondition(CFG_Port_for_Condition):
    role = "true_condition"
class CFG_Port_for_FalseCondition(CFG_Port_for_Condition):
    role = "false_condition"
    

class CFG_Port_for_Interrupting(CFG_Port):
    "abstract"
    role = "interrupting"

class CFG_Port_for_Return(CFG_Port_for_Interrupting):
    role = "return"

class CFG_Port_for_Break(CFG_Port_for_Interrupting):
    role = "break"

class CFG_Port_for_Continue(CFG_Port_for_Interrupting):
    role = "continue"





# ======================== #
# ======================== #
