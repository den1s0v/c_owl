# cf_domain.py


from domain.bases import Domain
from domain.cf_classes import *


domain = Domain(
    name = 'control_flow',
)


@domain.register_feature_class
class Action(ControlFlowStructure):
    name = 'action'


# class Atom(ControlFlowStructure):
#     ...

@domain.register_feature_class
class Statement(Action):
    pass

@domain.register_feature_class
class Expr(Action):
    name = 'expr'
    pass

@domain.register_feature_class
class Sequence(Statement):
    name = 'sequence'
    
    components_info = [
        ComponentInfo(
            'body',
            element_class = Statement,
            onto_relation = 'body_item',
            type = 'SEQUENCE',
        )
    ]
    
    def get_cfg(self):
        pass
    

@domain.register_feature_class
class AlternativeBranch(ControlFlowStructure):
    name = 'alt_branch'
    
    
@domain.register_feature_class
class AlternativeIfBranch(AlternativeBranch):
    name = 'if'
    components_info = [
        ComponentInfo(
            'cond',
            element_class = Expr,
            onto_relation = 'cond',
        ),
        ComponentInfo(
            'body',
            element_class = Statement,
            onto_relation = 'cond',
        ),
    ]
    
    
@domain.register_feature_class
class AlternativeElseIfBranch(AlternativeIfBranch):
    name = 'else-if'
    # (same components_info as 'if' has)
    
    
@domain.register_feature_class
class AlternativeElseBranch(AlternativeIfBranch):
    name = 'else'
    components_info = [
        ComponentInfo(
            'body',
            element_class = Statement,
            onto_relation = 'cond',
        ),
    ]
    
@domain.register_feature_class
class Alternative(Statement):
    name = 'alternative'
    
    components_info = [
        ComponentInfo(
            'branches',
            element_class = AlternativeBranch,
            onto_relation = 'branches_item',
            type = 'SEQUENCE',
        )
    ]
    
    def get_cfg(self):
        pass
    


@domain.register_feature_class
class WhileLoop(Statement):
    name = 'while_loop'
    
    # def prepare_components(self):
    #     expr = self.alg_data.get('cond')
    #     self._inner.cond = Expr(name=str(expr), parent=self)
        
    #     body = self.alg_data.get('body')
    #     self._inner.body = ControlFlowStructure(name=str(body['name']), parent=self, alg_data=body)
        
    # def connect_inner(self):
    #     self.connect_inner_in_parent_classes()
        
    pass
        
    


# See: 
    # text2algntr: 384
    # ctrlstrct_run: 361
