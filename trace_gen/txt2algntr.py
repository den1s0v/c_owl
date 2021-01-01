# txt2algntr.py - Text to algorithm and trace mapped.


import re

_maxAlgID = 1
_maxTrID = 1

TRUTH_ALIASES = ("истина","да","true","1")
FALSE_ALIASES = ("ложь","нет","false","0")
TRUTH_ALIASES_re = re.compile("|".join(TRUTH_ALIASES))
FALSE_ALIASES_re = re.compile("|".join(FALSE_ALIASES))


def parse_expr_value(s: str):
    value = s
    s = s.lower()
    if s in TRUTH_ALIASES:
        value = True
    if s in FALSE_ALIASES:
        value = False
    return value

def parse_expr_values(s: str) -> list:
    """
    101             -> (True, False, True)
    1 0 1           -> (True, False, True)
    true FalsE TRUE -> (True, False, True)
    ДА НЕТ 1        -> (True, False, True)
    
    Допустимы скобочки повторения (как в периодических дробях):
    1(0)  means  100000...  -> (True, "(", False, ")")
    (001)  means  001001001...   -> ("(", False, False, True, ")")
    
    """
    values = []
    s = s.lower()
    repetition_start_i = -1
    while s:
        nchars = 1
        m = TRUTH_ALIASES_re.match(s)
        if m:
            values.append(True)
            nchars = len(m.group(0))
        else:
            m = FALSE_ALIASES_re.match(s)
            if m:
                values.append(False)
                nchars = len(m.group(0))
            # расстановка скобочек повторения: только эффективная группировка
            elif s[0] == "(":
                repetition_start_i = len(values)
            elif s[0] == ")" and repetition_start_i >= 0:
                values.insert(repetition_start_i, "(")
                values.append(s[0])
                break
        s = s[nchars:]  # strip some chars from left
    return tuple(values)

def get_ith_expr_value(expr_values: tuple, i: int):
    """Decodes the result of 'parse_expr_values' function.
    Return None if 'i' is out of range
    """
    # print(i, "from expr_values:", expr_values)
    if "(" not in expr_values:
        return expr_values[i] if i < len(expr_values) else None
        
    b_i = expr_values.index("(")
    if i < b_i:
        return expr_values[i]
    
    repeat_i = i - b_i
    
    b_i += 1  # skip the "(" element itself
    assert expr_values[-1] == ")", str(expr_values)
    e_i = expr_values.index(")")
    repeat_len = e_i - b_i
    if repeat_len <= 0:  # in case of stupid empty repeat: (True, "(", ")") 
        return None
    
    return expr_values[b_i + repeat_i % repeat_len]
    


