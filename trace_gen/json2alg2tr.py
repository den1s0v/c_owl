# json2alg2tr.py

import copy
from collections import namedtuple
import json
import re
import threading

# special storage that allows storing data isolated for each thread by dispatching calls from different threads internally
thread_globals = threading.local()

SUPPORTED_LANGS = ("ru", "en")
DEFAULT_LANG = "ru"


def set_target_lang(lang_code: str):
    # global TARGET_LANG
    assert lang_code in SUPPORTED_LANGS, lang_code
    thread_globals.TARGET_LANG = lang_code


### print('===', "TARGET_LANG:", TARGET_LANG, '===')

def get_target_lang():
    try:
        return thread_globals.TARGET_LANG
    except AttributeError:
        return DEFAULT_LANG


def tr(word_en, case='nomn'):
    """ Перевод на русский язык, если TARGET_LANG=="ru" """
    TARGET_LANG = get_target_lang()
    if TARGET_LANG == "en":
        return (
            str(word_en).lower()
                .replace("(he)", '')  # 1 leading space remains
                .replace("(she)", '')  # 1 leading space remains
                .replace("(it)", '')  # 1 leading space remains
                .replace("else-if", "else if")
                .replace("(branch)", '')
                .replace("comment", '// ')
                .replace("nth time", 'th time')
                .replace("started", 'began')
                .replace("finished", 'ended')
                .replace("performed", 'executed')
                .replace("cond", 'condition')  # 'condition of'
                .lstrip()
        )
    # if TARGET_LANG != "ru":
    # 	raise ValueError("TARGET_LANG variable must contain one of {%s}, but has `%s`" % (str(SUPPORTED_LANGS), TARGET_LANG))

    grammemes = ('nomn', 'gent')
    assert case in grammemes, "Unknown case: " + case
    res = {
        "comment": ("// ",),
        "algorithm": ("алгоритм", "алгоритма"),
        "program" : ("программа", "программы"),
        "func" 		: ("функция", "функции"),
        "func_call" : ("вызов функции", "вызова функции"),
        "alternative" : ("развилка", "развилки"),
        "branch" 	: ("ветка", "ветки"),
        "cond" 		: ("условие", "условия"),
        "cond of" 		: ("условие", "условия"),
        "if" 		: ("если", ),
        "else if" 	: ("иначе если", ),
        "else-if" 	: ("иначе если", ),
        "else" 		: ("иначе", ),
        "(branch) else" : ("иначe", ), # (e латинск.)
        "while" 	: ("пока", ),
        "do" 		: ("делать", ),
        "for" 		: ("для", ),
        "foreach" 	: ("для каждого", ),
        "in" 		: ("в", ),
        "trace" 	: ("трасса", ),
        "nth time" 	: ("-й раз", ),
        "True" 		: ("истина", ),
        "False" 	: ("ложь", ),
        True 		: ("истина", ),
        False 		: ("ложь", ),
        "None"		: ("ничего!", ),
        None		: ("ничего!", ),
        "not evaluated"		: ("не вычислено", ),
        "(she) started" 	: ("началась", ),
        "(she) finished"	: ("закончилась", ),
        "(he) started" 		: ("начался", ),
        "(he) finished" 	: ("закончился", ),
        "(it) started" 		: ("началось", ),
        "(it) finished" 	: ("закончилось", ),
        "(she) performed" 	: ("выполнилась", ),
        "(he) performed" 	: ("выполнился", ),
        "(it) performed" 	: ("выполнилось", ),
        "iteration" 	: ("итерация", "итерации"),
        "loop" 			: ("цикл", "цикла"),
        "init" 			: ("инициализация", ),
        "update" 		: ("переход", ),
        "from" 		: ("от", ),
        "to" 		: ("до", ),
        "with step" : ("с шагом", ),
        # "container is not empty"	: ("контейнер не пуст", ),
        "first element exists" 		: ("первый элемент существует", ),
        "next element exists" 		: ("следующий элемент существует", ),
        "to first element" 			: ("к первому элементу", ),
        "to next element" 			: ("к следующему элементу", ),
        "sequence" 			: ("следование", "следования"),
        "stmt"				: ("действие", "действия", ),
    }.get(word_en, ())
    try:
        return res[grammemes.index(case)]
    except IndexError:
        print("tr(%s, %s) error ! " %(word_en, case))
        return "==>%s.%s not found!<== " % (word_en, case)


def to_dict_or_self(jn, object_method_name="to_dict"):
    if hasattr(jn, object_method_name):
        mtd = getattr(jn, object_method_name)
        if hasattr(mtd, "__call__"):
            return mtd()
    return jn  # the default


def stringify(obj, trace_format=True, _visitor=None):
    if not trace_format:
        return json.dumps(obj, ensure_ascii=False, indent=None if _visitor else 2)
    visitor = _visitor or TextVisitor("  " * 2)

    if isinstance(obj, list):
        visitor.add_line("[").indent()
        for i, item in enumerate(obj):
            if i > 0:
                visitor.append_at_line(",")
            stringify(item, trace_format=True, _visitor=visitor)

        visitor.unindent().add_line("]")
    else:
        visitor.add_line(stringify(obj, trace_format=False, _visitor=visitor))

    if not _visitor:
        return str(visitor)


# ========= helper classes ========

class GlobalCounter:
    # "static" field:
    N_of_item = {}  # item -> int

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

    def count_item(self, item='any') -> int:
        """ self.register_act("my_item") -> int: number of the item appearance (n of item) """
        count = self.N_of_item.get(item, 0)
        self.N_of_item[item] = count + 1
        # print("__registered item: ", item, "#", count + 1)
        return self.N_of_item[item]

    def reset_count_of_item(self, item='any', value=0):
        self.N_of_item[item] = value

    def clear_count_of_all_items(self):
        self.N_of_item.clear()


class WithID:
    _maxID = 1

    def __init__(self, id=None, *args, **kw):
        super().__init__(*args, **kw)
        self.ID = None
        self.makeID(id)

    def newID(self, existing_id=None):
        if existing_id:
            assert isinstance(existing_id, int), existing_id
            WithID._maxID = max(WithID._maxID + 1, int(existing_id))
        else:
            WithID._maxID += 1
        return WithID._maxID

    def makeID(self, existing_id=None):
        if self.ID == None:
            self.ID = WithID.newID(existing_id)

    def to_dict(self):
        # super(?)
        return {"id": self.ID}


# ========= visitor classes ========

class TextVisitor(object):
    """ builds text by visiting JsonNodes """

    def __init__(self, indent=" " * 4):
        self.lines = []
        self.indent_level = 0
        self.indent_str = indent

    def visit(self, obj_or_str, same_line=False):
        if hasattr(obj_or_str, "accept"):
            obj_or_str.accept(self)
        else:
            if same_line:
                self.append_at_line(obj_or_str)
            else:
                self.add_line(obj_or_str)
        return self

    def accept_line_list(self, obj_or_str_list, same_line=False):
        for obj_or_str in obj_or_str_list:
            self.visit(obj_or_str, same_line=same_line)
        return self

    def add_line(self, line=""):
        self.lines.append(self.indent_str * self.indent_level + line)
        return self

    def current_line_index(self):
        return len(self.lines)  # - 1 ?? логично...

    def append_at_line(self, str_="", line_index=-1):
        if not self.lines:
            self.lines = [""]
        self.lines[line_index] += str_
        return self

    def indent(self, count=1):
        self.indent_level += count
        assert self.indent_level >= 0
        return self

    def unindent(self, count=1):
        self.indent_level -= count
        assert self.indent_level >= 0
        return self

    def begin_block(self):
        self.add_line("{").indent()  # customize the block style here
        return self

    def end_block(self):
        self.unindent().add_line("}")
        return self

    def __str__(self):
        return "\n".join(self.lines)


class AlgTextVisitor(TextVisitor):
    """ builds an algorithm text by visiting JsonNodes """
    pass


class TraceTextVisitor(TextVisitor):
    """ builds trace text by visiting JsonNodes """

    def __init__(self, condition_values="0100"):
        super().__init__()
        self.acts_of_stmt = {}  # stmt_id -> int

        def _gen(states_str):
            for ch in states_str:
                yield bool(int(ch))
            while 1:
                yield False

        self.condition_value_generator = _gen(condition_values)
        self.last_cond_tuple = (-1, False)

    def register_act(self, stmt_id='any'):
        """ self.register_act("my_stmt") -> int: number of the stmt execution (n of act) """
        count = self.acts_of_stmt.get(stmt_id, 0)
        self.acts_of_stmt[stmt_id] = count + 1
        # print("__registered: ", stmt_id, "#", count + 1)
        return self.acts_of_stmt[stmt_id]

    def next_cond_value(self):
        i, _ = self.last_cond_tuple
        v = next(self.condition_value_generator)
        v = bool(v)
        self.last_cond_tuple = (i + 1, v)
        return v

    @classmethod
    def format_nth_str(self, n=-1):
        """ if n <= 0, return empty string """
        return (" %d%s" % (n, tr("nth time"))) if n > 0 else ''

    def append_nth_str(self, n=-1):
        """ if n <= 0, do nothing  """
        if n > 0:
            self.append_at_line(self.format_nth_str(n))
        return self


class JsonVisitor(object):
    """ (abstract class) builds objects tree by visiting algorithm JsonNodes """

    def __init__(self):
        super().__init__()
        self.root = None
        self.stack = []

    def visit(self, obj_or_str):
        if hasattr(obj_or_str, "accept"):
            obj_or_str.accept(self)
        else:
            self.visit_fallback(obj_or_str)
        return self

    def visit_fallback(self, obj_or_str):
        "Called when an object cannot be visited normally"
        pass  # do nothing

    def visit_list(self, obj_or_str_list):
        for obj_or_str in obj_or_str_list:
            self.visit(obj_or_str)
        return self


class TraceJsonVisitor(JsonVisitor):
    """ builds trace objects tree by visiting algorithm JsonNodes """

    def __init__(self, condition_values="0100"):
        super().__init__()

        def _gen(states_str):
            for ch in states_str:
                yield bool(int(ch))
            while 1:
                yield 0

        self.condition_value_generator = _gen(condition_values)
        self.last_cond_tuple = (-1, False)

    def visit_fallback(self, obj_or_str):
        # "Called when an object cannot be visited normally"
        self.add_act(ActLine(obj_or_str))

    def next_cond_value(self):
        i, _ = self.last_cond_tuple
        v = next(self.condition_value_generator)
        v = bool(v)
        self.last_cond_tuple = (i + 1, v)
        return v

    def add_act(self, act, enter=False):
        if self.root is None:
            self.root = act
        # return
        elif not self.stack:  # empty
            raise Exception("TraceJsonVisitor.add_act(): Cannot add act after root")
        else:
            self.current_act().acts.append(act)
        if enter:
            self.enter_act(act)

    def current_act(self):  # as top
        assert self.stack, "acts stack is empty"
        return self.stack[-1]

    def enter_act(self, compound_act):  # as push
        assert hasattr(compound_act, "acts"), "CompoundActNode instance expected"
        self.stack.append(compound_act)
        # print("__stack push: ", [len(n.acts) for n in self.stack])
        return compound_act

    def leave_current_act(self):  # as pop
        # print("__stack pop : ", [len(n.acts) for n in self.stack])
        return self.stack.pop()


