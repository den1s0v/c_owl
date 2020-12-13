"""

Auto-augmenting ontology (wrapper for OwlReadу2 ontology).
Enables support for changing ontology via SWRL by iteratively ru reasoner and make changes directly in the ontology.


# ========================== #

Используем простые property для выполнения модификации онтологии

* Удаление связи prop1

UNLINK_prop1(?x, ?y)


* Добавление связи prop1  (позже)

LINK_prop1(?x, ?y)


* Удаление объекта (экземпляра) ?x

DESTROY_INSTANCE(?x)   # назначение объекту спец. класса DESTROY_INSTANCE


* Добавление объектов (экземпляров) класса Class1

CREATE(INSTANCE , "Class1{prop1=value1; prop2=value2}")  # назначение свойства глобальному спец. экземпляру со строкой

# если prop - DataProperty, то оставляем так
# если prop - ObjectProperty, то в условной части вытаскиваем id (поле-идентификатор) объекта и заменяем value на id.


"""

import re
import types

from owlready2 import *




def make_triple(subj, prop, obj):
	try:
		if FunctionalProperty in prop.is_a:
			# "not asserted" workaround
			setattr(subj, prop.python_name, obj)
		else:
			prop[subj].append(obj)
	except Exception as e:
		print("Exception in make_triple: ", subj, prop, obj)
		raise e


def remove_triple(subj, prop, obj):
	try:
		if FunctionalProperty in prop.is_a:
			# "not removed" workaround
			setattr(subj, prop.python_name, None)
		else:
			if obj in prop[subj]:
				prop[subj].remove(obj)
	except Exception as e:
		print("Exception in remove_triple: ", subj, prop, obj)
		raise e


def get_relation_object(subj, prop):
	"""
	Another way to retrieve 3rd element of stored triple.
	Usage:
		obj = get_relation_object(subj, prop)
	Works when the following fails (this appears generally with FunctionalProperty'es):
		obj = subj.prop
		objs = prop[subj]
	"""
	d = dict(prop.get_relations())
	return d.get(subj, None)

def get_relation_subject(prop, obj):
	"""
	Another way to retrieve 1st element of stored triple.
	Usage:
		obj = get_relation_object(subj, prop)
	(This may be good for InverseFunctionalProperty'es)
	"""
	d = dict((b,a) for a,b in prop.get_relations())
	return d.get(obj, None)



# make wrapping methods
# if False and AugmentingOntology:
# 	_src_class = namespace.Ontology
# 	_dst_class = AugmentingOntology
# 	mtds = "__contains__ __getattr__ __getitem__  __getslice__ __iter__ __len__ __setattr__ __setitem__ __setslice__ __setslice__".split()
# 	for m in mtds:
# 		if hasattr(_src_class, m):
# 			mtd = getattr(_src_class, m)
# 			wr_mtd = lambda self,*args,**kw: (getattr(self.onto, m).__call__(self.onto, *args,**kw))
# 			setattr(_dst_class, m, wr_mtd)



""" How to cause ontology augmentation: Examples

# create on ontology
onto1 = get_ontology("my-test-onto")

# ...

# mark to remove an instance ("a1" here)
onto1["a1"].is_a.append(onto1.DESTROY_INSTANCE)

# mark to create new ClsA instance with two properties assigned (note passing other instances as ontology name strings)
create_instance(onto1, "ClsA{hasProp=instB; hasFuncProp=instA}")


# mark to assert a relation
with onto1:
	make_triple(a, onto1.LINK_hasProp, b)

# mark to retract a relation
with onto1:
	make_triple(a, onto1.UNLINK_hasProp, b)


# ...

# run automatic augmentation which removing all the tool artifacts:
augment_ontology(onto1)

"""

class AugmentingOntology(object):
	"""A wrapper for OwlReadу2 ontology"""
	def __init__(self, src_onto, no_init=False):
		super(AugmentingOntology, self).__init__()
		self.onto = src_onto
		if not no_init:
			self.init()


	def init(self, **kwargs):
		# _patch_ontology(onto, ignore_properties=None)
		_patch_ontology(self.onto, **kwargs)

	def sync(self, **kwargs):
		"Perform full sync of the ontology with Pellet reasoner & augmentation mechanism allowing powerful means to change the ontology via SWRL"
		# sync_pellet_cycle(onto, runs_limit=15)
		success,n_runs = sync_pellet_cycle(self.onto, **kwargs)
		
		return success,n_runs


# injected property prefices
_special_prefixes =  [
	"LINK_", "UNLINK_",  # prefixes for properties replicated existiong properties
	"CREATE", "IRI", # "CountableProperty",  # full names of properties
	"COUNT_", "N_"  # prefix for name of property that holds the count of links
]


