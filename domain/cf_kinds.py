# cf_kinds.py

# from bases import *
from bases import ControlFlowStructure


class Atom(ControlFlowStructure):
    def connect_inner(self):

        self.connect_inner_in_parent_classes()

class Expr(Atom):
    pass

class Alternative(ControlFlowStructure):
    
    def prepare_components(self):
        pass
    
    def connect_inner(self):
        self.connect_inner_in_parent_classes()


class WhileLoop(ControlFlowStructure):
    
    def prepare_components(self):
        expr = self.alg_data.get('cond')
        self._inner.cond = Expr(name=str(expr), parent=self)
        
        body = self.alg_data.get('body')
        self._inner.body = ControlFlowStructure(name=str(body['name']), parent=self, alg_data=body)
        
    def connect_inner(self):
        self.connect_inner_in_parent_classes()
        
        pass
        
    


# See: 
    # text2algntr: 384
    # ctrlstrct_run: 361