class JsonNode(object):
    """ JsonNode is base for all json-encoded nodes """

    def __init__(self, jn_type="unkn", name="noname"):
        super(JsonNode, self).__init__()
        self.parent = None
        self.jn_type = jn_type
        self.name = name
        self.data = {}  # arbitrary data to share with children

    def setup(self, parent_node, setup_children=True):
        """ Точка входа для настройки узлов после первичного создания всего дерева.
        setup_children() - универсальный этап настройки дочерних узлов, который должен вызван подклассом, или в реализации по умолчанию, или самостоятельно, после собственной настройки (тогда в setup() сперва подайте setup_children=False). """
        # assert parent_node
        # print(self.__class__.__name__, ' .set_parent: ', parent_node.__class__.__name__)
        self.parent = parent_node
        # повторить в переопределении метода setup (в подклассе)
        if setup_children: self.setup_children()

    def setup_children(self):
        """ для всех дочерних объектов дерева, в т.ч. в массивах, вызвать инициализацию (setup) """
        for child in self.get_children():
            child.setup(self)

    def get_children(self):
        """ пройтись по всем полям, и для всех под-объектов дерева, в т.ч. в массивах, вернуть объекты нашего дерева """
        children = []
        for k in vars(self):  # ! переопределение стандартных методов типа __dict__ ломает vars(self)
            if k in ('parent',
                     'owner'):  # !!! ходим только по дочерним данным, игнорируя все где-либо определёные указатели на родительские узлы!
                continue
            val = getattr(self, k)
            if isinstance(val, JsonNode):
                children.append(val)
            elif isinstance(val, list):
                for item in val:
                    if isinstance(item, JsonNode):
                        children.append(item)
        return children

    def search_up(self, node_class_or_func=None):
        """ Поиск верх по иерархии: или по типу (классу) узла, либо вызывая предикат с 1 параметром - объектом узла в иерархии.
        Если None, то возвращает корень дерева. """
        is_me = False
        if node_class_or_func is None:
            is_me = not (self.parent) or self.parent == self
        elif hasattr(node_class_or_func, '__call__'):
            is_me = node_class_or_func(self)
        else:
            is_me = isinstance(self, node_class_or_func)
        if is_me:
            return self
        elif self.parent:
            return self.parent.search_up(node_class_or_func)
        else:
            print('!!! %s could not be found in the tree!' % node_class_or_func.__name__);
            return None

    def to_dict(self):
        """ Преобразование к простым словарям и массивам, для сериализации в JSON """
        return {self.jn_type: None}

    @classmethod
    def parse(cls, json_data):
        """ json_data : JSON string, or python dict parsed from JSON representation """
        if isinstance(json_data, str):
            print("parsing plain json...")
            json_data = cls.parse_json(json_data)

        return cls.parse_element(json_data)

    @classmethod
    def parse_json(cls, text):
        return json.loads(text)

    @classmethod
    def nodes_tro(cls):
        "To be redefined in subclasses"
        return []  # _alg_node_map

    @classmethod
    def any_node_tro(cls):
        "To be redefined in subclasses"
        return TypeRecognizeOption()  # _any_alg_node_option

    @classmethod
    def parse_element(cls, json_node):
        """ json_node : dict parsed from JSON representation """
        if isinstance(json_node, str):
            # print('str:', json_node)
            return json_node

        if isinstance(json_node, list):
            return list(map(cls.parse_element, json_node))

        if not isinstance(json_node, dict):
            raise Exception("`json_node` must be dict or list or str, not  `%s`" % str(json_node))

        keys = set(json_node.keys())
        # print('keys:', keys)

        using_tro = None  # a TypeRecognizeOption

        _any_node_option = cls.any_node_tro()
        for tro in cls.nodes_tro():
            mandatory = tro.mandatory | _any_node_option.mandatory
            optional = tro.optional | _any_node_option.optional
            forbidden = tro.forbidden | _any_node_option.forbidden

            # проверим, что всё на месте, и нет ничего лишнего
            if not (mandatory - keys) and not (forbidden & keys) and not (keys - mandatory - optional):
                using_tro = tro
                break

        if not using_tro:
            raise Exception("cannot resolve json_node with following keys:  `%s`" % str(keys))

        ###
        # print('-->', tro.args)

        values_dict = {}  # дочерние узлы - параметры для конструктора

        # наполним словарь значениями для всех ключей
        for k in keys:
            values_dict[k] = cls.parse_element(json_node[k])

        # создадим элемент дерева вызовом callback"а
        values_dict.update(using_tro.args)
        return using_tro.callback(**values_dict)


# def accept(self, visitor):
# 	return visitor.visit_JsonNode(self)


class GenericAlgorithmJsonNode(JsonNode, WithID):
    def __init__(self, *args, expand_act="auto", noexpand_act="auto", **kw):
        super().__init__(*args, **kw)
        self.expand_act = expand_act
        self.noexpand_act = noexpand_act
        self.gen = 'she'  # род (м., ж., ср.) для акта элемента в трассе на рус. яз. (can be redefined)
        self.act_line_format_str = "{name} {phase_str}{nth_str}"  # can be redefined

    def list_expand_strs2Stmts(self, seq):
        return [
            StatementAtomJN("stmt", json_node) if isinstance(json_node, str) else json_node
            for json_node in seq
        ]

    def display_name(self, case='nomn', include_type_only=False):
        """ Получение имени для отображения, например, "развилка_5", "функция main", "ветка иначе".
        Для смены символа связки нужно задать поле `self.display_name_delimeter` """
        delim = ' '  # связка по умолчанию
        if hasattr(self, "display_name_delimeter"):
            delim = self.display_name_delimeter
        if include_type_only:
            return tr(self.jn_type, case)
        else:
            return tr(self.jn_type, case) + delim + self.name

    # return tr(self.jn_type, case) + delim + self.name
    @classmethod
    def nodes_tro(cls):
        return _alg_node_map

    @classmethod
    def any_node_tro(cls):
        return _any_alg_node_option

    def to_dict_4onto(self):
        """Minimalistic to_dict() """
        d = {"id": self.ID, "type": self.jn_type}
        d.update({f: getattr(self, f) for f in ("name",)})
        d.update(self.fields_to_dict())
        d.update(self.children_to_dict())
        return d

    def fields_to_dict(self):
        return {}

    def children_to_dict(self):
        return {}

    def make_act_line(self, phase='performed', n=0, format_str=None, **kwargs):
        if 'name' not in kwargs:
            name = self.display_name()
        if 'phase_str' not in kwargs:
            if '(' not in phase:  # 'performed' but not '(she) performed'
                phase = '(%s) %s' % (self.gen, phase)
            phase_str = tr(phase)
        nth_str = TraceTextVisitor.format_nth_str(n)
        return (format_str or self.act_line_format_str).format(**locals(), **kwargs)

    def accept(self, visitor):
        return visitor.visit_GenericAlgorithmJsonNode(self)


if AlgTextVisitor:
    def _(self, node):
        self.add_line(node.display_name())
        return self


    AlgTextVisitor.visit_GenericAlgorithmJsonNode = _
if TraceTextVisitor:
    def _(self, node):
        self.register_act(node.display_name())
        return self


    TraceTextVisitor.visit_GenericAlgorithmJsonNode = _