def _patch_ontology(onto, ignore_properties=None, verbose=False):
	"""
	Run once after an ontology init.

	ignore_properties=None : TODO (skip some properties)
	make extended properties selectively relying on SWRL rules set : TODO
	"""

	with onto:
		# создаём новые property
		for pass_i in range(1):   # ensure to create "COUNT_" first
			for p in onto.properties():
				name = p.name
				if any(name.startswith(px) for px in _special_prefixes):
					print("skipped", name)
					continue

				# domain = p.domain[0]  if isinstance(p.domain, list) else p.domain
				# range_ = p.range[0]  if isinstance(p.range, list) else p.range
				domain = p.domain
				range_ = p.range
				if isinstance(domain, list):
					domain = domain[0]  if len(domain)>0 else Thing
				if isinstance(range_, list):
					range_ = range_[0]  if len(range_)>0 else (str  if DataProperty in p.is_a else  Thing)


				temp_name = "LINK_"+name
				if pass_i == 0 and not onto[temp_name]:  # не было создано ранее
					types.new_class(temp_name, (domain >> range_, ))  # , Property
					if verbose: print(name, ":", domain, ">>", range_)

				temp_name = "UNLINK_"+name
				if pass_i == 0 and not onto[temp_name]:  # не было создано ранее
					types.new_class(temp_name, (domain >> range_, ))

				temp_name = "COUNT_"+name
				if pass_i == 0 and not onto[temp_name]:  # не было создано ранее
					types.new_class(temp_name, (domain >> bool , FunctionalProperty))
				temp_name = "N_"+name
				if pass_i == 0 and not onto[temp_name]:  # не было создано ранее
					types.new_class(temp_name, (domain >> int , FunctionalProperty))


		# создаём новый class
		if not onto["DESTROY_INSTANCE"]:
			class DESTROY_INSTANCE(Thing): pass

		# новый глоб. экземпляр
		if not onto["INSTANCE"]:
			Thing("INSTANCE")

		# новое глоб. свойство (цепляется только к INSTANCE)
		if not onto["CREATE"]:
			class CREATE(Thing >> str):
				domain = [OneOf([onto["INSTANCE"]])]

		# новое свойство (name в owlready2 для того, чтобы ссылаться на объекты строками)
		if not onto["IRI"]:
			class IRI(Thing >> str, FunctionalProperty): pass

	return onto


# global / persistent
_regexes = {}

def create_instance(onto, str_formatted):
	"""
	str_formatted example: "Class1{prop1=value1; prop2=value2}"
	"""
	if "class_fields" not in _regexes:
		# <class_name> with optional {...}
		_regexes["class_fields"] = re.compile(r"([\w\d_#~/&%$@()+=-]+)\s*(?:\{(.*)\})?", re.I)
		# <prop_name> = <short IRI> or [...a string...]
		_regexes["keyvalue_pairs"] = re.compile(r"([\w\d_#~/&%$@()+=-]+)\s*=\s*([\w\d_#~/&%$@()+=-]+|\[[^\]]+?\]);?\s*", re.I)

	m = _regexes["class_fields"].match(str_formatted)
	assert m
	class_name, fields_str = m.groups()
	# print(class_name, fields_str)

	# создаём объект
	class_ = onto[class_name]
	assert class_ , (class_name)
	obj = class_()

	if fields_str:
		fields = _regexes["keyvalue_pairs"].findall(fields_str)
	else:
		fields = []

	for prop_name, value in fields:
		# получаем Property
		prop = onto[prop_name]
		assert prop , (prop_name)

		if DataProperty in prop.is_a:
			# скалярный тип данных  -  преобразуем значение из строки
			if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
				value = value[1:-1]
			range_class = prop.range[0]
			value_actual = range_class(value)
		else:
			# объект онтологии - получаем его по IRI как есть (без проверки типов и пр.)
			value_actual = onto[value]
			assert value_actual , ("instance name: "+value)

		# создаём триплет (см. также make_triple())
		prop[obj].append(value_actual)

	print("Instance of {} created : {}, fields: {}".format(class_name, obj.name, str(fields)))


