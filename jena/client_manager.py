# client_manager.py

'''
	Manages instances (e.g. of JenaClient) over different threads in order to provide free instances as workers for simultaneous requests (connections)
'''

from threading import Lock

# from jena.jenaClient import JenaClient


class ClientManager:
	def __init__(self, instance_factory_function):
		self.factory = instance_factory_function
		self._lock = Lock()
		# sets of ready active instances
		self._busy = set()
		self._free = set()

	def run(self, lambda_on_instance) -> 'result':
		instance = self.get()
		try:
			result = lambda_on_instance(instance)
			return result  # finally will run anyway ->
		except Exception as ex:
			raise ex
		finally:
			self.free(instance)

	def get(self) -> 'instance':
		'get a _free instance or allocate a new instance'
		with self._lock:
			if not self._free:
				self._free.add(self.factory())
			instance = next(iter(self._free))
			self._free.remove(instance)
			self._busy.add(instance)
		return instance

	def free(self, instance):
		'call after the instance has completed its work!'
		with self._lock:
			assert instance in self._busy, "instance is not in manager's _busy ones!"
			self._busy.remove(instance)
			self._free.add(instance)

