# common_helpers.py

from timeit import default_timer as timer


class Checkpointer():  # dict
    'Measures time between hits. Requires the `from timeit import default_timer as timer`'
    def __init__(self, start=True):
        super().__init__()
        self.first = timer()
        self.last = self.first
        # if start:
        #     self.hit()
    def reset_now(self):
        self.__init__(start=False)
    def hit(self, label=None) -> float:
        now = timer()
        delta = now - self.last
        if label:
            print((label or 'Checkpoint') + ':', "%.3f" % delta, 's')
        self.last = now
        return delta
    def since_start(self, label=None, hit=False) -> float:
        now = timer()
        delta = now - self.first
        if label:
            print(label or 'Total:', "%.3f" % delta, 's')
        if hit:
            self.last = now
        return delta


class Uniqualizer():

	label2max_free = {}

	@classmethod
	def get(cls, label: str):
		# if label in label2max_free:
		max_n, free = cls.label2max_free.get(label, (0, ()))
		if free:
			n = free[0]
			free = free[1:]
		else:
			n = max_n + 1
			max_n = n
		cls.label2max_free[label] = (max_n, free)

		return '%s_%x' % (label, n), n

	@classmethod
	def free(cls, label: str, n: int):
		if label in cls.label2max_free:
			max_n, free = cls.label2max_free.get(label)
			if max_n == n:
				max_n -= 1
				# continue freeing
				if max_n in free:
					free = list(free)
					while max_n in free:
						free.remove(max_n)
						max_n -= 1
					free = tuple(free)

			elif n not in free:
				free = free + (n,)

			cls.label2max_free[label] = (max_n, free)

	def __init__(self):
		"Should not be instantiated"
		pass


import os

def delete_file(file):
	if os.path.exists(file):
		try:
			os.remove(file)
			print("File removed:", file)
		except Exception as e:
			print("Exception while removing file:", file)
			print('\t', e)
	else:
		# print("File does not exist")
		pass


if __name__ == '__main__':
	print(Uniqualizer.get('abc'))
	print(Uniqualizer.get('abc'))
	print(Uniqualizer.get('abc'))
	print(Uniqualizer.free('abc', 1))
	print(Uniqualizer.free('abc', 2))
	print(Uniqualizer.free('abc', 5))
	print(Uniqualizer.get('abc'))
	print(Uniqualizer.get('abc'))
	print(Uniqualizer.get('abc'))
	print(Uniqualizer.get('abc'))
