# cf_kinds.py

# from bases import *
from bases import ControlFlowStructure


class Atom(ControlFlowStructure):
	def connect_inner(self):

		self.connect_inner_in_parent_classes()