def augment_ontology(onto, apply_only=None, apply_changes=True, autoremove=True, verbose=1):
	"""
	Find all specials intended to make changes in the ontology and apply them.
	
	When `apply_only` is None (the default), find and apply all the specials available.
	When `apply_only` is not None it must be an iterable of a (subset of) report returned before. If so, the changes applied will be limited to the provided, other changes wiil be discarded (removed but not applied).
	Passing [] blocks applying any of specials present in the ontology (along with autoremove=True, all specials will be discarded). The returned report will be empty is this case.
	
	When `apply_changes` is True (the default), apply the changes to the ontology, leave the ontology untouched otherwise (a.k.a. "dry run").
	
	When `autoremove` is True (the default) and `apply_changes` is True, remove the special properties applied/found. Leave them untouched otherwise (if possible). Nothing is done if when `apply_changes` is False.
	
	Returns report of special properties found (regardling the related changes applied or not).
	"""
	
	def judge_case(report_case):  # -> apply, remove  (booleans)
		nonlocal report
		report.append(report_case)
		if apply_only is None:
			return apply_changes, autoremove and apply_changes
		else:
			return apply_changes and report_case in apply_only, autoremove and apply_changes
		
	
	report = []

	with onto:
		# удаляем объекты, которые подцеплены к классу DESTROY_INSTANCE
		for o in onto.DESTROY_INSTANCE.instances():
			apply_, remove = judge_case( (onto.DESTROY_INSTANCE.name, o.name) )
			if apply_:
				destroy_entity(o)
				if verbose: print("<DESTROY_INSTANCE> : ", o.name)
				# информацию об указании удалить нельзя оставить, т.к. удаляется её носитель.

		# создаём и разрываем указанные связи (LINK_ , UNLINK_), считаем объекты (COUNT_)

		for p in onto.properties():
			if p.name.startswith("LINK_"):
				real_p = onto[ p.name.replace("LINK_", "") ]  # does always exist
				for s,o in p.get_relations():
					apply_, remove = judge_case( (s.name, p.name, getattr(o,"name",o)) )
					if apply_:
						make_triple(s, real_p, o)
					if remove:
						remove_triple(s, p, o)

			if p.name.startswith("UNLINK_"):
				real_p = onto[ p.name.replace("UNLINK_", "") ]
				for s,o in p.get_relations():
					apply_, remove = judge_case( (s.name, p.name, getattr(o,"name",o)) )
					if apply_:
						remove_triple(s, real_p, o)
					if remove:
						remove_triple(s, p, o)

			if p.name.startswith("COUNT_"):
				real_p = onto[ p.name.replace("COUNT_", "") ]
				n_p = onto[ p.name.replace("COUNT_", "N_") ]
				for s,o in p.get_relations():
					old_n = get_relation_object(s, real_p)
					# подсчитаем число триплетов с s в левой части
					new_n = [s1 for s1,o1 in real_p.get_relations()].count(s)
					# this modification cannot cause infinite loop, so do not log it
					judge_case( (s.name, p.name, old_n, new_n) )  # just report activity
					if apply_changes:  # if apply_:
						if o:  # true -> do count
							make_triple(s, n_p, float(new_n))
						else:  # false -> remove the special property
							remove_triple(s, n_p, old_n)
					# if remove:
					# 	remove_triple(s, p, o)

		# создаём новые объекты
		for str_formatted in onto.INSTANCE.CREATE:
			apply_, remove = judge_case( (onto.INSTANCE.name, onto.CREATE.name, str_formatted) )
			if apply_:
				if verbose: print("<INSTANCE.CREATE> : {}".format(str_formatted))
				create_instance(onto, str_formatted)
			if remove:
				remove_triple(onto.INSTANCE, onto.CREATE, str_formatted)

	return report


def prepare_ontology_for_reasoning(onto):
	""" Ensure all instances have an IRI property assigned """
	with onto:
		assert onto.IRI
		for o in onto.individuals():
			if not o.IRI:
				o.IRI = o.name


def sync_pellet_cycle(onto, runs_limit=15, verbose=1):
	"""
	 Обёртка вокруг запуска Pellet
	 Put the result to the same ontology `onto`.
	"""

	with onto:
		# Для предотвращения опосредованного закцикливания ведём полную историю спец. команд
		all_specials = set()
		i = 0
		try:
			
			while True:
				i += 1; 	
				if verbose: print("sync_pellet_cycle: iteration",i,"began ...")
				prepare_ontology_for_reasoning(onto)

				# запуск Pellet
				sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True, debug=0)

				if verbose: print("sync_pellet_cycle: augmenting ontology ...")
				specials_to_use = augment_ontology(onto, apply_changes=False, verbose=verbose)
				specials_to_use = set(specials_to_use) - all_specials

				if not specials_to_use:
					# вывод закончен, новых вещей не появится.
					# очистим онтологию от неиспользованных спец. свойств
					augment_ontology(onto, apply_only=[], verbose=verbose)
					if verbose: 
						print("sync_pellet_cycle: iteration",i,"is a final one. Finished successfully!")
						print("Total distinct specials used: ",len(all_specials))
					return True,i
					# break
				# specials_to_use = None  # uncomment to allow repeated commands to run

				if verbose: print("sync_pellet_cycle: augmenting ontology ...")
				specials_used = augment_ontology(onto, apply_only=specials_to_use, verbose=verbose)
				specials_used = set(specials_used)
				if verbose: 
					print("sync_pellet_cycle: specials_used:")
					print(specials_used)
	            # print(prev_specials)

				# prev_specials = specials_used
				all_specials.update(specials_used)
				
				if verbose: print("sync_pellet_cycle: iteration",i,"completed.")
				if runs_limit > 0 and i >= runs_limit:
					if verbose: print("sync_pellet_cycle: max iteration count reached:",runs_limit,", stopping.")
					return False,i
					# break
					
		except base.OwlReadyInconsistentOntologyError:
			# if verbose: 
			print("sync_pellet_cycle: OwlReadyInconsistentOntologyError thrown.")
			return False,i