class AlgorithmRootJN(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", algorithm=None, noexpand_types=None, **kw):
        super(AlgorithmRootJN, self).__init__(jn_type, name='algorithm', **kw)
        assert jn_type == "algorithm", jn_type
        assert algorithm
        self.funcs_and_stmts = self.list_expand_strs2Stmts(algorithm)
        # self.data["functions"] = []
        # self.data["stmts"] = []
        self.noexpand_types = noexpand_types
        # обновить всё созданное дерево (точка входа, в других классах сами не вызываем!)
        self.setup(parent_node=None, setup_children=True)

        # разделим функции и глобальный код
        if "functions" not in self.data:  # функций не было найдено и зарегистрировано
            self.data["functions"] = []
        stmts = [st for st in self.funcs_and_stmts if st.jn_type != 'func']
        self.data["stmts"] = SequenceJN(stmts, name="global_code")
        self.act_line_format_str = "{phase_str} {name}"

    def to_dict(self):
        return {self.jn_type: [to_dict_or_self(ch) for ch in self.funcs_and_stmts]}

    def children_to_dict(self):
        # return {"program": [to_dict_or_self(ch,"to_dict_4onto") for ch in self.funcs_and_stmts]}
        return {"functions": [to_dict_or_self(ch, "to_dict_4onto") for ch in self.data["functions"]],
                "stmts": self.data["stmts"].to_dict_4onto()
                }

    def get_entry_node(self):
        """ -> func node, or list of statements """
        # ищем функцию - точку входа
        if "functions" in self.data:
            for func in self.data["functions"]:
                if func.is_entry:
                    return func
        # # функции нет - собираем все операторы верхнего уровня
        if self.data["stmts"]:
            return self.data["stmts"]
        # stmts = [st for st in self.funcs_and_stmts if st.jn_type != 'func']
        # if stmts:
        # 	return stmts

        # операторов верхнего уровня тоже нет
        return None

    def display_name(self, case='nomn'):
        return tr("program")

    def accept(self, visitor):
        return visitor.visit_AlgorithmRootJN(self)


if AlgTextVisitor:
    def _(self, node):
        self.add_line(tr("comment") + tr(node.jn_type))
        # self.begin_block()
        self.add_line("{")
        for el in node.funcs_and_stmts:
            el.accept(self)
        self.add_line("}")
        self.add_line()
        # self.end_block()
        return self


    AlgTextVisitor.visit_AlgorithmRootJN = _
if TraceTextVisitor:
    def _(self, node):
        # self.register_act(node.display_name())
        self.add_line(tr("comment") + tr("trace") + " ")
        self.add_line("{")
        # self.add_line("%s %s" % (tr("(she) started"), tr("program")))
        self.add_line(node.make_act_line("started", n=0))
        inner = node.get_entry_node()
        if inner:
            if isinstance(inner, list):
                self.indent()
                self.accept_line_list(inner)
                self.unindent()
            else:
                self.visit(inner)
        # self.add_line("%s %s" % (tr("(she) finished"), tr("program")))
        self.add_line(node.make_act_line("finished", n=0))
        self.add_line("}")
        return self


    TraceTextVisitor.visit_AlgorithmRootJN = _
if TraceJsonVisitor:
    def _(self, node):
        program = ActLine(tr("program"), gen="she", n=None, executes=node.ID, appearance="reversed")
        self.add_act(CompoundActNode(program), enter=True)

        inner = node.get_entry_node()
        if inner:
            if isinstance(inner, list):
                self.visit_list(inner)
            else:
                self.visit(inner)

        self.leave_current_act()


    TraceJsonVisitor.visit_AlgorithmRootJN = _


class StatementAtomJN(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", name='noname', **kw):
        super().__init__(jn_type, name=name, **kw)
        assert jn_type == "stmt", jn_type
        self.gen = 'it'

    def to_dict(self):
        return self.name

    def accept(self, visitor):
        return visitor.visit_StatementAtomJN(self)


if AlgTextVisitor:
    def _(self, node):
        self.add_line(node.name)
        return self


    AlgTextVisitor.visit_StatementAtomJN = _
if TraceTextVisitor:
    def _(self, node):
        # Пример:    печатать_минус выполнилось 1-й раз
        i = self.register_act(node.name)
        # self.add_line("%s %s %d%s" % (node.name, tr("(it) performed"), i, tr("nth time")))
        self.add_line(node.make_act_line(name=node.name, phase="performed", n=i))
        return self


    TraceTextVisitor.visit_StatementAtomJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = ActLine(node.name, executes=node.ID)
        self.add_act(act)


    TraceJsonVisitor.visit_StatementAtomJN = _


class NameOnlyStatementJN(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", name='noname', **kw):
        super().__init__(jn_type, name=name, **kw)
        assert jn_type in ("break", "continue", "return",), jn_type
        self.gen = 'it'

    def to_dict(self):
        return self.name

    def accept(self, visitor):
        return visitor.visit_NameOnlyStatementJN(self)

    def display_name(self, case='nomn', include_type_only=False):
        return self.name


if AlgTextVisitor:
    def _(self, node):
        self.add_line(node.name)
        return self


    AlgTextVisitor.visit_NameOnlyStatementJN = _
if TraceTextVisitor:
    def _(self, node):
        # Пример:    return -1 выполнилось 1-й раз
        i = self.register_act(node.name)
        self.add_line(node.make_act_line(name=node.name, phase="performed", n=i))
        return self


    TraceTextVisitor.visit_NameOnlyStatementJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = ActLine(node.name, executes=node.ID)
        self.add_act(act)


    TraceJsonVisitor.visit_NameOnlyStatementJN = _


class FuncJN(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", func="noname", body=None, is_entry=None, param_list=None, **kw):
        super(FuncJN, self).__init__(jn_type, name=func, **kw)
        assert jn_type == "func", jn_type
        self.body = self.list_expand_strs2Stmts(body)
        if is_entry is not None:
            # self.is_entry = not (str(is_entry).lower() in ('false', "no", "0"))
            self.is_entry = (str(is_entry).lower() in ('true', "yes", "1"))
        else:
            self.is_entry = False

        self.param_list = param_list  # or []

    def setup(self, parent_node, setup_children=True):
        super(FuncJN, self).setup(parent_node, setup_children=False)
        if self.is_entry is None:
            # по умолчанию, в алгоритме точка входа одна - main()
            self.is_entry = self.name == 'main'
            print('"main" is entry!')
        # print('"main".is_entry', self.is_entry)
        root = self.search_up()
        root.data["functions"] = root.data.get("functions", []) + [self]
        if setup_children: self.setup_children()

    def to_dict(self):
        """ Преобразование к простым словарям и массивам, для сериализации в JSON """
        return {self.jn_type: self.name,
                "is_entry": self.is_entry,
                "param_list": self.param_list,
                "body": [to_dict_or_self(ch) for ch in self.body]}

    def fields_to_dict(self):
        return {
            "is_entry": self.is_entry,
            "param_list": self.param_list,
        }

    def children_to_dict(self):
        return {
            "body": [to_dict_or_self(ch, "to_dict_4onto") for ch in self.body]
        }

    def accept(self, visitor):
        return visitor.visit_FuncJN(self)


if AlgTextVisitor:
    def _(self, node):
        self.add_line(node.display_name())  # добавить параметры, когда понадобится
        self.begin_block()
        self.accept_line_list(node.body)
        self.end_block()
        return self


    AlgTextVisitor.visit_FuncJN = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s %s" % (tr("(she) started"), tr(node.jn_type), node.name)).append_nth_str(i)
        self.add_line("%s %s" % (tr("(she) started"), node.display_name())).append_nth_str(i)
        if node.body:
            self.indent()
            self.accept_line_list(node.body)
            self.unindent()
        self.add_line("%s %s" % (tr("(she) finished"), node.display_name())).append_nth_str(i)
        return self


    TraceTextVisitor.visit_FuncJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("func", node.name, gen="she", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)
        if node.body:
            self.visit_list(node.body)
        self.leave_current_act()


    TraceJsonVisitor.visit_FuncJN = _


class FuncCallJN(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", func_name="func_name", func_args='()', **kw):
        super(FuncCallJN, self).__init__(jn_type, name=func_name.strip() + func_args.strip(), **kw)
        assert jn_type == "func_call", jn_type
        self.func_name = func_name
        self.func_args = func_args  # string, not list so far
        self.func = None
        self.gen = 'he'

    def setup(self, parent_node, setup_children=True):
        super(FuncCallJN, self).setup(parent_node, setup_children=False)
        root = self.search_up()
        functions = root.data.get("functions", [])
        if functions := [f for f in functions if f['name'] == self.func_name]:
            self.func = functions[0]

        if setup_children: self.setup_children()

    def to_dict(self):
        """ Преобразование к простым словарям и массивам, для сериализации в JSON """
        return {"type": self.jn_type,
                "name": self.name,
                "func_name": self.func_name,
                "func_args": self.func_args,
               }

    def accept(self, visitor):
        return visitor.visit_FuncCallJN(self)


if AlgTextVisitor: pass
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name() + '_started')
        # self.add_line("%s %s %s" % (tr("(she) started"), tr(node.jn_type), node.name)).append_nth_str(i)
        self.add_line("%s %s" % (tr("(he) started"), node.display_name())).append_nth_str(i)
        if node.func.body:
            self.indent()
            self.accept_line_list(node.body)
            self.unindent()
        i = self.register_act(node.display_name() + '_finished')
        self.add_line("%s %s" % (tr("(he) finished"), node.display_name())).append_nth_str(i)
        return self


    TraceTextVisitor.visit_FuncCallJN = _
if TraceJsonVisitor: pass


class AlternativeJN(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", alternative=None, alt='noname', branches=None, **kw):
        super(AlternativeJN, self).__init__(jn_type, name=alternative or alt, **kw)
        assert jn_type == "alternative", jn_type
        self.branches = branches
        self.act_line_format_str = "{phase_str} {name}{nth_str}"

    def setup(self, parent_node, setup_children=True):
        super().setup(parent_node, setup_children=False)
        root = self.search_up()
        root.data["alternatives"] = root.data.get("alternatives", [])  # ensure existence
        if self.name in ("", "-"):
            # здесь надо применять стратегию выбора имени, + уникальность имени
            i = 1 + len(root.data["alternatives"])
            self.name = str(i)
        # self.name = "развилка_%d" % i
        root.data["alternatives"] += [self]
        if setup_children: self.setup_children()

    def to_dict(self):
        return {self.jn_type: self.name,
                "branches": [to_dict_or_self(ch) for ch in self.branches]}

    def children_to_dict(self):
        return {"branches": [to_dict_or_self(ch, "to_dict_4onto") for ch in self.branches]}

    def accept(self, visitor):
        return visitor.visit_AlternativeJN(self)


if AlgTextVisitor:
    def _(self, node):
        i = self.current_line_index()
        self.accept_line_list(node.branches)
        # дописать имя справа от "если"
        self.append_at_line("  " + tr("comment") + node.name, i)
        return self


    AlgTextVisitor.visit_AlternativeJN = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s" % (tr("(she) started"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        if node.branches:
            self.indent()

            for branch in node.branches:
                branch.accept(self)
                if self.last_cond_tuple[1] == True:
                    break

            self.unindent()
        # self.add_line("%s %s" % (tr("(she) finished"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_AlternativeJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("alternative", node.name, gen="she", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.branches:
            for branch in node.branches:
                branch.accept(self)  # self.visit(branch)
                if self.last_cond_tuple[1] == True:
                    break

        self.leave_current_act()


    TraceJsonVisitor.visit_AlternativeJN = _


class GenericAlternativeBranch(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", stmt=None, **kw):
        super(GenericAlternativeBranch, self).__init__(jn_type, name="noname", **kw)
        assert jn_type in ("if", "else if", "else"), jn_type
        assert stmt
        self.stmts = self.list_expand_strs2Stmts(stmt)

    def children_to_dict(self):
        return {"branch": [to_dict_or_self(ch, "to_dict_4onto") for ch in self.stmts]}

    def accept(self, visitor):
        return visitor.visit_GenericAlternativeBranch(self)


if AlgTextVisitor:
    def _(self, node):
        """ Ввести только тело ветки ! (проставив блок или только отступы для единственного действия) """
        if len(node.stmts) == 1:
            self.indent().visit(node.stmts[0]).unindent()
        else:
            self.begin_block()
            self.accept_line_list(node.stmts)
            self.end_block()
        return self


    AlgTextVisitor.visit_GenericAlternativeBranch = _
if TraceTextVisitor:
    def _(self, node):
        # make indented block of the branch's body
        if node.stmts:
            self.indent()
            self.accept_line_list(node.stmts)
            self.unindent()
        return self


    TraceTextVisitor.visit_GenericAlternativeBranch = _


class GenericCondition(GenericAlgorithmJsonNode):
    def __init__(self, cond=None, owner=None, name="", **kw):
        super(GenericCondition, self).__init__("cond", name=name, **kw)
        self.cond = cond
        self.owner = owner
        self.gen = 'it'
        self.act_line_format_str = "{name} {phase_str}{nth_str} - {value}"

    def setup(self, parent_node, setup_children=True):
        super(GenericCondition, self).setup(parent_node, setup_children=False)
        assert self.owner
        if self.cond == "-":
            self.cond = ""  # обнулить условие для определённости
        if setup_children: self.setup_children()  # может впоследствии понадобиться при разборе внутренностей выражений

    def display_name(self, case='nomn'):
        if self.cond:
            return "%s %s (%s)" % (
                tr("cond of", case), self.owner.display_name('gent', include_type_only=True), self.cond)
        else:
            return "%s %s" % (tr("cond", case), self.name)

    # return "%s %s%s %s" % (tr("cond", case), self.name, insert_cond, self.owner.display_name('gent'))
    def accept(self, visitor):
        return visitor.visit_GenericCondition(self)


if AlgTextVisitor:
    def _(visitor, node):
        """ Например: добавит "X>0" на строке и получится "иначе если X>0" """
        visitor.append_at_line(node.cond or node.name)
        return visitor


    AlgTextVisitor.visit_GenericCondition = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        v = self.next_cond_value()
        # self.add_line("%s %s" % (node.display_name(), tr("(it) performed"))).append_nth_str(i).append_at_line(" - " + tr(v))
        self.add_line(node.make_act_line("performed", i, value=tr(v)))

        return self


    TraceTextVisitor.visit_GenericCondition = _
if TraceJsonVisitor:
    def _(self, node):
        # i = self.register_act(node.display_name())
        v = self.next_cond_value()
        owner_type = "alternative" if node.owner.jn_type == "alternative" else "loop"
        act = MultiWordActLine([
            {"tr": "cond"},
            {"tr": owner_type, "case": "gent"},
            {"word": node.cond, "parens": 1},
        ], value={"tr": v}, gen="it", executes=node.ID)
        self.add_act(act)


    # self.add_act(CompoundActNode(act), enter=False)
    # self.leave_current_act()

    TraceJsonVisitor.visit_GenericCondition = _


class ConditionalAlternativeBranch(GenericAlternativeBranch):
    def __init__(self, jn_type="unkn", cond=None, stmt=None, **kw):
        super(ConditionalAlternativeBranch, self).__init__(jn_type, stmt=stmt, **kw)
        assert jn_type in ("if", "else if"), jn_type
        self.cond = cond

    def setup(self, parent_node, setup_children=True):
        super().setup(parent_node, setup_children=False)
        assert isinstance(self.parent, AlternativeJN)
        # Здесь нумерация не изменится на другой способ именования
        i = 1 + self.parent.branches.index(self)  # все ветки уже добавлены к альтернативе
        self.name = str(i)
        self.cond_obj = GenericCondition(self.cond, owner=self.parent, name=self.name)
        if setup_children: self.setup_children()

    def display_name(self, case='nomn'):
        return "%s %s" % (tr("branch", case), self.cond_obj.display_name('gent'))

    def to_dict(self):
        """ for conditional branches only """
        return {self.jn_type: self.cond,
                "then": [to_dict_or_self(ch) for ch in self.stmts]}

    def fields_to_dict(self):
        return {"cond": self.cond}

    def accept(self, visitor):
        return visitor.visit_ConditionalAlternativeBranch(self)


if AlgTextVisitor:
    def _(visitor, node):
        """ Вывести заголовок ветки, а тело - вызвав базовый класс """
        visitor.add_line(tr(node.jn_type) + " ").visit(node.cond_obj)
        super(ConditionalAlternativeBranch, node).accept(visitor)
        return visitor


    AlgTextVisitor.visit_ConditionalAlternativeBranch = _
if TraceTextVisitor:
    def _(self, node):
        node.cond_obj.accept(self)
        _, cond_v = self.last_cond_tuple
        if cond_v:
            i = self.register_act(node.display_name())
            # self.add_line("%s %s" % (node.display_name(), tr("(she) started"))).append_nth_str(i)
            self.add_line(node.make_act_line("started", i))
            super(ConditionalAlternativeBranch, node).accept(self)  # show branch contents
            # self.add_line("%s %s" % (node.display_name(), tr("(she) finished"))).append_nth_str(i)
            self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_ConditionalAlternativeBranch = _
if TraceJsonVisitor:
    def _(self, node):
        node.cond_obj.accept(self)
        _, cond_v = self.last_cond_tuple

        if cond_v:
            act = MultiWordActLine([
                {"tr": "branch"},
                {"tr": "cond", "case": "gent"},
                {"word": node.cond, "parens": 1},
            ], appearance="normal", gen="she", executes=node.ID)
            self.add_act(CompoundActNode(act), enter=True)

            if node.stmts:
                self.visit_list(node.stmts)
            self.leave_current_act()


    TraceJsonVisitor.visit_ConditionalAlternativeBranch = _


class IfBranchJN(ConditionalAlternativeBranch):
    def __init__(self, jn_type="unkn", then=None, **kw):
        super(IfBranchJN, self).__init__(jn_type, cond=kw["if"], stmt=then, **{k: kw[k] for k in kw if k != "if"})
        assert jn_type == "if", jn_type


class ElseIfBranchJN(ConditionalAlternativeBranch):
    def __init__(self, jn_type="unkn", then=None, **kw):
        super(ElseIfBranchJN, self).__init__(jn_type, cond=kw["else if"], stmt=then,
                                             **{k: kw[k] for k in kw if k != "else if"})
        assert jn_type == "else if", jn_type


class ElseBranchJN(GenericAlternativeBranch):
    def __init__(self, jn_type="unkn", **kw):
        super(ElseBranchJN, self).__init__(jn_type, stmt=kw["else"], **{k: kw[k] for k in kw if k != "else"})
        assert jn_type == "else", jn_type

    def display_name(self, case='nomn'):
        return "%s %s" % (tr("branch", case), tr("(branch) else"))

    def to_dict(self):
        """ redefine for UNconditional branch """
        return {self.jn_type: [to_dict_or_self(ch) for ch in self.stmts]}

    def accept(self, visitor):
        """ Вывести заголовок ветки, а тело - вызвав базовый класс """
        return visitor.visit_ElseBranchJN(self)


if AlgTextVisitor:
    def _(visitor, node):
        visitor.add_line(tr(node.jn_type))
        super(ElseBranchJN, node).accept(visitor)
        return visitor


    AlgTextVisitor.visit_ElseBranchJN = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s" % (node.display_name(), tr("(she) started"))).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        super(ElseBranchJN, node).accept(self)  # show branch contents
        # self.add_line("%s %s" % (node.display_name(), tr("(she) finished"))).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_ElseBranchJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = MultiWordActLine([
            {"tr": "branch"},
            {"tr": "(branch) else"},
        ], gen="she", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.stmts:
            self.visit_list(node.stmts)
        self.leave_current_act()


    TraceJsonVisitor.visit_ElseBranchJN = _


class GenericLoop(GenericAlgorithmJsonNode):
    def __init__(self, jn_type="unkn", name="noname", body=None, **kw):
        super(GenericLoop, self).__init__(jn_type, name, **kw)
        assert jn_type in ("while", "do while", "for", "foreach"), jn_type
        assert body
        self.body = self.list_expand_strs2Stmts(body)
        self.gen = 'he'
        self.act_line_format_str = "{phase_str} {name}{nth_str}"

    def to_dict(self):
        return {"name": self.name,
                "body": [to_dict_or_self(ch) for ch in self.body]}

    def children_to_dict(self):
        return {
            "body": [to_dict_or_self(ch, "to_dict_4onto") for ch in self.body]
        }

    def display_name(self, case='nomn', include_type_only=False):
        if include_type_only:
            return tr("loop", case)
        else:
            return tr("loop", case) + " " + self.name  # + super().display_name()

    def iteration_name(self, n=0):
        return tr("iteration") + (" %d " % n) + self.display_name('gent')

    def make_iteration_act_line(self, phase, n=1):
        return self.make_act_line("(she) " + phase, name=self.iteration_name(n), format_str=None)

    def accept(self, visitor):
        return visitor.visit_GenericLoop(self)


if AlgTextVisitor:
    def _(visitor, node):
        """ Ввести только имя и тело цикла ! (вызывать только после записи заголовка на строке) """
        # i = visitor.current_line_index()
        # visitor.accept_line_list(self.branches)
        # дописать имя справа от заголовка
        visitor.append_at_line("  " + tr("comment") + node.name)
        # записать тело
        if len(node.body) == 1:
            visitor.indent().visit(node.body[0])
            visitor.unindent()
        else:
            visitor.begin_block()
            visitor.accept_line_list(node.body)
            visitor.end_block()
        return visitor


    AlgTextVisitor.visit_GenericLoop = _
if TraceTextVisitor:
    def _(self, node):
        self.acts_of_stmt[node.iteration_name()] = 0
        return self


    TraceTextVisitor.loop_reset_iterations_count = _


    def _(self, node):
        i = self.register_act(node.iteration_name())
        # self.add_line("%s %s" % (tr("(she) started"), node.iteration_name(i)))
        self.add_line(node.make_iteration_act_line("started", n=i))
        if node.body:
            self.indent()
            self.accept_line_list(node.body)
            self.unindent()
        # self.add_line("%s %s" % (tr("(she) finished"), node.iteration_name(i)))
        self.add_line(node.make_iteration_act_line("finished", n=i))
        return self


    TraceTextVisitor.loop_make_iteration = _


class ConditionalLoop(GenericLoop):
    def __init__(self, jn_type="unkn", name="noname", cond=None, body=None, **kw):
        super(ConditionalLoop, self).__init__(jn_type, name, body, **kw)
        assert jn_type in ("while", "do while", "for"), jn_type
        self.cond = cond

    def setup(self, parent_node, setup_children=True):
        super(ConditionalLoop, self).setup(parent_node, setup_children=False)
        self.cond_obj = GenericCondition(self.cond, owner=self)
        if setup_children: self.setup_children()

    def to_dict(self):
        d = {
            self.jn_type: self.cond
        }
        d.update(super(ConditionalLoop, self).to_dict())
        return d

    def fields_to_dict(self):
        return {"cond": self.cond}


class WhileJN(ConditionalLoop):
    def __init__(self, jn_type="unkn", name="noname", body=None, **kw):
        super(WhileJN, self).__init__(jn_type, name, cond=kw["while"], body=body,
                                      **{k: kw[k] for k in kw if k != "while"})
        assert jn_type == "while", jn_type

    def accept(self, visitor):
        """ Вывести заголовок цикла, а имя и тело - вызвав базовый класс """
        return visitor.visit_WhileJN(self)


if AlgTextVisitor:
    def _(visitor, node):
        visitor.add_line(tr(node.jn_type) + " ").visit(node.cond_obj)
        super(WhileJN, node).accept(visitor)
        return visitor


    AlgTextVisitor.visit_WhileJN = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s" % (tr("(he) started"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        if node.body:
            self.loop_reset_iterations_count(node)
            self.indent()

            while 1:
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break
                self.loop_make_iteration(node)

            self.unindent()
        # self.add_line("%s %s" % (tr("(he) finished"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_WhileJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("loop", node.name, gen="he", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.body:
            iter_n = 1  # нумеруем итерации с 1

            while 1:
                # check condition
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break
                # self.loop_make_iteration(node)
                act = IterationActLine(node.name, loop_act_id=node.ID, n=iter_n,
                                       executes=node.ID)  # для body нет отдельного узла!
                self.add_act(CompoundActNode(act), enter=True)
                self.visit_list(node.body)
                self.leave_current_act()
                iter_n += 1

        self.leave_current_act()


    TraceJsonVisitor.visit_WhileJN = _


class DoWhileJN(ConditionalLoop):
    def __init__(self, jn_type="unkn", name="noname", body=None, **kw):
        super(DoWhileJN, self).__init__(jn_type, name, cond=kw["do while"], body=body,
                                        **{k: kw[k] for k in kw if k != "do while"})
        assert jn_type == "do while", jn_type

    def accept(self, visitor):
        return visitor.visit_DoWhileJN(self)


if AlgTextVisitor:
    def _(visitor, node):
        """ Вывести метку начала цикла, а имя и тело - вызвав базовый класс, в конце - заголовок. """
        visitor.add_line(tr("do") + " ")
        super(DoWhileJN, node).accept(visitor)
        visitor.add_line(tr("while") + " ").visit(node.cond_obj)
        return visitor


    AlgTextVisitor.visit_DoWhileJN = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s" % (tr("(he) started"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        if node.body:
            self.loop_reset_iterations_count(node)
            self.indent()

            while 1:
                self.loop_make_iteration(node)
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break

            self.unindent()
        # self.add_line("%s %s" % (tr("(he) finished"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_DoWhileJN = _
if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("loop", node.name, gen="he", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.body:
            iter_n = 1  # нумеруем итерации с 1

            while 1:
                # self.loop_make_iteration(node)
                act = IterationActLine(node.name, loop_act_id=node.ID, n=iter_n,
                                       executes=node.ID)  # для body нет отдельного узла!
                self.add_act(CompoundActNode(act), enter=True)
                self.visit_list(node.body)
                self.leave_current_act()
                # check condition
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break
                iter_n += 1

        self.leave_current_act()


    TraceJsonVisitor.visit_DoWhileJN = _


class ForJN(ConditionalLoop):
    def __init__(self, jn_type="unkn", name="noname", body=None, **kw):
        assert "for" in kw
        self.loop_var = str(kw["for"])

        assert not (
                "from" in kw and "init" in kw), "`for by {var}` got `from` and `init` keys both. Pass one of that instead.".format(
            var=self.loop_var)
        self.range_start = kw.get("from", None)
        if self.range_start is not None:
            self.range_start = str(self.range_start)
            self.init_stmt = self.loop_var + " = " + self.range_start
        else:
            self.init_stmt = str(kw.get("init", None))
        # note that self.range_start is None here

        # `step` is not required, defaulted to 1
        self.step = str(kw.get("step", "1"))
        try:
            self.step = int(self.step)
        except Exception as e:
            raise Exception(
                "`for by {var}` got invalid value for `step`: '{val}'".format(var=self.loop_var, val=self.step))
        self.update_stmt = "{v}={v}{:+d}".format(self.step, v=self.loop_var)

        assert not (
                "to" in kw and "while" in kw), "`for by {var}` got `to` and `while` keys both. Pass one of that instead.".format(
            var=self.loop_var)
        self.range_end = kw.get("to", None)
        if self.range_end is not None:
            self.range_end = str(self.range_end)
            comp_sign = "<=" if self.step > 0 else ">="
            cond_stmt = self.loop_var + " %s " % comp_sign + self.range_end
        else:
            cond_stmt = str(kw.get("while", None))
        # note that self.range_end is None here

        # cond_stmt -> self.cond !

        # prepare act strings if not provided

        self.init_act = str(kw.get("init_act", self.init_stmt))
        self.cond_act = str(kw.get("cond_act", cond_stmt))
        self.update_act = str(kw.get("update_act", self.update_stmt))

        # call super`s constuctor
        super(ForJN, self).__init__(jn_type, name,
                                    cond=self.cond_act,
                                    body=body, **{k: kw[k] for k in kw if
                                                  k not in {"for", "from", "init", "to", "while", "step", "init_act",
                                                            "cond_act", "update_act"}})
        assert jn_type == "for", jn_type

    def fields_to_dict(self):
        return {"init": self.init_act, "cond": self.cond_act, "update": self.update_act, }

    def accept(self, visitor):
        return visitor.visit_ForJN(self)


if AlgTextVisitor:
    def _(visitor, node):
        """ Вывести метку начала цикла, а имя и тело - вызвав базовый класс, в конце - заголовок. """
        visitor.add_line(tr(node.jn_type) + " ").visit(node.loop_var, same_line=True).append_at_line(
            " " + tr("from") + " ")
        if node.range_start is not None:
            visitor.visit(str(node.range_start), same_line=True)
        else:
            visitor.visit(node.init_stmt, same_line=True)
        visitor.append_at_line(" ")

        if node.range_end is not None:
            visitor.append_at_line(tr("to") + " ").visit(str(node.range_end), same_line=True)
        else:
            visitor.append_at_line(tr("while") + " ").visit(node.cond_act, same_line=True)
        visitor.append_at_line(" ")

        visitor.append_at_line(tr("with step") + " " + ("%+d" % node.step))

        super(ForJN, node).accept(visitor)
        return visitor


    AlgTextVisitor.visit_ForJN = _
if TraceTextVisitor:  # visit
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s" % (tr("(he) started"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        if node.body:
            self.loop_reset_iterations_count(node)
            self.indent()

            init_id = tr("init") + " " + node.display_name('gent')
            init_i = self.register_act(init_id)
            self.add_line("%s %s (%s)" % (tr("(she) performed"), tr("init"), node.init_act))
            self.append_nth_str(init_i)

            while 1:
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break
                self.forloop_make_iteration(node)

            self.unindent()
        # self.add_line("%s %s" % (tr("(he) finished"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_ForJN = _


    def _(self, node):  # make_iteration
        i = self.register_act(node.iteration_name())
        # self.add_line("%s %s" % (tr("(she) started"), node.iteration_name(i)))
        self.add_line(node.make_iteration_act_line("started", n=i))
        if node.body:
            self.indent()
            self.accept_line_list(node.body)
            self.unindent()
        # self.add_line("%s %s" % (tr("(she) finished"), node.iteration_name(i)))
        self.add_line(node.make_iteration_act_line("finished", n=i))

        update_name = tr("update") + " " + node.display_name('gent')
        upd_i = self.register_act(update_name)
        # выполнился переход (шаг +1) 1-й раз
        self.add_line("%s %s (" % (tr("(he) performed"), tr("update"))).visit(node.update_act,
                                                                              same_line=True).append_at_line(
            ")").append_nth_str(upd_i)

        return self


    TraceTextVisitor.forloop_make_iteration = _
if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("loop", node.name, gen="he", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.body:
            # init act
            act = MultiWordActLine([
                {"tr": "init"},
                # {"tr":"loop", "case":"gent"},
                {"word": node.init_act, "parens": 1},
            ], gen="she", appearance="reversed", executes=node.ID)
            self.add_act(act)  # ^ для init_act нет спец. узла!

            iter_n = 1  # нумеруем итерации с 1

            while 1:
                # check condition
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break
                # self.loop_make_iteration(node)
                act = IterationActLine(node.name, loop_act_id=node.ID, n=iter_n,
                                       executes=node.ID)  # для body нет отдельного узла!
                self.add_act(CompoundActNode(act), enter=True)
                self.visit_list(node.body)
                self.leave_current_act()
                iter_n += 1
                # update act
                act = MultiWordActLine([
                    {"tr": "update"},
                    # {"tr":"loop", "case":"gent"},
                    {"word": node.update_act, "parens": 1},
                ], gen="he", appearance="reversed", executes=node.ID)  # ^ для update_act нет спец. узла!
                self.add_act(act)

        self.leave_current_act()


    TraceJsonVisitor.visit_ForJN = _


class ForEachLoopCondition(GenericCondition):
    def __init__(self, cond=None, owner=None, **kw):
        super(ForEachLoopCondition, self).__init__(cond=tr("to next element"), owner=owner, name="", **kw)
        self.is_first_time = False  # это поле нужно явно устанавливать извне

    # def setup(self, parent_node, setup_children=True): derive
    def display_name(self, case='nomn'):
        conditional_name = tr("cond") + " (%s)"
        if self.is_first_time:
            conditional_name = conditional_name % tr("first element exists")  # ? or --> "container is not empty"
        else:
            conditional_name = conditional_name % tr("next element exists")

        return conditional_name

    # if self.cond:
    # 	return "%s (%s) %s" % (tr("cond", case), self.cond, self.owner.display_name('gent'))
    # else:
    # 	return "%s %s %s" % (tr("cond", case), self.name, self.owner.display_name('gent'))
    # return "%s %s%s %s" % (tr("cond", case), self.name, insert_cond, self.owner.display_name('gent'))
    def accept(self, visitor):
        return visitor.visit_ForEachLoopCondition(self)


if AlgTextVisitor:
    # use parent's visit() method
    AlgTextVisitor.visit_ForEachLoopCondition = AlgTextVisitor.visit_GenericCondition
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name() + node.owner.display_name('gent'))
        v = self.next_cond_value()

        # self.add_line("%s %s" % (node.display_name(), tr("(it) performed"))).append_nth_str(i).append_at_line(" - " + tr(v))
        self.add_line(node.make_act_line("performed", i, value=tr(v)))
        return self


    TraceTextVisitor.visit_ForEachLoopCondition = _
if TraceJsonVisitor:
    TraceJsonVisitor.visit_ForEachLoopCondition = TraceJsonVisitor.visit_GenericCondition


class ForEachJN(GenericLoop):
    def __init__(self, jn_type="unkn", name="noname", foreach=None, body=None, **kw):
        assert "in" in kw
        super(ForEachJN, self).__init__(jn_type, name, body=body, **{k: kw[k] for k in kw if k != "in"})
        assert jn_type == "foreach", jn_type
        self.variable = foreach
        self.container = kw["in"]
        self.cond_obj = ForEachLoopCondition(owner=self)

    def to_dict(self):
        d = {
            self.jn_type: self.variable,
            "in": self.container,
        }
        d.update(super().to_dict())
        return d

    def fields_to_dict(self):
        return {"variable": self.variable, "container": self.container, }

    def accept(self, visitor):
        """ Вывести метку начала цикла, а имя и тело - вызвав базовый класс, в конце - заголовок. """
        return visitor.visit_ForEachJN(self)


if AlgTextVisitor:
    def _(visitor, node):
        visitor.add_line(tr(node.jn_type) + " ")
        visitor.visit(node.variable, same_line=True).append_at_line(" ")
        visitor.append_at_line(tr("in") + " ")
        visitor.visit(node.container, same_line=True)
        super(ForEachJN, node).accept(visitor)
        return visitor


    AlgTextVisitor.visit_ForEachJN = _
if TraceTextVisitor:
    def _(self, node):  # visit
        i = self.register_act(node.display_name())
        self.add_line("%s %s" % (tr("(he) started"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        if node.body:
            self.loop_reset_iterations_count(node)
            self.indent()
            node.cond_obj.is_first_time = True

            while 1:
                node.cond_obj.accept(self)
                if self.last_cond_tuple[1] == False:
                    break
                self.foreachloop_make_iteration(node)

                # обнулить в любом случае
                if node.cond_obj.is_first_time: node.cond_obj.is_first_time = False

            self.unindent()
        self.add_line("%s %s" % (tr("(he) finished"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_ForEachJN = _


    def _(self, node):  # make_iteration
        # выполнился переход (к первому/следующему элементу) i-й раз
        if node.cond_obj.is_first_time:
            update_command = tr("to first element")
        else:
            update_command = tr("to next element")
        update_id = tr("update") + " (" + update_command + ") " + node.display_name('gent')
        upd_i = self.register_act(update_id)
        self.add_line("%s %s (" % (tr("(he) performed"), tr("update"))).visit(update_command,
                                                                              same_line=True).append_at_line(
            ")").append_nth_str(upd_i)

        i = self.register_act(node.iteration_name())
        # self.add_line("%s %s" % (tr("(she) started"), node.iteration_name(i)))
        self.add_line(node.make_iteration_act_line("started", n=i))

        if node.body:
            self.indent()
            self.accept_line_list(node.body)
            self.unindent()
        # self.add_line("%s %s" % (tr("(she) finished"), node.iteration_name(i)))
        self.add_line(node.make_iteration_act_line("finished", n=i))

        return self


    TraceTextVisitor.foreachloop_make_iteration = _
if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("loop", node.name, gen="he", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.body:
            # check condition
            node.cond_obj.cond = tr("first element exists")
            node.cond_obj.accept(self)
            if self.last_cond_tuple[1] == False:
                pass
            else:
                node.cond_obj.cond = tr("next element exists")

                # init act
                act = MultiWordActLine([
                    {"tr": "update"},
                    # {"tr":"loop", "case":"gent"},
                    {"tr": "to first element", "parens": 1},
                ], gen="he", appearance="reversed", executes=node.ID)
                self.add_act(act)  # ^ для init_act нет спец. узла!

                iter_n = 1  # нумеруем итерации с 1

                while 1:
                    # self.loop_make_iteration(node)
                    act = IterationActLine(node.name, loop_act_id=node.ID, n=iter_n,
                                           executes=node.ID)  # для body нет отдельного узла!
                    self.add_act(CompoundActNode(act), enter=True)
                    self.visit_list(node.body)
                    self.leave_current_act()
                    iter_n += 1
                    # update act
                    act = MultiWordActLine([
                        {"tr": "update"},
                        # {"tr":"loop", "case":"gent"},
                        {"tr": "to next element", "parens": 1},
                    ], gen="he", appearance="reversed", executes=node.ID)  # ^ для update_act нет спец. узла!
                    self.add_act(act)
                    # check condition
                    node.cond_obj.accept(self)
                    if self.last_cond_tuple[1] == False:
                        break

        self.leave_current_act()


    TraceJsonVisitor.visit_ForEachJN = _


class SequenceJN(GenericAlgorithmJsonNode):
    def __init__(self, stmts=None, **kw):
        super(SequenceJN, self).__init__(jn_type="sequence", **{k: kw[k] for k in kw if k != "jn_type"})
        assert self.jn_type == "sequence", self.jn_type
        self.stmts = self.list_expand_strs2Stmts(stmts)
        self.gen = 'it'
        self.act_line_format_str = "{name} {phase_str}{nth_str}"

    def to_dict(self):
        return {self.jn_type: [to_dict_or_self(ch) for ch in self.stmts],
                "name": self.name}

    def children_to_dict(self):
        return {
            "body": [to_dict_or_self(ch, "to_dict_4onto") for ch in self.stmts]
        }

    def accept(self, visitor):
        return visitor.visit_SequenceJN(self)


if TraceJsonVisitor:
    def _(self, node):
        act = CtrlStructActLine("sequence", node.name, gen="it", executes=node.ID)
        self.add_act(CompoundActNode(act), enter=True)

        if node.stmts:
            self.visit_list(node.stmts)

        self.leave_current_act()


    TraceJsonVisitor.visit_SequenceJN = _
if AlgTextVisitor:
    def _(visitor, node):
        """ записать блок + имя. """
        visitor.begin_block()
        visitor.append_at_line("  " + tr("comment") + node.name)
        visitor.accept_line_list(node.stmts)
        visitor.end_block()
        return visitor


    AlgTextVisitor.visit_SequenceJN = _
if TraceTextVisitor:
    def _(self, node):
        i = self.register_act(node.display_name())
        # self.add_line("%s %s" % (tr("(it) started"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("started", i))
        if node.stmts:
            self.indent()
            self.accept_line_list(node.stmts)
            self.unindent()
        # self.add_line("%s %s" % (tr("(it) finished"), node.display_name())).append_nth_str(i)
        self.add_line(node.make_act_line("finished", i))
        return self


    TraceTextVisitor.visit_SequenceJN = _


class NamedSequenceJN(SequenceJN):
    def __init__(self, jn_type="unkn", name="noname", sequence=None, **kw):
        # print("NamedSequenceJN", kw)
        super(NamedSequenceJN, self).__init__(stmts=sequence, jn_type=jn_type, name=name, **kw)
        assert jn_type == "sequence", jn_type
    # self.stmts = self.list_expand_strs2Stmts(sequence)


# def accept(self, visitor):
# return visitor.visit_NamedSequenceJN(self)


# ================ Trace Nodes ================


class ActLine(GlobalCounter, WithID):
    def __init__(self, action, executes="-NA-", n="auto", gen="it", phase="performed", comment="", appearance="normal",
                 **kw):
        assert gen in ("he", "she", "it",)  # род (м/ж/ср)
        assert phase in ("started", "finished", "performed",)
        assert n == None or n == "auto" or isinstance(n, int)
        assert appearance in ("normal", "reversed",)  # род (м/ж/ср)
        super().__init__({k: kw[k] for k in kw if k in {"id"}})
        self.executes = executes
        self.action = action
        self.gen = gen  # род (м/ж/ср)
        self.phase = phase
        self.find_n = (n == "auto")
        self.auto_n = self.find_n  # to indicate initial state of n
        self.n = n  # 0 if self.find_n else n
        self.comment = comment
        self.appearance = appearance
        self.json_mandatory_fields = ("executes", "gen", "phase",)

    def action_to_str(self):
        return self.action

    def phase_to_str(self):
        return tr("(%s) %s" % (self.gen, self.phase))

    def comment_to_str(self):
        if self.comment:
            return " " + tr("comment") + self.comment
        return ""

    def count_self(self):
        if self.find_n is not None:
            # count anyway
            n_back = self.n
            self.n = 1  # just to pass to counter
            self.find_n = None
            c = self.count_item(self.to_str())
            self.find_n = False
            self.n = n_back
            return c

    def nth_to_str(self):
        if self.find_n:
            self.n = self.count_self()
        elif self.n is None or self.n <= 0:
            return ""
        elif self.find_n is not None:
            # count anyway
            self.count_self()
        return "%d%s" % (self.n, tr("nth time"))

    def value_to_str(self):
        return ""

    def to_str(self):
        action = self.action_to_str().rstrip()
        comment = self.comment_to_str()
        phase = self.phase_to_str()
        nth = self.nth_to_str()
        value = self.value_to_str()
        if self.appearance == "normal":
            arr = (action, phase, nth, value, comment)
        elif self.appearance == "reversed":
            arr = (phase, action, nth, value, comment)
        arr = [s for s in arr if s]  # remove empty parts
        return " ".join(arr).rstrip()

    def action_to_dict(self):
        return {"action": self.action}

    def comment_to_dict(self):
        if self.comment:
            return {"comment": self.comment}
        return {}

    def nth_to_dict(self):
        self.nth_to_str()
        d = {}
        if not self.auto_n:
            d.update({"n": self.n})
        # elif not (self.n is None or self.n <= 0):
        else:
            d.update({"_n": self.n})
        return d

    def to_dict(self):
        # self.json_mandatory_fields = ("executes","gen","phase",)
        d = {}
        d.update(super().to_dict())
        d.update(self.action_to_dict())
        d.update({f: getattr(self, f) for f in self.json_mandatory_fields})
        d.update(self.nth_to_dict())
        d.update(self.comment_to_dict())
        return d

    def accept(self, visitor):
        return visitor.visit_ActLine(self)


if TextVisitor:
    def _(self, node):
        return self.add_line(node.to_str())


    TextVisitor.visit_ActLine = _


class IterationActLine(ActLine):
    " началась итерация 1 цикла по_нечётным "

    def __init__(self, loop_name, loop_act_id="-no-loop-act-id-", appearance="reversed",
                 **kw):  # executes="-a-loop-body-", n="auto", comment=""):
        kw.update(action=loop_name, phase="performed", appearance=appearance, gen="she", )
        super().__init__(**kw)
        self.json_mandatory_fields = ("executes", "loop_act_id", "phase",)
        self.loop_name = loop_name
        self.loop_act_id = loop_act_id

    def action_to_str(self):
        " итерация 1 цикла по_нечётным"
        self.nth_to_str()
        return "%s %d %s %s" % (tr("iteration"), (self.n), tr("loop", 'gent'), self.loop_name)

    def nth_to_str(self):
        return ""

    def action_to_dict(self):
        return {"iteration": self.n, "loop_name": self.loop_name}


# def to_dict(self):
# # self.json_mandatory_fields = ("executes","gen","phase",)
# d = {}
# d.update( self.action_to_dict() )
# d.update( {f:getattr(self, f) for f in self.json_mandatory_fields} )
# if self.loop_act_id:
# 	d.update( {"loop_act_id": self.loop_act_id} )
# d.update( self.comment_to_dict() )
# return d


class CtrlStructActLine(ActLine):
    def __init__(self, struct_type=None, struct_name="-unnamed-ctrl-struct-", appearance="reversed",
                 **kw):  # executes="-a-ctrl-struct-", n="auto", comment=""
        possible_types = {"func", "alternative", "loop", "sequence"}
        if not struct_type:
            provided_type = set(kw.keys()) & possible_types
            assert provided_type
            provided_type = next(iter(provided_type))
            struct_type, struct_name = provided_type, kw[provided_type]
        assert (struct_type in possible_types), struct_type
        kw.update(action=struct_name, phase="performed", appearance=appearance)
        super().__init__(**kw)
        # self.json_mandatory_fields = ("gen","executes","phase",)
        self.struct_type = struct_type
        self.struct_name = struct_name

    def action_to_str(self):
        return tr(self.struct_type) + " " + self.struct_name

    def action_to_dict(self):
        return {self.struct_type: self.struct_name}


# def to_dict(self):
# d = {}
# d.update( self.action_to_dict() )
# d.update( {f:getattr(self, f) for f in self.json_mandatory_fields} )
# d.update( self.comment_to_dict() )
# return d


def special_to_str(dict_or_str):
    if isinstance(dict_or_str, str):
        return str(dict_or_str)
    s = ""
    if isinstance(dict_or_str, dict):
        s = dict_or_str.get("word", None)
        if not s:
            s = dict_or_str.get("tr", "-its-a-wrong-key!-")
            if s != "-its-a-wrong-key!-":
                s = tr(s, dict_or_str.get("case", "nomn"))
            else:
                raise Exception("special_to_str(): " + str(dict_or_str))
        if s and dict_or_str.get("parens", False):
            s = "(%s)" % s
    return str(s)


class MultiWordActLine(ActLine):
    def __init__(self, action_words, value=None, appearance="normal",
                 **kw):  # executes="-a-ctrl-struct-", n="auto", comment=""
        """ action_words : iterable of dicts:
            {
                "tr" : "my-key",  # run through tr()
                "case" : "gent" or "nomn",  # case to pass to tr()
                "word" : "explicit-str",
                "parens": bool  # enclose in ()
            },
            value : a value the expression is evaluated to (separated frim string with " - ").
        """
        self.json_mandatory_fields = ("gen", "executes", "phase",)
        self.action_words = list(action_words)
        self.value = value
        kw.update(action=self.action_to_dict(), phase="performed", appearance=appearance)
        super().__init__(**kw)

    def value_to_str(self):
        if self.value:
            return "- " + special_to_str(self.value)
        return ""

    def action_to_str(self):
        return " ".join([special_to_str(s) for s in self.action_words])

    def action_to_dict(self):
        return dict(action_words=self.action_words, value=self.value)


# def to_dict(self):
# # self.json_mandatory_fields = ("executes","gen","phase",)
# d = {}
# d.update( self.action_to_dict() )
# d.update( {f:getattr(self, f) for f in self.json_mandatory_fields} )
# d.update( self.comment_to_dict() )
# return d


class CompoundActNode(object):
    def __init__(self, line: ActLine, acts=None, **kw):
        assert line
        self.line = line
        self.acts = list(acts) if acts else []
        self.begin_line = None
        self.end_line = None

    # self.prepare_bounds()

    def prepare_bounds(self):
        if not self.end_line and self.acts:
            self.begin_line = copy.copy(self.line)
            self.begin_line.phase = "started"
            self.end_line = copy.copy(self.line)
            self.end_line.phase = "finished"

    def to_str(self):
        self.prepare_bounds()
        if not self.acts:
            return self.line.to_str()
        return '\n'.join([
            self.begin_line.to_str(),
            *[node.to_str() for node in self.acts],
            self.end_line.to_str(),
        ])

    def to_dict(self):
        self.prepare_bounds()
        if not self.acts:
            return self.line.to_dict()
        return [
            self.begin_line.to_dict(),
            [node.to_dict() for node in self.acts],
            self.end_line.to_dict(),
        ]

    def accept(self, visitor):
        return visitor.visit_CompoundActNode(self)


if TextVisitor:
    def _(self, node):
        node.prepare_bounds()
        if not node.acts:
            return self.add_line((node.line.to_str()))

        self.add_line(node.begin_line.to_str()).indent()

        self.accept_line_list(node.acts)

        self.unindent().add_line(node.end_line.to_str())
        return self


    TextVisitor.visit_CompoundActNode = _

if 0:  # DEBUG
    # a = ActLine("бежать", comment="ошибка!")
    a = ActLine("блок", gen="he")
    # print(a.to_str())
    # print(a.to_dict())

    an = CompoundActNode(a, [
        ActLine("бежать", n=123),
        CompoundActNode(IterationActLine("по_нечётным"), acts=[
            ActLine("бежать"),
            ActLine("лежать"),
        ]),
        MultiWordActLine([
            {"tr": "cond"},
            {"tr": "loop", "case": "gent"},
            {"word": "по_нечётным", "parens": 1},
        ], value=tr(True)),
        CompoundActNode(CompoundActNode(IterationActLine("по_нечётным"), acts=[
            ActLine("бежать"),
            ActLine("лежать"),
        ]), acts=[
            # ActLine("админ?"),
            # ActLine("лежать"),
        ]),
    ])
    print(an.to_str())
    print(an.to_dict())

    exit()

TypeRecognizeOption = namedtuple("TypeRecognizeOption", [
    "mandatory",  # обязательные параметры
    "optional",  # необязательные параметры
    "forbidden",  # ? запрещённые параметры - нужны другому типу узла (для отмены вариантов по умолчанию)
    "callback", "args"
])

# общее для всех узлов алгоритма
_any_alg_node_option = TypeRecognizeOption(
    set(),
    {"name", "expand_act", "noexpand_act"},
    set(),
    FuncJN, {"jn_type": "func"}  # copy&paste (may remove?)
)

# спецификация для конкретных узлов
_alg_node_map = [
    TypeRecognizeOption({"algorithm"},
                        {"noexpand_types"},  # optional
                        {"name"},  # forbidden
                        AlgorithmRootJN, {"jn_type": "algorithm"}
                        ),
    TypeRecognizeOption({"func", "body"},
                        {"is_entry", "param_list"},
                        {"name"},  # forbidden
                        FuncJN, {"jn_type": "func"}
                        ),
    TypeRecognizeOption({"func_name", "func_args"},
                        {"name", "func_id"},
                        set(),  ##{"name"},  # forbidden
                        FuncCallJN, {"jn_type": "func_call"}
                        ),
    # a basic form "alternative"
    TypeRecognizeOption({"alternative", "branches"},
                        set(),
                        {"name"},  # forbidden
                        AlternativeJN, {"jn_type": "alternative"}
                        ),
    # alias "alt" for "alternative"
    TypeRecognizeOption({"alt", "branches"},
                        set(),
                        {"name"},  # forbidden
                        AlternativeJN, {"jn_type": "alternative"}
                        ),
    TypeRecognizeOption({"if", "then"},
                        set(),
                        {"name"},  # forbidden
                        IfBranchJN, {"jn_type": "if"}
                        ),
    # a basic form "else if"
    TypeRecognizeOption({"else if", "then"},
                        set(),
                        {"name"},  # forbidden
                        ElseIfBranchJN, {"jn_type": "else if"}
                        ),
    TypeRecognizeOption({"else"},
                        set(),
                        {"name"},  # forbidden
                        ElseBranchJN, {"jn_type": "else"}
                        ),
    TypeRecognizeOption({"while", "body"},
                        set(), set(),
                        WhileJN, {"jn_type": "while"}
                        ),
    TypeRecognizeOption({"do while", "body"},
                        set(), set(),
                        DoWhileJN, {"jn_type": "do while"}
                        ),
    TypeRecognizeOption({"for", "body"},
                        {"from", "init", "to", "while", "step", "init_act", "cond_act", "update_act"},
                        set(),
                        ForJN, {"jn_type": "for"}
                        ),
    TypeRecognizeOption({"foreach", "in", "body"},
                        set(), set(),
                        ForEachJN, {"jn_type": "foreach"}
                        ),
    TypeRecognizeOption({"sequence"},
                        set(), set(),
                        NamedSequenceJN, {"jn_type": "sequence"}
                        ),
    # TypeRecognizeOption(set(),set(),set(),None,None),
]

# общее для всех узлов трассы
_any_trace_node_option = TypeRecognizeOption(
    {"id", "executes", "phase", },
    {"name", "gen", "n", "_n", "comment", "appearance", "type"},  # "_n" does present just for info: calculated n
    set(),
    ActLine, {}  # copy&paste (may remove?)
)

# спецификация для конкретных узлов
_trace_node_map = [
    TypeRecognizeOption({"action"},
                        set(),
                        set(),  # forbidden
                        ActLine, {}
                        ),
    TypeRecognizeOption({"loop_name"},
                        {"iteration"},
                        set(),  # forbidden
                        IterationActLine, {}
                        ),
    TypeRecognizeOption(set(),
                        {"loop", "alternative"},
                        set(),  # forbidden
                        CtrlStructActLine, {}
                        ),
    TypeRecognizeOption({"action_words"},
                        {"value"},
                        set(),  # forbidden
                        MultiWordActLine, {}
                        ),
    # TypeRecognizeOption(set(),set(),set(),None,None),
]

test_str = """
{
"algorithm": [
        {"for":"var_i", "from": "2", "to":"15", "step":"+1",
            "init_act": "var_i значением 2",
            "cond_act": "i не достигло 16",
            "update_act": "прибавить 1 к i",  "name":"my-for-3", "body": [
                "for_body_action_3"
            ]
        }
]}
"""
test_str = """
{
"algorithm": [
    {"func":"main", "is_entry":"0", "param_list":[], "body": [
            "бежать",
            "break"
        ]
    },
    {"alternative":"my-alt-1", "branches": [
            {"if": "цвет==зелёный", "then": [
                "бежать",
                "стоп"
            ]},
            {"else if": "цвет==желтый", "then": [
                "лежать"
            ]},
            {"else": [
                "ждать"
            ]}
        ]
    },
    {"while":"while-cond-1", "name":"my-while-1", "body": [
            "повернуть",
            {"do while":"dowhile-cond-2", "name":"my-dowhile-2", "body": [
                    "do_while_body_action_2"
                ]
            },
            {"for":"день", "from":"1", "to":"5", "step":"+1", "name":"my-for-3", "body": [
                    "for_body_action_3",
                    {"foreach":"x", "in": "list", "name":"my-for-in-4", "body": [
                    "foreach_body_action_4"]
                    },
                    {"sequence": [
                        "seq_action_1",
                        "seq_action_2"
                        ],
                        "name":"myseq-5"
                    }
                ]
            }
        ]
    }
]}
"""
test_str = """
{
"algorithm": [
    "делай_раз",
    "делай_два",
    "делай_три"
]}
"""


def boolean_line_usage_actual(boolean_line, visitor_obj):
    L = len(boolean_line)
    c = 1 + visitor_obj.last_cond_tuple[0]
    if c == L:
        return boolean_line
    elif c < L:
        return boolean_line[:c]
    else:  # if c > L:
        return boolean_line.ljust(c, '0')


def boolean_line_usage_report(boolean_line, visitor_obj):
    L = len(boolean_line)
    actual_line = boolean_line_usage_actual(boolean_line, visitor_obj)
    c = 1 + visitor_obj.last_cond_tuple[0]
    if c == L:
        return boolean_line
    elif c < L:
        return "%s (reduced from %s)" % (actual_line, boolean_line)
    else:  # if c > L:
        return "%s (auto-expanded from %s)" % (actual_line, (boolean_line or "''"))


def act_line_for_alg_element(alg_element: dict, phase: str, expr_value=False, use_exec_time=0, lang=None) -> dict:
    """ Produce trace acts strings separately with minimum of config (no whole algorithm tree is required).
        We tried to maintain maximum flexibility.
    Not all algorithm structures are covered, but only the most frequently used ones.
    """
    if lang:
        set_target_lang(lang)

    elem_type = alg_element["type"]
    elem_type = elem_type.replace('-', ' ')
    suffix = '_loop'
    if elem_type.endswith(suffix):
        elem_type = elem_type.replace(suffix, '').replace("_", " ")

    node = None
    parent = None
    is_iteration = False
    # в случае с простыми действиями (stmt, expr) phase не имеет значения - создаётся с фазой performed
    if elem_type == "stmt":
        node = StatementAtomJN("stmt", name=alg_element["name"])
    elif elem_type in ("break", "continue", "return"):
        node = NameOnlyStatementJN(elem_type, name=alg_element["name"])
    elif elem_type == "expr":
        node = GenericCondition(cond=None, name=alg_element["name"])
    # в случае со сложными действиями создаётся акт целиком, со всеми вложенными действиями?..  phase указывает, начало или конец нам нужно взять
    if not node:  # elem_type in ("if", "else if"):
        tro = find_tro_for_act_type(elem_type)
        assert tro, "act_line_for_alg_element(): node type not found: alg_element['type'] == " + alg_element["type"]

        class_ = tro.callback
        kwargs = {}
        if 'then' in tro.mandatory:  # "if", "else if"
            kwargs[elem_type] = alg_element["cond"]["name"]
            kwargs['then'] = "dummy"

        if 'else' in tro.mandatory:  # "else"
            kwargs['else'] = "dummy"

        if 'alternative' in tro.mandatory:
            kwargs[elem_type] = alg_element["name"]
        # kwargs['branches'] = ["dummy"]

        if 'body' in tro.mandatory:
            if 'cond' in alg_element:
                kwargs[elem_type] = alg_element["cond"]["name"]
            kwargs['name'] = alg_element["name"]
            kwargs['body'] = "dummy"

        if 'sequence' == elem_type:  # in tro.mandatory:
            name = alg_element["name"]
            if not name.endswith('_loop_body'):
                kwargs[elem_type] = ["dummy"]
                kwargs['name'] = name
            else:
                is_iteration = True
                # parent = AlternativeJN("alternative", branches=[node])
                class_ = WhileJN
                elem_type = "while"
                kwargs["while"] = "dummy"
                kwargs['name'] = name.replace('_loop_body', '')
                kwargs['body'] = "dummy"
                pass

        if 'algorithm' == elem_type:
            kwargs[elem_type] = ["dummy"]

        if 'func_call' == elem_type:
            kwargs.update({
                "func_name": alg_element["func_name"],
                "func_args": alg_element["func_args"],
            })

        # print("### creating element of type:", class_)
        node = class_(jn_type=elem_type, **kwargs)

        if isinstance(node, ConditionalAlternativeBranch):
            parent = AlternativeJN("alternative", branches=[node])

        if parent:
            node.setup(parent)

    assert node, "act_line_for_alg_element(): Not implemented for: alg_element['type'] == " + elem_type

    if is_iteration:
        text_trace = node.make_iteration_act_line(phase, n=use_exec_time)
    else:
        # universal way to make strimg of trace line (except sequences *_loop_body)
        text_trace = node.make_act_line(phase, n=use_exec_time, value=tr(expr_value))

    # boolean_line = [expr_value]

    # tr_v = TraceTextVisitor(boolean_line)
    # node.accept(tr_v)

    # if phase != 'performed':
    # 	# limit generated lines to desired one only
    # 	index = {
    # 		'started': 0,
    # 		'finished': -1,
    # 	}.get(phase)
    # 	tr_v.lines = [tr_v.lines[index]]

    # assert len(tr_v.lines) == 1, tr_v.lines
    # text_trace = str(tr_v)

    text_trace = text_trace.strip()

    # # set exec_time
    # if use_exec_time > 1:
    # 	text_trace = text_trace.replace('1th time', '%sth time' % use_exec_time)
    # 	text_trace = text_trace.replace('1-й раз', '%s-й раз' % use_exec_time)

    return patch_trace(text_trace)


# tr_v = TraceJsonVisitor(boolean_line)
# node.accept(tr_v)
# json_trace = tr_v.root.to_dict()

# json_trace['as_string'] = text_trace

# return json_trace
# return "Not implemented: act_line_to_string(act_json) -> str"

def find_tro_for_act_type(act_type: str):
    for tro in _alg_node_map:
        if tro.args["jn_type"] == act_type:
            return tro
    return None


def patch_trace(trace: str) -> str:
    # apply patches
    trace = trace.replace(
        "1th", "1st"
    ).replace(
        "2th", "2nd"
    ).replace(
        "3th", "3rd"
    ).replace(
        "branch condition of alternative", "branch of condition"
    ).replace(
        "began program", "program began"
    ).replace(
        "ended program", "program ended"
    ).replace(
        "alternative", "selection"
    )

    # move <phase word> right before <ith>
    trace = re.sub(r"^(\s*)(began\s+|ended\s+|executed\s+)(.+?\s+)(\d+\w+)", r"\1\3\2\4", trace, flags=re.M)

    # remove "sequence global_code" lines
    trace = re.sub(r"^\s*sequence\s+global_code.*?\s*^", "", trace, flags=re.M)

    # move <phase word> to the end of line on iteration line
    trace = re.sub(r"(began|ended|executed)\s+(iteration)(.+?)loop(.+?)$", r"\2\3of loop\4 \1", trace, flags=re.M)

    # replace "executed" to "evaluated" (for condition lines only)
    trace = re.sub(r"(condition[^\n\r]+)executed", r"\1evaluated", trace, flags=re.M)

    return trace


def get_text_trace(alg_root_node, boolean_line) -> (str, TraceTextVisitor):
    tr_v = TraceTextVisitor(boolean_line)
    alg_root_node.accept(tr_v)
    trace = str(tr_v)

    return patch_trace(trace), tr_v


if __name__ == "__main__":

    # exit()  # DEBUG

    if 0:  # DEBUG
        r = GenericAlgorithmJsonNode.parse(test_str)
        # print(r)
        # print(r.to_dict())

        v = AlgTextVisitor()
        r.accept(v)
        print(v)  # печатаем алгоритм

        v = TraceJsonVisitor("11010111011")
        tv = TextVisitor()
        try:
            r.accept(v)
            v.root.accept(tv)
            print(tv)  # печатаем трассу

            alg = stringify(r.to_dict_4onto(), False)
            # print(alg)
            with open("alg_out.json", "w", encoding='utf-8') as f:
                f.write(alg)

            trace = stringify(v.root.to_dict())
            # print(trace)
            with open("tr_out.json", "w", encoding='utf-8') as f:
                f.write(trace)
        except Exception as e:
            # print(v.root.to_str())
            # r.accept(v)
            # v.root.accept(tv)
            # print(tv)
            print(stringify(v.root.to_dict()))
            raise e

        exit()

    try:
        import os
        import os.path

        input_alg_file = 'alg_in.json'
        input_trace_specs_file = 'tr_in.txt'
        speak_lang_file = 'speak.lang'

        output_alg_traces_file = 'algtr_out.txt'
        output_alg_json_file = 'alg_out.json'
        output_trace_json_template = 'tr_out_{}.json'

        if os.path.exists(speak_lang_file):
            with open(speak_lang_file, encoding='utf-8') as f:
                lang = f.read().strip().lower()
                if lang in SUPPORTED_LANGS:
                    set_target_lang(lang)
                    print("Switched to language `%s`." % lang)
                else:
                    print(
                        "Warning: invalid content of language-target file `%s` (one of %s is expected). Defaulting to `%s`." % (
                            speak_lang_file, str(SUPPORTED_LANGS), DEFAULT_LANG))

        if os.path.exists(input_alg_file):
            with open(input_alg_file, encoding='utf-8') as f:
                json_data = f.read()
        else:
            print("Not found:", input_alg_file)
            exit()

        if os.path.exists(input_trace_specs_file):
            with open(input_trace_specs_file) as f:
                tr_boolean_lines = f.readlines()
        else:
            print("Not found:", input_trace_specs_file)
            tr_boolean_lines = []

        with open(output_alg_traces_file, "w", encoding='utf-8') as f:
            # print(json_data)
            r = GenericAlgorithmJsonNode.parse(json_data)
            alg_v = AlgTextVisitor()
            r.accept(alg_v)
            f.write(str(alg_v))
            print("Saved: ", "algorithm as text")

            for boolean_line in tr_boolean_lines:
                boolean_line = boolean_line.strip()
                trace, tr_v = get_text_trace(r, boolean_line)

                f.write("\n\n// " + boolean_line_usage_report(boolean_line, tr_v) + '\n' + trace)

        alg = stringify(r.to_dict_4onto(), False)
        with open(output_alg_json_file, "w", encoding='utf-8') as f:
            f.write(alg)

        print("Saved: ", "algorithm as json")

        for boolean_line in tr_boolean_lines:
            boolean_line = boolean_line.strip()
            tr_v = TraceJsonVisitor(boolean_line)
            r.accept(tr_v)
            trace = stringify(tr_v.root.to_dict())

            actual_fname = output_trace_json_template.format(boolean_line_usage_actual(boolean_line, tr_v))
            with open(actual_fname, "w", encoding='utf-8') as f:
                f.write(trace)

            print("Saved: ", "trace as json", " file:", actual_fname)

        print("Completed: ", len(tr_boolean_lines), 'trace(s)')

    except Exception as e:
        with open(output_alg_traces_file, "w", encoding='utf-8') as f:
            f.write("An error (%s) occured :\n\n" % (type(e).__name__) + str(e))
            raise e
