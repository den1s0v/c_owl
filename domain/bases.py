# bases.py

"""
    Наброски классов данных для представления и анализа алгоритмов с точки зрения свойств и поведения алгоритмических структур.

    Что изменить в текущем "дизайне":
    • направление порта — не выделять отдельно, сделать функцией роли (input - единственая роль для входа).
    • CFG_Transition — корректный переход между портами описываемых структур. Но возможны и произвольные прыжки (GFG_Jump), о которых мы тоже можем что-то знать (какие ошибки  порождает некорректный прыжок)
    • ...
    
"""

import enum

import adict


    
def allowed(obj, black_list=None, white_list=None) -> bool:
    """General check if an object mathes black & white list (assume no restriction if related list is empty)"""
    if black_list and obj in black_list:
        return False
    if white_list and obj not in white_list:
        return False
    return True


class CallWrapper:
    """ Helper class: wrapper over function or method call, somewhat like functools.partial(). 
        The first argument of unbound method ('self', 'this' object) can be set & changed any time.
    """
    def __init__(self, func, args=(), kwargs=None, this=None) -> None:
        self.func = func # function or method
        self.args = args
        self.kwargs = kwargs or {}
        self.this = this  # object to call the method on
    def with_this(self, this=None):
        self.this = this
        return self
    def call_as_function(self, *more_args, **more_kwargs) -> enum.Any:
        """ Use also for bound methods. """
        all_kwargs = {**self.kwargs, **(more_kwargs)}
        return self.func(*self.args, *more_args, **all_kwargs)
    def call_as_method(self, *more_args, **more_kwargs) -> enum.Any:
        """ Use for unbound methods. """
        all_kwargs = {**self.kwargs, **(more_kwargs)}
        return self.func(self.this, *self.args, *more_args, **all_kwargs)
    def call(self, *more_args, **more_kwargs) -> enum.Any:
        if self.this:
            self.call_as_method(*more_args, **more_kwargs)
        else:
            self.call_as_function(*more_args, **more_kwargs)

    __call__ = call


class ConceptFeature:
    concept_class: type

    def check_concept_class(self, concept_instance) -> bool:
        if self.concept_class:
            return isinstance(concept_instance, self.concept_class)
        return True

    def applicable_to(self, concept_instance) -> bool:
        return self.check_concept_class(concept_instance)
        # raise NotImplementedError()
        pass
        
    def _apply_to_concept_instance(self, concept_instance) -> bool:
        # raise NotImplementedError()
        pass
        
    def apply_to(self, concept_instance) -> bool:
        if not self.applicable_to(concept_instance):
            return False
        return self._apply_to_concept_instance(concept_instance) or True
        

class CorrectTransitionFeature(ConceptFeature):
    pass

class WrongJumpFeature(ConceptFeature):
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
    

class ControlFlowStructure(CFG_Node):

    _inner: dict[str, 'ControlFlowStructure']
    parent: 'ControlFlowStructure' | None
    features: dict[str, 'function']

    def __init__(self):
        super().__init__()
        self._inner = adict()
        self.parent = None
        self.features = adict()

    def make_consequent(self, transition_id: str, spec: tuple[4]):
        ### not-TODO: указать направление порта: вход/выход !!!!!!!!
        from_, role_from, to, role_to = spec
        s_from = self.inner(from_) if from_ else self
        s_to = self.inner(to) if to else self
        ...

    def register_feature_maker(self, name: str, call: CallWrapper) -> None:
        if name in self.features:
            raise ValueError(f'feature with key "{name}" has already been registered.')
        self.features[name] = call

    # def connect_inner_in_parent_classes(self, black_list=None, white_list=None):
    #     try:
    #         super().connect_inner(black_list, white_list)
    #     except Exception as e: ## TODO: method\attribute not found Exception
    #         pass
    #         ###
    #         print(" :::exception in connect_inner_in_parent_classes():::", e.__class__.__name__, e)
    #         ###

    def apply_features(self, black_list=None, white_list=None):
        """ Внести/записать в объект фичи, определяемые этим классом. Возможно отключить некоторые из фич через чёрный и белый списки. """
        for name in self.features.keys():
            if allowed(name, black_list, white_list):
                self.apply_feature(name)

    def apply_feature(self, name):
        """ Внести/записать в объект фичу, определяемую этим классом. """
        func = self.features[name]
        try:
            
            func()  ### ...TODO!

        except Exception as e:
            print(f'Error appying feature "{name}" for class {self.__class__.__name__}: {e.__class__,__name__} — {e}.')

    def inner(self, name) -> 'ControlFlowStructure':
        """ Get existing inner structure and raise KeyError if it is not in self._inner.
            If passed 'this' or falsy value, self will be returned.
        """
        if isinstance(name, ControlFlowStructure):
            return name
        if name == 'this' or not name:
            return self
        return self._inner[name]

    def __getattr__(self, field):
        return self._inner[field]

    def connect_inner_in_parent_classes(self, black_list=None, white_list=None):
        try:
            super().connect_inner(black_list, white_list)
        except Exception as e: ## TODO: method\attribute not found Exception
            pass
            ###
            print(" :::exception in connect_inner_in_parent_classes():::", e.__class__.__name__, e)
            ###

    def connect_inner(self, black_list=None, white_list=None):
        """ создать структуру внутренних объектов/структур, соединяя начало и конец этой структуры """
        # TODO: implement in subclassses.
        # raise NotImplementedError()
        pass

    pass


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
    register_port_class(role, )

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