class AlgorithmParser:
    def __init__(self, line_list=None, start_id=1, verbose=0):
        assert type(start_id) is int
        self._maxID = max(start_id - 1, _maxAlgID)
        self.verbose = verbose
        self.clear()
        if line_list:
            self.parse(line_list)

    def clear(self):
        self.name2id = {}
        
        self.algorithm = {
              "id": self.newID("algorithm"),
              "type": "algorithm",
              "name": "algorithm",
              "functions": [],
              "global_code" : {   #  stmts -> global_code  !!! 
                    "id": self.newID("global_code"),
                    "type": "sequence",
                    "name": "global_code",
                    "body": []
                },
              "entry_point": None,
              "expr_values": {},
        }

            
            
    def newID(self, what=None):
        self._maxID += 1
        global _maxAlgID; _maxAlgID = self._maxID
        if what:
            if what in self.name2id:
                print("Warning: multiple objects named as '%s' !"%what,
                      "Old id/new id:", self.name2id[what],"/", self._maxID, "; Overriding with latter one.")
            self.name2id[what] = self._maxID
        return self._maxID

    def parse(self, line_list: "list(str)"):
        self.algorithm["global_code"]["body"] += self.parse_algorithm_ids(line_list)
        # найдём точку входа
        for func in self.algorithm["functions"]:
            if func["is_entry"]:
                self.algorithm["entry_point"] = func  # надеемся, что объект с id сформируется в ссылку на функцию ...
                break
        else:  # нет функции
            self.algorithm["entry_point"] = self.algorithm["global_code"]  # надеемся с id
                
                
        
    def parse_expr(self, name: str, values=None) -> dict:
        "Нововведение: самостоятельный объект для выражений (пока - только условия)"
        if values:
            self.algorithm["expr_values"][name] = parse_expr_values(values)
        return {
            "id": self.newID(name),
            "type": "expr",
            "name": name,
        }

    def parse_stmt(self, name:str) -> dict:
        ""
        return {
            "id": self.newID(name),
            "type": "stmt",
            "name": name
        }

    def parse_algorithm_ids(self, line_list: "list(str)", start_line=0, end_line=None) -> list:
        """Формирует список словарей объектов алгоритма в формате alg.json для ctrlstrct_run.py
            Функции автоматически добавляются в self.algorithm["functions"].
            Глобальный код возввращается списком statement'ов верхнего уровня.
        """
        
        parse_algorithm = self.parse_algorithm_ids  # синоним для простоты написания
        
        def make_loop_body(loop_name, stmt_List):
            name = loop_name + "_loop_body"
            return {
                    "id": self.newID(name),
                    "type": "sequence",
                    "name": name,
                    "body": stmt_List
            }

        result = []
        line_list = line_list[start_line:end_line]
        line_indents = [len(s) - len(s.lstrip()) for s in line_list]

        current_level_stmt_line_idx = []
        current_level = None  # отступ текущего уровня (найдём в цикле как отступ первой строки кода, но не { }. )

        for i,idt in enumerate(line_indents):
            if line_indents[i] == current_level  or  current_level is None:  # элемент текущего уровня
                if line_list[i].strip() in ("", "{", "}"):  # пропускаем { } и пустые
                    continue
                current_level = line_indents[i]
                current_level_stmt_line_idx.append(i)
            if line_indents[i] < current_level:  # элемент более верхнего уровня
                break

        current_level_stmt_line_idx.append(len(line_list))  # конец последнего

        # print(current_level_stmt_line_idx)

        ci = 0  # current line index

        for entry_i in range(len(current_level_stmt_line_idx) - 1):
            i = current_level_stmt_line_idx[entry_i]
            e = current_level_stmt_line_idx[entry_i + 1] - 1
            if i < ci:
                continue

            ci = i
            # print(ci, e)
            # print(*line_list[ci:e+1])

            # функция main
            m = re.match(r"(?:function|функция)\s+(\S+)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("function")
                name = m.group(1)  # имя функции
                body_name = name+"-body"
                self.algorithm["functions"].append({
                      "id": self.newID(name),
                      "type": "func",
                      "name": name,  # имя функции
                      "is_entry": name == "main",
                      "param_list": [],
                      "body" : {   #  stmts -> global_code  !!! 
                            "id": self.newID(body_name),
                            "type": "sequence",
                            "name": body_name,
                            "body": parse_algorithm(line_list[i+2:e])  # исключая скобки { } вокруг тела
                        },
                })
                ci = e + 1
                continue  # with next stmt on current level

            # если цвет==зелёный  // my-alt-1
            # if color==green  -> true,false,true // my-alt-1
            # если условие (цвет==зелёный) -> 101 // my-alt-1
            # if condition (color==green) -> 1(01) // my-alt-1
            m = re.match(r"""
                (?:if|если)
                (?:\s+condition|\s+условие)?   # optional
                \s+
                (\(.+\)|\S+)  # 1 cond_name
                (?:
                    \s+ - >?    # - or ->   
                    \s+ (\S+)   # 2 optional values
                )?
                \s* (?://|\#)\s*(\S+)  # 3 name
                """, line_list[ci].strip(), re.I|re.VERBOSE)
            if m:
                if self.verbose: print("alt if")
                name = m.group(3)  # имя альтернативы (пишется в комментарии)
                values = m.group(2)  # значения, принимаемые выражением по мере выполнения программы (опционально)
                cond_name = m.group(1)  # условие if (может быть в скобках)
                if cond_name[0]+cond_name[-1] == "()":
                    cond_name = cond_name[1:-1]      # удалить скобки
                branch_name = "if-"+cond_name  # имя ветки должно отличаться от имени условия
                # self.parse_expr()
                result.append({
                    "id": self.newID(name),
                    "type": "alternative",
                    "name": name,
                    "branches": [ {
                        "id": self.newID(branch_name),
                        "type": "if",
                        "name": branch_name,
                        "cond":  self.parse_expr(cond_name, values=values),
                        "body": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                    } ]
                })
                ci = e + 1
                continue  # with next stmt on current level

            # иначе если цвет==желтый
            # иначе если условие (цвет==желтый)  -> true,false,true
            # else if color==yellow  -> 101
            # else if condition (color==yellow)
            m = re.match(r"""
                (?:
                    else \s+ if (?:\s+condition)?
                |
                    иначе \s+ если (?:\s+условие)?
                )
                \s+(\(.+\)|\S+) # 1 cond_name
                (?:
                    \s+ - >?    # - or ->   
                    \s+ (\S+)   # 2 optional values
                )?
                """, line_list[ci].strip(), re.I|re.VERBOSE)
            if m:
                if self.verbose: print("alt elseif")
                cond_name = m.group(1)  # условие else if (условие может быть в скобках)
                if cond_name[0]+cond_name[-1] == "()":
                    cond_name = cond_name[1:-1]      # удалить скобки
                values = m.group(2)  # значения, принимаемые выражением по мере выполнения программы (опционально)
                branch_name = "elseif-"+cond_name  # имя ветки должно отличаться от имени условия
                assert len(result)>0 and result[-1]["type"] == "alternative", "Algorithm Error: 'иначе если' does not follow 'если' :\n\t"+line_list[ci].strip()
                alt_obj = result[-1]
                alt_obj["branches"] += [ {
                        "id": self.newID(branch_name),
                        "type": "else-if",
                        "name": branch_name,
                        "cond":  self.parse_expr(cond_name, values=values),
                        "body": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                    } ]
                ci = e + 1
                continue  # with next stmt on current level

            # иначе
            m = re.match(r"(?:else|иначе)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("alt else")
                assert len(result)>0 and result[-1]["type"] == "alternative", "Algorithm Error: 'иначе' does not follow 'если' :\n\t"+line_list[ci].strip()
                alt_obj = result[-1]
                branch_name = alt_obj["name"]+"-else"  # имя ветки должно отличаться от имени ветвления
                alt_obj["branches"] += [ {
                        "id": self.newID(branch_name),
                        "type": "else",
                        "name": branch_name,
                        "body": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                    } ]
                ci = e + 1
                continue  # with next stmt on current level


            # пока while-cond-1  // my-while-1
            # while my-cond-2   -> 101 // my-while-2
            m = re.match(r"""
                (?:while|пока)
                \s+
                (\(.+\)|\S+)    # 1 cond_name
                (?:
                    \s+ - >?    # - or ->   
                    \s+ (\S+)   # 2 optional values
                )?
                \s* (?://|\#)
                \s* (\S+)       # 3 loop name
                """, line_list[ci].strip(), re.I|re.VERBOSE)
            if m:
                if self.verbose: print("while")
                name = m.group(3)  # имя цикла (пишется в комментарии)
                values = m.group(2)  # значения, принимаемые выражением по мере выполнения программы (опционально)
                cond_name = m.group(1)  # условие цикла (может быть в скобках)
                result.append({
                    "id": self.newID(name),
                    "type": "while_loop",
                    "name": name,
                    "cond": self.parse_expr(cond_name, values=values),
                    "body":  make_loop_body(
                                name,
                                parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                            )
                })
                ci = e + 1
                continue  # with next stmt on current level

            # делать   // my-dowhile-2
            #    ...
            # пока dowhile-cond-2
            # 
            # 
            # do   // my-dowhile-3
            #    ...
            # while dowhile-cond-3  -> 100011100
            m = re.match(r"(?:do|делать)\s*(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            m2 = e+1 < len(line_list)  and  re.match(r"""
                (?:while|пока)
                \s+
                (\(.+\)|\S+)  # 1 cond_name
                (?:
                    \s+ - >?    # - or ->   
                    \s+ (\S+)   # 2 optional values
                )?
                """,   line_list[ e+1 ].strip(), re.I|re.VERBOSE)
            if m and m2:
                if self.verbose: print("do while")
                name = m.group(1)  # имя цикла (пишется в комментарии)
                cond_name = m2.group(1)  # условие цикла (может быть в скобках)
                values = m2.group(2)  # значения, принимаемые выражением по мере выполнения программы (опционально)
                result.append({
                    "id": self.newID(name),
                    "type": "do_while_loop",
                    "name": name,
                    "cond": self.parse_expr(cond_name, values=values),
                    "body": make_loop_body(
                                name,
                                parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                            )
                })
                ci = e + 2
                continue  # with next stmt on current level

            # делать   // my-dountil-2
            #    ...
            # до dountil-cond-2
            # 
            # 
            # do   // my-dountil-3
            #    ...
            # until dountil-cond-3  -> 100011100
            m = re.match(r"(?:do|делать)\s*(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            m2 = e+1 < len(line_list)  and  re.match(r"""
                (?:until|до)
                \s+
                (\(.+\)|\S+)  # 1 cond_name
                (?:
                    \s+ - >?    # - or ->   
                    \s+ (\S+)   # 2 optional values
                )?
                """,   line_list[ e+1 ].strip(), re.I|re.VERBOSE)
            if m and m2:
                if self.verbose: print("do until")
                name = m.group(1)  # имя цикла (пишется в комментарии)
                cond_name = m2.group(1)  # условие цикла (может быть в скобках)
                values = m2.group(2)  # значения, принимаемые выражением по мере выполнения программы (опционально)
                result.append({
                    "id": self.newID(name),
                    "type": "do_until_loop",
                    "name": name,
                    "cond": self.parse_expr(cond_name, values=values),
                    "body": make_loop_body(
                                name,
                                parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                            )
                })
                ci = e + 2
                continue  # with next stmt on current level

            # для день от 1 до 5 с шагом +1  // my-for-3
            # for day from 1 to 5 step +1  // my-for-4
            m = re.match(r"""
                            (?:for|для)\s+(\S+)\s+  # 1 var
                            (?:from|от)\s+([-+]?\d*.?\d+)\s+   # 2 from
                            (?:to|до)\s+([-+]?\d*.?\d+)\s+     # 3 to
                            (?:step|с\s+шагом)\s+([-+]?\d*.?\d+) # 4 step
                            (?:
                                \s+ - >?    # - or ->   
                                \s+ (\S+)   # 5 optional values
                            )?
                            \s* (?://|\#)\s*(\S+)         # 6 name
                        """, line_list[ci].strip(), re.I|re.VERBOSE)
            if m:
                if self.verbose: print("for")
                s_var =  m.group(1)  # переменная цикла
                s_from = m.group(2)  # нижняя граница цикла
                s_to =   m.group(3)  # верхняя граница цикла
                s_step = m.group(4)  # шаг цикла
                values = m.group(5)  # значения, принимаемые выражением - условием продолжения цикла - по мере выполнения программы (опционально)
                name =   m.group(6)  # имя цикла (пишется в комментарии)
                result.append({
                    "id": self.newID(name),
                    "type": "for_loop",
                    "name": name,
                    "variable": s_var,
                    "init":   self.parse_stmt("{}={}".format(s_var, s_from)),
                    "cond":   self.parse_expr("{}<={}".format(s_var,s_to), values=values),
                    "update": self.parse_stmt("{v}={v}{:+d}".format(int(s_step), v=s_var)),
                    "body":  make_loop_body(
                                name,
                                parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                            )
                })
                ci = e + 1
                continue  # with next stmt on current level

            # для каждого x в list  // my-for-in-4
            # foreach x in list -> 1110110  // my-for-in-5
            # for each x in list  // my-for-in-5
            m = re.match(r"""
                (?:for\s*each|для\s+каждого)
                \s+ (\S+)             # 1 var
                \s+ (?:in|в)\s+((?:array\s+|массив\w*\s+)?\S+)  # 2 in (container name)
                (?:
                    \s+ - >?    # - or ->   
                    \s+ (\S+)   # 3 optional values
                )?
                \s* (?://|\#)\s*(\S+)  # 4 name
                """, line_list[ci].strip(), re.I|re.VERBOSE)
            if m:
                if self.verbose: print("foreach")
                s_var = m.group(1)  # переменная цикла
                s_container = m.group(2)  # контейнер
                values = m.group(3)  # значения, принимаемые выражением - условием продолжения цикла - по мере выполнения программы (опционально)
                name =   m.group(4)  # имя цикла (пишется в комментарии)
                result.append({
                    "id": self.newID(name),
                    "type": "foreach_loop",
                    "name": name,
                    "variable": s_var,
                    "container": s_container,
                    "init":   self.parse_stmt("{}={}.first()".format(s_var, s_container)),
                    "cond":   self.parse_expr("{}!={}.last()".format(s_var,s_container), values=values),
                    "update": self.parse_stmt("{v}=next({},{v})".format(s_container, v=s_var)),
                    "body":  make_loop_body(
                                name,
                                parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                            )
                })
                ci = e + 1
                continue  # with next stmt on current level


            # {  // myseq-5  -  начало именованного следования
            m = re.match(r"\{\s*(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("named sequence:", m.group(1))
                name =   m.group(1)  # имя следования (пишется в комментарии)
                result.append({
                    "id": self.newID(name),
                    "type": "sequence",
                    "name": name,
                    "body": parse_algorithm(line_list[i+1:e]),  # учитывая скобки { } вокруг тела
                })
                ci = e + 1
                continue  # with next stmt on current level

            # одно слово - имя действия: "бежать"
            m = re.match(r"(\S+)$", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("action")
                name = m.group(1)
                result.append( self.parse_stmt(name) )
                ci = e + 1
                continue  # with next stmt on current level

            # print("Warning: unknown control structure: ")
            raise ValueError("AlgorithmError: unknown control structure at line %d: '%s'"%(ci, line_list[ci].strip()))


        return result


def create_algorithm_from_text(lines: list) -> AlgorithmParser:
    'just a wrapper for AlgorithmParser constructor'
    try:
        return AlgorithmParser(lines)
    except Exception as e:
        print("Error !")
        print("Error parsing algorithm:")
        print(" ", e)
        # raise e  # useful for debugging
        return str(e)


# ap = AlgorithmParser(test_lines)
# ap.algorithm

class TraceParser:
    def __init__(self, line_list=None, alg_parser_obj=None, start_id=1, start_line=0, end_line=None, verbose=0):
        assert type(start_id) is int
        self._maxID = max(start_id - 1, _maxTrID)
        self.verbose = verbose

        if alg_parser_obj:
            assert isinstance(alg_parser_obj, AlgorithmParser)
            self.alg_dict = alg_parser_obj.algorithm
            self.name2id = alg_parser_obj.name2id
            self._maxID = max(self._maxID, alg_parser_obj._maxID + 1)
        else:
            self.alg_dict = None
            self.name2id = None
        
        self.name2id_no_whitespace = None
        
        self.trace = []
        self.boolean_chain = []
        
        if line_list and self.alg_dict:
            self.parse(line_list, self.alg_dict, self.name2id, start_line, end_line)
            
    def get_alg_node_id(self, name, node_type=None):
        """ `node_type` is useful to force "expr" type of returned node """
        if isinstance(name, (list, set, tuple)):
            r = None
            for n in name:
                r = self.get_alg_node_id(n, node_type=node_type)
                if r:
                    name = n
                    break
        else:
            r = self.name2id.get(name, None)
            if not r and name[0] + name[-1] == "()":
                return self.get_alg_node_id(name[1:-1], node_type=node_type)
            if not r:
                name = name.replace(' ','')
                if not self.name2id_no_whitespace:
                    # копия словаря с ключами, из которых вырезаны пробелы
                    self.name2id_no_whitespace = { n.replace(' ',''):v for n,v in self.name2id.items() }
                # поищем без пробелов
                r = self.name2id_no_whitespace.get(name, None)
    
        if node_type:  # and node_type == "expr":
            name = name.replace('(','').replace(')','')

            criterion = lambda d: (type(d) is dict and "id" in d and  d["type"] == node_type and  d["name"].replace(' ','').replace('(','').replace(')','') == name)
            nodes = list(find_by_predicate(self.alg_dict, criterion, find_one=True))
            if nodes:
                expr = nodes[0]
                return expr["id"]

        elif r is not None:            
            # check if the node is expr
            criterion = lambda d: (type(d) is dict and "id" in d and d["id"] == r and d["type"] == "expr")
            expr = list(find_by_predicate(self.alg_dict, criterion, find_one=True))
            if expr:
                expr = expr[0]


                # find the (expr as "cond")`s parent statement and return it
                criterion = lambda d: (type(d) is dict and "cond" in d and d["cond"] == expr)
                p = list(find_by_predicate(self.alg_dict, criterion, find_one=True))
                if p:
                    # print(name, p)
                    r = p[0]["id"]
                else:
                    print(f"cannot find parent statement for '{name}'!")
        return r
            
    def newID(self, what=None, owerwrite=False):
        self._maxID += 1
        global _maxTrID; _maxTrID = self._maxID
        # if what:
        #     if what in self.name2id:
        #         if owerwrite:
        #             print("Warning: multiple trace objects named as '%s' !"%what,
        #               "Old id/new id:", self.name2id[what],"/", self._maxID, "; Overriding with latter one.")
        #         else:
        #             return self.name2id[what]
        #     self.name2id[what] = self._maxID
        return self._maxID

    def parse(self, line_list: "list(str)", alg_dict=None, name2id=None, start_line=0, end_line=None):
        self.alg_dict = self.alg_dict or alg_dict
        assert self.alg_dict
        self.name2id = self.name2id or name2id
        assert self.name2id
        self.iteration_count_dict = {}
        
        self.trace += self.parse_trace_by_alg(line_list, start_line, end_line)
        
        return self
        
    def parse_trace_by_alg(self, line_list: "list(str)", start_line=0, end_line=None) -> list:
        """Формирует плоский список объектов трассы в формате trace.json для ctrlstrct_run.py
        """
        
        # parse_trace = self.parse_trace_by_alg  # синоним для простоты написания

        result = []
        
        ci = start_line  # index of line
        end_line = end_line or len(line_list)
        
        for line in line_list[ci:]:
        
            if ci >= end_line or not line:
                break

            ci += 1  # increment before any usage to match 1-based enumeration
        
            line = line.strip()
            
            # ...  // comment
            m = re.search(r"(?://|#)\s*(.+)$", line, re.I)
            comment = m and m.group(1) or ""

            if m and m.start() == 0:
                continue
        
            BEGAN_ru = "(?:начал[оа]?с[ья])"
            ENDED_ru = "(?:закончил[оа]?с[ья])"
            EXECUTED_ru = "(?:выполнил[оа]?с[ья])"
            BEGAN_en = "(?:began)"
            ENDED_en = "(?:ended)"
            EXECUTED_en = "(?:executed|evaluated|calculated)"
            BEGAN = "(?:начал[оа]?с[ья]|began)"
            ENDED = "(?:закончил[оа]?с[ья]|ended)"
            EXECUTED = "(?:выполнил[оа]?с[ья]|executed|evaluated|calculated)"
            Ith1_ru = r"(?:\s+(\d+)[-_]?й?\s+раз)"
            Ith1_en = r"(?:\s+(\d+)(?:st|nd|rd|th)?\s+time)"
            Ith1 = r"(?:\s+(\d+)(?:st|nd|rd|th|[-_]й)?\s+(?:time|раз))"
            Ith1_femn = r"(?:\s+(\d+)(?:st|nd|rd|th|[-_]я)?)"  # 1-я [итерация]
            PHASE_dict = dict(BEGAN=BEGAN, ENDED=ENDED, EXECUTED=EXECUTED, 
                BEGAN_ru=BEGAN_ru, ENDED_ru=ENDED_ru, EXECUTED_ru=EXECUTED_ru, 
                BEGAN_en=BEGAN_en, ENDED_en=ENDED_en, EXECUTED_en=EXECUTED_en, 
                Ith1=Ith1, Ith1_femn=Ith1_femn, )
            BEGAN_re = re.compile(BEGAN, re.I)
            ENDED_re = re.compile(ENDED, re.I)
            EXECUTED_re = re.compile(EXECUTED, re.I)
            
            def get_phase_by_str(phase_str):
                if BEGAN_re.match(phase_str):
                    return "started"  
                elif ENDED_re.match(phase_str):
                    return "finished"  
                elif EXECUTED_re.match(phase_str):
                    return "performed"
                else:
                    return "U-N-K-N-O-W-N"
                
        
            # началась программа
            # закончилась программа
            # program began
            # program ended
            m = re.match(r"({BEGAN_ru}|{ENDED_ru})\s+программа|program\s+({BEGAN_en}|{ENDED_en})".format(**PHASE_dict), line, re.I)
            if m:
                phase_str = m.group(1) or m.group(2)
                if self.verbose: print("{} программа".format(phase_str))
                #   {"id": 32, "action": "программа", "executes": 25, "gen": "she", "phase": "started", "n": null},
                name = "program"
                phase = get_phase_by_str(phase_str)  # "started"  if BEGAN_re.match(phase_str) else  "finished"
                # alg_obj_id = self.get_alg_node_id(("algorithm","алгоритм"))
                # assert alg_obj_id, "TraceError: no corresporning '{}' found for '{}'".format("algorithm' or 'алгоритм", name)
                alg_obj_id = self.alg_dict["entry_point"]["id"]
                assert alg_obj_id, f"TraceError: no entry_point found for '{name}'."
                result.append({
                      "id": self.newID(name),
                      # "action": name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": 1,
                      "text_line": ci,
                      "comment": comment,
                })
                
                if phase == "finished":
                    break  # трасса построена до конца!
                
                continue  # with next act
        
            # началось следование global_code 1-й раз
            # закончилось следование global_code 1-й раз
            # начался цикл my-while-1 1-й раз
            # началась развилка my-alt-1 1-й раз
            # началась функция main 1-й раз
            # выполнилась функция main 1-й раз
            # alternative over_color began 1st time
            #     alternative by_response ended 1st time
            m = re.match(r"""(?:({BEGAN_ru}|{ENDED_ru}|{EXECUTED_ru})\s+)?  # 1 phase (ru)
                (следование|развилка|цикл|функция|sequence|alternative|loop|function)   # 2 struct 
                \s+(\S+)                     # 3 name 
                (?:\s+({BEGAN_en}|{ENDED_en}|{EXECUTED_en}))?  # 4 phase (en)
                {Ith1}?   # 5 ith  (optional)
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                struct_str = m.group(2)
                phase_str = m.group(1) or m.group(4)
                assert phase_str, "TraceError: phase term (began/ended/executed) is missing at line {}".format(ci)
                if self.verbose: print("{} {}".format(phase_str, struct_str))
                #   {"id": 32, "action": "программа", "executes": 25, "gen": "she", "phase": "started", "n": null},
                struct = {
                            "следование": "sequence", 
                            "развилка": "alternative", 
                            "цикл": "loop", 
                            "функция": "func",
                            "function": "func",
                         }.get(struct_str, struct_str)
                name = m.group(3)
                ith = m.group(5)  if len(m.groups())>=5 else  None
                phase = get_phase_by_str(phase_str)
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                if struct == "func":
                    alg_obj_id = next(find_by_keyval_in("name", name, self.alg_dict["functions"]))["body"]["id"]
                result.append({
                      "id": self.newID(name),
                      # struct: name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act
        
            # условие развилки (цвет==зелёный) выполнилось 1-й раз - истина
            # условие цикла (while-cond-1) выполнилось 1-й раз - истина
            # условие (while-cond-1) выполнилось 1-й раз - ложь
            # condition (response_is_positive) executed 1st time - true
            # condition of alternative (color_is_red) executed 1st time - true
            m = re.match(r"""
                (?:условие|condition)
                \s*
                (развилки|цикла|of\s+alternative|of\s+loop)?  # 1 struct (optional)
                \s+ (\(.+\)|\S+)   # 2 cond name
                \s+ {EXECUTED}  # добавить остальные фазы - после расширения/усложнения логики
                {Ith1}?   # 3 ith  (optional)
                \s+ - >?    # - or ->
                \s+ (\S+)   # 4 value
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("условие {} {} выполнилось - {}".format(m.group(1) or "\b", m.group(2), m.group(4)))
                struct = {"развилки":"alternative", "цикла":"loop", }.get(m.group(1), "alternative or loop")
                name = m.group(2)
                value = m.group(4)
                ith = m.group(3)  if len(m.groups())>=3 else  None
                phase = "performed"  # "started"  if "начал" in m.group(1) else  "finished"
                # alg_obj_id = self.get_alg_node_id(name)
                cond_obj_id = self.get_alg_node_id(name, node_type="expr")
                if cond_obj_id is None:
                    # имя не позволяет найти элемент алгоритма
                    # поищем вверх начало ближайшей развилки и/или цикла
                    criterion = lambda d: (type(d) is dict and "id" in d and (
                            d["type"] in struct or 
                            "loop" in struct and "loop" in d["type"]
                        ))
                    nodes = list(find_by_predicate(self.alg_dict, criterion, find_one=False))
                    stmt_ids = [node["id"] for node in nodes]
                    for act in reversed(result):
                        if  act["executes"] in stmt_ids:
                            node = nodes[stmt_ids.index(act["executes"])]
                            cond_obj_id = node["cond"]["id"]
                            print()
                            print(f'warning: condition "{name}" at line {ci} resolved as {node["cond"]["name"]} (of {node["type"]}: {node["name"]})')
                            break
                    
                assert cond_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                
                # convert value to true / false if matches so
                value = parse_expr_value(value)
                # value = {
                #     "истина":True,
                #     "true"  :True,
                #     "ложь" :False,
                #     "false":False,
                #     }.get(value.lower(), value)
                if isinstance(value, bool):
                    self.boolean_chain.append(value)
                
                result.append({
                      "id": self.newID(name),
                      # "expr": name,
                      "name": name,
                      "value": value,
                      "executes": cond_obj_id,  # not alg_obj_id !
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act
            
            # ветка иначе началась 1-й раз
            # ветка иначе закончилась 1-й раз
            # else branch began 1st time
            m = re.match(r"""(?:
                    ветка\s+ин[аa]ч[еe]   # транслит букв (раз начал использовать, нужно себя обезопасить)
                |
                    else\s+branch
                )
                \s+
                    # (начал[оа]?с[ья]|закончил[оа]?с[ья])  # 1 phase
                ({BEGAN}|{ENDED})  # 1 phase
                {Ith1}?   # 2 ith  (optional)
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("ветка иначе {}".format(m.group(1)))
                # строка не хранит данных о развилке, найдём первую развилку выше ...
                else_branch_name = None
                for obj in reversed(result):
                    if "alternative" in obj:
                        else_branch_name = obj["alternative"] + "-else"  # используем правило формирования имени ветки "иначе"
                        break
                if else_branch_name is None:  # !!!!
                    # в трассе нет (ошибочная трасса!) - найдём первую попавшуюся ветку ИНАЧЕ в алгоритме (как часть развилки)
                    found = tuple(find_by_keyval_in("type", "else", self.alg_dict))
                    if found:
                        else_branch_name = found[0]["name"]
                    else:
                        raise ValueError("TraceError: no else_branch element found in algorithm to bound '{}' at line {}!".format("ветка иначе", ci))
                name = else_branch_name
                ith = m.group(2)  if len(m.groups())>=2 else  None
                phase = get_phase_by_str(m.group(1))  # "started"  if "начал" in m.group(1) else  "finished"
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format("ветка иначе", ci)
                result.append({
                      "id": self.newID(name),
                      # "branch": name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act

            # ветка условия развилки (цвет==зелёный) началась 1-й раз
            # ветка условия развилки (цвет==зелёный) закончилась 1-й раз
            # branch of condition (color_is_red) began 1st time
            m = re.match(r"""
                (?:
                    ветка
                    (?:\s+условия)?
                    (?:\s+развилки)?
                |
                    (?:alternative\s+)?
                    (?:condition\s+)?
                    branch
                |
                    branch
                    (?:\s+of\s+condition)?
                    (?:\s+of\s+alternative)?
                )
                \s+
                # \(?(\S+?.*?)\)?  # 1 cond name (optional braces not inclusive)
                (?: \((\S+?)\) | (\S+) )  # 1, 2 cond name (optional braces not inclusive)
                \s+
                    # (начал[оа]?с[ья]|закончил[оа]?с[ья])  # 3 phase
                ({BEGAN}|{ENDED})  # 3 phase
                    # (?:\s+(\d+)[-_]?й?\s+раз)?   # 4 ith  (optional)
                {Ith1}   # 4 ith  (optional)
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                name = m.group(1) or m.group(2)
                phase = get_phase_by_str(m.group(3))  # "started"  if "начал" in m.group(2) else  "finished"
                if self.verbose: print("ветка {} {}".format(name, phase))
                ith = m.group(4)  if len(m.groups())>=4 else  None
                alg_obj_id = self.get_alg_node_id([prfx+name for prfx in ("if-","elseif-")])  # префиксы для веток "if" и "else if" - ветка Иначе здесь не обрабатывается!
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                result.append({
                      "id": self.newID(name),
                      # "branch": name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act
                
            # началась итерация 1 цикла my-while-1
            # началась итерация 1 цикла ожидание
            # началась 1-я итерация цикла my-while-1
            # iteration 1 of loop my-while-1 began
            # 1st iteration of loop my-while-1 began
            m = re.match(r"""
                (?:({BEGAN_ru}|{ENDED_ru})\s+)?  # 1 phase_1 - (началась|закончилась)
                (?:
                    (?:итерация|iteration)\s+(\d+)         # 2 numb_1
                    |
                    {Ith1_femn}  # (\d+)[-_]?я?     # 3 numb_2
                    \s+(?:итерация|iteration)
                )\s+
                (?:цикла|of\s+loop)\s+
                (\S+)  # 4 loop name
                (?:\s+({BEGAN_en}|{ENDED_en}))?  # 5 phase_2
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} итерация цикла {}".format(m.group(1), m.group(4)))
                loop_name = m.group(4)
                name = loop_name + "_loop_body"  # тело цикла сделано отдельной сущностью
                ith = m.group(2) or m.group(3)
                phase = get_phase_by_str(m.group(1) or m.group(5))  # "started"  if "начал" in m.group(1) else  "finished"
                alg_obj_id = self.get_alg_node_id(loop_name)  # access body via loop
                loop_dict = next(find_by_keyval_in("id", alg_obj_id, self.alg_dict))
                alg_obj_id = loop_dict["body"]["id"]
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                
                count_dict = self.iteration_count_dict.get(alg_obj_id, {})
                ith = count_dict.get(phase, 0) + 1
                count_dict.update({phase: ith})
                  # Временное решение! Не работает с рекурсией (считает все вхождения, идентично exec_time). Нужно отталкиваться от акта начала цикла, и запоминать все связанные непосредственно с ним итерации.
                self.iteration_count_dict[alg_obj_id] = count_dict
                
                result.append({
                      "id": self.newID(name),
                      # "loop_name": name,
                      # Добавлять информацию об объемлющем акте цикла?..
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "iteration_n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act
            
            # выполнилась инициализация (день = 1) 1-й раз
            # выполнился переход (день=день+1) 1-й раз
            m = re.match(r"""
                ({EXECUTED})  # (выполнил[оа]?с[ья])  # 1 phase
                \s+
                (инициализация|переход|init|initialization|update)  # 2 struct
                \s+
                (\(.+\)|[^()\s]+)  # 3 name (optional braces inclusive!)
                {Ith1}?  # (?:\s+(\d+)[-_]?й?\s+раз)?   # 4 ith  (optional)
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} {} {}".format(m.group(1), m.group(2), m.group(4)))
                struct_str = m.group(2)
                struct = {"инициализация":"init", "initialization":"init", "переход":"update", }.get(struct_str, struct_str)
                name = m.group(3)
                ith = m.group(4)  if len(m.groups())>=4 else  None
                phase = "performed"
                alg_obj_id = self.get_alg_node_id(name)
                if alg_obj_id is None:
                    # имя не позволяет найти элемент алгоритма
                    # поищем вверх начало ближайшего цикла и возьмём имя из него
                    criterion = lambda d: (type(d) is dict and "id" in d and "loop" in d["type"])
                    nodes = list(find_by_predicate(self.alg_dict, criterion, find_one=False))
                    stmt_ids = [node["id"] for node in nodes]
                    for act in reversed(result):
                        if  act["executes"] in stmt_ids:
                            node = nodes[stmt_ids.index(act["executes"])]
                            alg_obj_id = node[struct]["id"]
                            print()
                            print(f'warning: {struct} "{name}" at line {ci} resolved as {node[struct]["name"]} (of {node["type"]}: {node["name"]})')
                            break
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                result.append({
                      "id": self.newID(name),
                      # "action": name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act
            
                
            # что-то выполнилось 1-й раз
            # greet executed 1st time 
            m = re.match(r"""
                (\S+)   # 1 name
                \s+
                ({BEGAN}|{ENDED}|{EXECUTED})  # 2 phase
                {Ith1}?   # 3 ith  (optional)
                """.format(**PHASE_dict), line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} {}".format(m.group(1), m.group(2)))
                name = m.group(1)
                ith = m.group(3)  if len(m.groups())>=3 else  None
                # phase = "performed"  # "started"  if "начал" in m.group(1) else  "finished"
                phase = get_phase_by_str(m.group(2))
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                result.append({
                      "id": self.newID(name),
                      # "action": name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                continue  # with next act

            
            # print("Warning: unknown trace line structure at line %d: "%ci, line)
            raise ValueError("TraceError: unknown trace line structure at line %d: %s"%(ci, line))

        return result
       
    
# TraceParser(test_tr_lines, ap).trace


def word_in(words, text):
    if not isinstance(words, (list,tuple)): words = [words]
    rgx = "|".join([r"\b%s\b"%re.escape(w) for w in words])
    return re.search(rgx, text) is not None

def extract_alg_name(line) -> str:
    """Берём слово, стоящее за словом "алгоритм" """
    words = line.split()
    choises = ("алгоритм", "algorithm")
    choice = [w for w in words if w in choises]
    if choice:
        choice = choice[0]
        i = words.index(choice)
    else:
        print("Warning: No", f"\"{'/'.join(choises)}\"", "in line:", line)
        return None
    if i == len(words) - 1:
        print("Warning: No algoritm name following", f'"{choise}"', "in line:", line)
        return None
    return words[i+1]

# extract_alg_name("line 15 // алгоритм 07_while (while в стиле foreach, с 2 действиями)")

def find_by_predicate(dict_or_list, pred=lambda x:(type(x) is dict), find_one=False, _not_entry=None):
    "plain list of dicts or objects of specified type"
    _not_entry = _not_entry or set()
    _not_entry.add(id(dict_or_list))
    if pred(dict_or_list):
        yield dict_or_list
        if find_one:
            return
    if isinstance(dict_or_list, dict):
        for v in dict_or_list.values():
            if id(v) not in _not_entry:
                yield from find_by_predicate(v, pred, _not_entry)
    elif isinstance(dict_or_list, (list, tuple, set)):
        for v in dict_or_list:
            if id(v) not in _not_entry:
                yield from find_by_predicate(v, pred, _not_entry)

def find_by_key_in(key, dict_or_list):
    if isinstance(dict_or_list, dict):
        for k, v in dict_or_list.items():
            if k == key:
                yield dict_or_list
            else:
                yield from find_by_key_in(key, v)
    elif isinstance(dict_or_list, (list, tuple, set)):
        for d in dict_or_list:
            yield from find_by_key_in(key, d)

def find_by_keyval_in(key, val, dict_or_list):
    if isinstance(dict_or_list, dict):
        for k, v in dict_or_list.items():
            if k == key and v == val:
                yield dict_or_list
            else:
                yield from find_by_keyval_in(key, val, v)
    elif isinstance(dict_or_list, (list, tuple, set)):
        for d in dict_or_list:
            yield from find_by_keyval_in(key, val, d)

# list(find_by_keyval_in("type", "sequence", ap.algorithm))


def parse_text_file(txt_file_path, encoding="utf8"):
    """Returns list of dicts like
    {
        "trace_name"    : str,
        "algorithm_name": str,
        "trace"         : list,
        "algorithm"     : dict,
        "header_boolean_chain" : list of bool, 
    }
    collected from specified file_path.
    """

    try:
        with open(txt_file_path, encoding=encoding) as f:
            text = f.read()
    except OSError as e:
        print(f"Error reading file {txt_file_path} :\n  " + str(e))
        return []

    print("="*40)
    print("Parsing algorithms and traces from".center(40))
    print(txt_file_path.center(40))
    print("="*40)
    
    valid_alg_trs = parse_algorithms_and_traces_from_text(text)

    print()
    print("Total in file (%s):" % txt_file_path)
    print("  Number of effective algorithms:", len( {
        trdct["algorithm_name"] 
        for trdct in valid_alg_trs 
        # if "erroneous" not in trdct["algorithm"]
        } ))
    print("  Number of valid traces:", len(valid_alg_trs))
    print()
    
    return valid_alg_trs
    
    
def parse_algorithms_and_traces_from_text(text: str):
    """Returns list of dicts like
    {
        "trace_name"    : str,
        "algorithm_name": str,
        "trace"         : list,
        "algorithm"     : dict,
        "header_boolean_chain" : list of bool, 
    }
    collected from specified text data.
    """

    text = text.replace("\t", " "*4)  # expand tabs to spaces (if any)
    lines = text.split("\n")
    text = None
    
    
    # Алгоритмы ...
    
    last_line = len(lines)-2
    alg_data = {}

    for i in range(0, last_line):
        if word_in(("алгоритм", "algorithm"), lines[i]) and '"algorithm"' not in lines[i]:
            # проверить начало алгоритма
            if not re.search(r"\{|функция|function", lines[i+1]):
                print("Ignored (no alg. begin): line", i, lines[i])
                continue
            # найти конец алгоритма: не ранее 3-х строк ниже названия и далее
            for j in range(i + 3, last_line):
                next_line = lines[j+1].strip()
                if not next_line or re.match(r"/\*|//|#", next_line):  # следующая - пустая или комментарий
                    if "}" in lines[j]:
                        # найдено
                        name = extract_alg_name(lines[i])
                        alg_data[name] = {
                            "lines": (i+1, j)  # строки текста алгоритма (вкл-но)
                        }
                        # print("line", i, name)  # , lines[i])
                    # иначе - не найдено
                    else:
                        print(f"Ignored line {i}: {lines[i]}\n\tas no '{'}'}' found at line {j}: {lines[j]}")
                    break



    # Трассы ....
                    
    last_line = len(lines)-1
    
    
    print("Algorithm names:", *list(alg_data.keys()))
    
    # регулярка для всех имён алгоритмов: одно целое слово (имя одного из алгоритмов) должно быть найдено в заголовке трассы
    alg_names_rgx = "|".join([r"\b%s\b" % re.escape(w) for w in alg_data.keys()])
    alg_names_rgx = re.compile(alg_names_rgx)
    
    tr_data = {}

    for i in range(0, last_line):
        if word_in(("началась программа", "program began"), lines[i]):
            # найти имя трассы
            name = None
            boolean_chain = None
            # ищем ссылку на алгоритм...
            for j in range(i-1, i-5, -1):  # проверяем 4 строки вверх
                m = alg_names_rgx.search(lines[j])
                if m:
                    alg_name = m.group(0)
                    # отбрасываем комментарий / strip comment out
                    name = re.sub(r"^\s*(?:/\*|//|#)\s*", "", lines[j])
                    
                    # найти цепочку из 0 и 1, стоящую за именем алгоритма (если есть)
                    boolean_chain = None # слово за именем алгоритма
                    words = name.split()
                    alg_name_i = words.index(alg_name)
                    if alg_name_i < len(words) - 1:
                        boolean_chain = words[alg_name_i + 1]
                        boolean_chain = re.sub(r"[^01]", "", boolean_chain)
                        boolean_chain = list(map({"0":False, "1":True}.get, boolean_chain))  # convert to boolean list
                    break
    
            if not name:
                print("Ignored (no reference to an algorithm found): line", i, lines[i])
                continue
            # найти конец трассы
            for j in range(i + 1, last_line):
                if "}" in lines[j+1]:  # закрывающая скобка
                    if word_in(("закончилась программа","program ended"), lines[j]):
                        # найдено
                        tr_data[name] = {
                            "alg_name": alg_name,
                            "boolean_chain": boolean_chain,  # последовательность из 0 и 1 - значения условий в порядке появления в трассе
                            # !
                            "lines":(i, j)  # строки текста трассы (вкл-но)
                        }

                        # print("line", i, name)
                    # иначе - не найдено
                    else:
                        print("Ignored: line", i, lines[i])
                    break

    # Парсинг трасс совместно с алгоритмами, указывая строки в файле ...
    
    for tr_name, tr_dict in tr_data.items():
        
        print()
        alg_name = tr_dict["alg_name"]
        if "alg_parser" not in alg_data[alg_name] and "erroneous" not in alg_data[alg_name]:
            print("Parsing algorithm:", alg_name, "...", end='\t')
            try:
                b,e = alg_data[alg_name]["lines"]
                alg_data[alg_name]["alg_parser"] = AlgorithmParser(lines[b:e+1])
                print("Success")
            except Exception as e:
                print("Error !")
                alg_data[alg_name]["erroneous"] = True
                print("Error parsing algorithm:", alg_name, ":")
                print(" ", e)
                raise e
        
        if "alg_parser" not in alg_data[alg_name]:
            print("Skipping trace:", tr_name, ", because the corresponding algorithm could not be parsed:", alg_name)
            continue
            
        print("Parsing trace:", tr_name, "...", end='\t')
        try:
            b,e = tr_dict["lines"]
            tr_dict["trace_parser"] = TraceParser(lines, alg_data[alg_name]["alg_parser"], start_line=b)
            
            # store boolean chain
            
            print("Success")
            
        except Exception as e:
            print("Error !")
            print("Error parsing trace:", tr_name, ":")
            print(" ", repr(e))
            raise e
            
            
    valid_alg_trs = [{
        "trace_name"    : nm,
        "algorithm_name": trdct["alg_name"],
        "trace"         : trdct["trace_parser"].trace,
        "algorithm"     : alg_data[trdct["alg_name"]]["alg_parser"].algorithm,
        "header_boolean_chain" : trdct["boolean_chain"], 
        
    } for nm, trdct in tr_data.items() if "trace_parser" in trdct]
    
    # print()
    # print("Total in file (%s):" % txt_file_path)
    # print("  Number of valid algorithms:", len( {nm for nm,adct in alg_data.items() if "erroneous" not in adct} ))
    # print("  Number of valid traces:", len(valid_alg_trs))
    # print()
    
    return valid_alg_trs
            

def parse_text_files(file_paths, encoding="utf8"):
    """Returns concatenation of lists of traces collected from specified file paths.
    """
    
    alg_trs = []
    
    for fpath in file_paths:
        alg_trs += parse_text_file(fpath, encoding=encoding)
    
    print("Number of traces with algorithms collected from", len(file_paths), "text file(s):", len(alg_trs))
    print()
    
    return alg_trs
            
def search_text_trace_files(directory="../handcrafted_traces/", file_extensions=(".txt", ".tr"), skip_starting_with_hypen=True, filter_file="filter.inf"):
    import os
    result_list = []
    search_in_dir = True
    if filter_file and os.path.exists(os.path.join(directory, filter_file)):
        try:
            with open(os.path.join(directory, filter_file)) as f:
                text = f.read()
            file_list = [s.strip() for s in text.split("\n") if s.strip()]
            text = None
            search_in_dir = False
        except OSError:
            pass

    if search_in_dir:
        file_list = os.listdir(directory)
    
    for fname in file_list:
        if not fname.endswith(file_extensions):
            continue
            
        if skip_starting_with_hypen and fname.startswith("-"):
            continue
            
        fpath = os.path.join(directory, fname)
        if not os.path.exists(fpath):
            # print("path does not exist: ", fpath)
            continue
            
        result_list.append(fpath)
    
    return result_list

def main():

	# parse_text_file("../handcrafted_traces/err_branching.txt")
	# parse_text_file("../handcrafted_traces/err_loops.txt")
	# parse_text_file("../handcrafted_traces/correct_branching.txt")
	# parse_text_file("../handcrafted_traces/correct_loops.txt")
    
    # parse_text_files([
    #     # "../handcrafted_traces/err_branching.txt",
    #     # "../handcrafted_traces/err_loops.txt",
    #     "../handcrafted_traces/correct_branching.txt",
    #     # "../handcrafted_traces/correct_loops.txt",
    #     "../handcrafted_traces/no_such_file.txt",
    # ])


    result = parse_text_files( search_text_trace_files() )
    from pprint import pprint
    pprint(result)
    

if __name__ == '__main__':
	main()
    
    # v = get_ith_expr_value(
    #         ("(", 1, 2, 3, 4, ")", ), 16
    #     )
    # print(v)
