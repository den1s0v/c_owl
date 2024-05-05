# bases.py

import enum

import adict


class ControlFlowStructure:
    pass


### CFG ###

class ControlFlowGraph:
    pass


class CFG_Node(adict):
    
    def __init__(self):
        self.input_ports = adict()
        self.output_ports = adict()
        
    def add_port(self, direction: 'PortDirection', role='normal')


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

class CFG_Port(adict):
    "abstract"
    direction: PortDirection # in|out — 0: in, 1: out
    role = "any"
    
    role2class = adict()
    
    @classmethod   ### ???
    def register_subclass(subclass, role: str):  CFG_Port.role2class[role] = subclass;   ### , subclass: type
    
    def __init__(self):
        self.outgoing_transitions = []
        self.incoming_transitions = []
        self.connected_ports = []
    
    def set_IN_direction(self):
        self.direction = PortDirection.IN
        return self
    
    def set_OUT_direction(self):
        self.direction = PortDirection.OUT
        return self
    
    def connect_to_port_with_transition(self, other: 'CFG_Port', transition: CFG_Transition):
        # no.> # assert other.direction != self.direction, f"Expected inequal directions: {other.direction} != {self.direction}"
        if other not in self.connected_ports:
            # ensure correct config of transition ...
            # connect
            transition.port_src = self
            transition.port_dst = other
            self. outgoing_transitions.append(transition)
            other.incoming_transitions.append(transition)
            # remember to not to add this one twice
            self.connected_ports.append(transition)
        return self


class CFG_Port_for_NormalFlow(CFG_Port):
    role = "normal"
    register_subclass(role, )

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


