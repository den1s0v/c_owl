# bases.py

import enum

import adict


class ControlFlowStructure:

    _port_in: 'CFG_Port' = None
    _ports_out: dict[str, 'CFG_Port'] = dict()

    inner: dict[str, 'ControlFlowStructure']

    def __init__(self):
        self._port_in = None
        self._ports_out = dict()
        self.inner = dict()

    def make_consequent(self, spec: tuple[4]):
        ### TODO: указать направлние порта: вход/выход !!!!!!!!
        from_, role_from, to, role_to = spec
        s_from = self.inner[from_] if from_ else self
        s_to = self.inner[to] if to else self


    def input(self):
        if not self._port_in:
            self._port_in = CFG_Port.make_with_role(role='normal', structure=self).with_IN_direction()

        return self._port_in

    def output(self, role='normal'):
        if role not in self._ports_out:
            self._ports_out[role] = CFG_Port.make_with_role(role=role, structure=self).with_OUT_direction()
            ### debug.
            if role != 'normal':
                print(f'Added port with role="{role}" for structure {self.__class__.__name__}')
            ###

        return self._ports_out[role]

    def connect_inner_in_parent_classes(self):
        try:
            super().connect_inner()
        except Exception as e: ## TODO: method\attribute not found Exception
            pass
            ###
            print(" :::exception in connect_inner_in_parent_classes():::", e.__class__.__name__, e)
            ###

    def connect_inner(self):
        """ создать структуру внутренних объектов/структур, соединяя начало и конец этой структуры """
        # TODO: implement in subclassses.
        raise NotImplementedError()

    pass


### CFG ###

class ControlFlowGraph:
    pass


class CFG_Node(adict):
    
    def __init__(self):
        self.input_ports = adict()
        self.output_ports = adict()
        
    def add_port(self, direction: 'PortDirection', role='normal'):
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
    "abstract"

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


