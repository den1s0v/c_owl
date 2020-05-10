# txt2algntr.py - Text to algorithm and trace mapped.


import re


class AlgorithmParser:
    def __init__(self, line_list=None, start_id=1, verbose=0):
        assert type(start_id) is int
        self._maxID = start_id - 1
        self.verbose = verbose
        
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
        }
        
        if line_list:
            self.parse(line_list)
            
            
    def newID(self, what=None):
        self._maxID += 1
        if what:
            if what in self.name2id:
                print("Warning: multiple objects named as '%s' !"%what,
                      "Old id/new id:", self.name2id[what],"/", self._maxID, "; Overriding with latter one.")
            self.name2id[what] = self._maxID
        return self._maxID

    def parse(self, line_list: "list(str)"):
        self.algorithm["global_code"]["body"] += self.parse_algorithm_ids(line_list)
        
    def parse_expr(self, name:str) -> dict:
        "Нововведение: самостоятельный объект для выражений (пока - только условия)"
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
            if line_indents[i] < current_level:  # элемент волее верхнего уровня
                break

        current_level_stmt_line_idx.append(len(line_list))  # конец последнего

    #     print(current_level_stmt_line_idx)

        ci = 0  # current line index

        for entry_i in range(len(current_level_stmt_line_idx) - 1):
            i = current_level_stmt_line_idx[entry_i]
            e = current_level_stmt_line_idx[entry_i + 1] - 1
            if i < ci:
                continue

            ci = i
    #         print(ci, e)

            # функция main
            m = re.match(r"функция\s+(\S+)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("function")
                name = m.group(1)  # имя функции
                self.algorithm["functions"].append({
                      "id": self.newID(name),
                      "type": "func",
                      "name": name,  # имя функции
                      "is_entry": name == "main",
                      "param_list": [],
                      "body": parse_algorithm(line_list[i+2:e])  # исключая скобки { } вокруг тела
                })
                ci = e + 1
                continue  # with next stmt on current level

            # если цвет==зелёный  // my-alt-1
            # если условие (цвет==зелёный)  // my-alt-1
            m = re.match(r"""
                если
                (?:\s+условие)?   # optional
                \s+
                (\(.+\)|\S+)  # 1 cond_name
                \s+
                (?://|\#)\s*(\S+)  # 2 name
                """, line_list[ci].strip(), re.I|re.VERBOSE)
            if m:
                if self.verbose: print("alt if")
                name = m.group(2)  # имя альтернативы (пишется в комментарии)
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
                        "cond":  self.parse_expr(cond_name),
                        "branch": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                    } ]
                })
                ci = e + 1
                continue  # with next stmt on current level

            # иначе если цвет==желтый
            # иначе если условие (цвет==желтый)
            m = re.match(r"иначе\s+если(?:\s+условие)?\s+(\(.+\)|\S+)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("alt elseif")
                cond_name = m.group(1)  # условие else if (может быть в скобках)
                if cond_name[0]+cond_name[-1] == "()":
                    cond_name = cond_name[1:-1]      # удалить скобки
                branch_name = "elseif-"+cond_name  # имя ветки должно отличаться от имени условия
                assert len(result)>0 and result[-1]["type"] == "alternative", "Algorithm Error: 'иначе если' does not follow 'если' :\n\t"+line_list[ci].strip()
                alt_obj = result[-1]
                alt_obj["branches"] += [ {
                        "id": self.newID(branch_name),
                        "type": "else if",
                        "name": branch_name,
                        "cond":  self.parse_expr(cond_name),
                        "branch": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                    } ]
                ci = e + 1
                continue  # with next stmt on current level

            # иначе
            m = re.match(r"иначе", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("alt else")
                assert len(result)>0 and result[-1]["type"] == "alternative", "Algorithm Error: 'иначе' does not follow 'если' :\n\t"+line_list[ci].strip()
                alt_obj = result[-1]
                branch_name = alt_obj["name"]+"-else"  # имя ветки должно отличаться от имени ветвления
                alt_obj["branches"] += [ {
                        "id": self.newID(branch_name),
                        "type": "else",
                        "name": branch_name,
                        "branch": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                    } ]
                ci = e + 1
                continue  # with next stmt on current level


            # пока while-cond-1  // my-while-1
            m = re.match(r"пока\s+(\(.+\)|\S+)\s+(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("while")
                name = m.group(2)  # имя цикла (пишется в комментарии)
                cond_name = m.group(1)  # условие цикла (может быть в скобках)
                result.append({
                    "id": self.newID(name),
                    "type": "while",
                    "name": name,
                    "cond": self.parse_expr(cond_name),
                    "body":  parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                })
                ci = e + 1
                continue  # with next stmt on current level

            # делать   // my-dowhile-2
            #    ...
            # пока dowhile-cond-2
            m = re.match(r"делать\s+(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            m2 = e+1 < len(line_list)  and  re.match(r"пока\s+(\(.+\)|\S+)",   line_list[ e+1 ].strip(), re.I)
            if m and m2:
                if self.verbose: print("do while")
                name = m.group(1)  # имя цикла (пишется в комментарии)
                cond_name = m2.group(1)  # условие цикла (может быть в скобках)
                result.append({
                    "id": self.newID(name),
                    "type": "do while",
                    "name": name,
                    "cond": self.parse_expr(cond_name),
                    "body": parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                })
                ci = e + 2
                continue  # with next stmt on current level

            # для день от 1 до 5 с шагом +1  // my-for-3
            m = re.match(r"для\s+(\S+)\s+от\s+(\S+)\s+до\s+(\S+)\s+с\sшагом\s+(\S+)\s+(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            #                    ^ 1 var      ^ 2 from     ^ 3 to             ^ 4 step           ^ 5 name
            if m:
                if self.verbose: print("for")
                s_var =  m.group(1)  # переменная цикла
                s_from = m.group(2)  # нижняя граница цикла
                s_to =   m.group(3)  # верхняя граница цикла
                s_step = m.group(4)  # шаг цикла
                name =   m.group(5)  # имя цикла (пишется в комментарии)
                result.append({
                    "id": self.newID(name),
                    "type": "for",
                    "name": name,
                    "variable": s_var,
                    "init":   self.parse_stmt("{}={}".format(s_var, s_from)),
                    "cond":   self.parse_expr("{}<={}".format(s_var,s_to)),
                    "update": self.parse_stmt("{v}={v}{:+d}".format(int(s_step), v=s_var)),
                    "body":  parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                })
                ci = e + 1
                continue  # with next stmt on current level

            # для каждого x в list  // my-for-in-4
            m = re.match(r"для\s+каждого\s+(\S+)\s+в\s+(\S+)\s+(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            #                              ^ 1 var     ^ 2 in             ^ 3 name
            if m:
                if self.verbose: print("foreach")
                s_var = m.group(1)  # переменная цикла
                s_container = m.group(2)  # контейнер
                name =   m.group(3)  # имя цикла (пишется в комментарии)
                result.append({
                    "id": self.newID(name),
                    "type": "foreach",
                    "name": name,
                    "variable": s_var,
                    "container": s_container,
                    "init":   self.parse_stmt("{}={}.first()".format(s_var, s_container)),
                    "cond":   self.parse_expr("{}!={}.last()".format(s_var,s_container)),
                    "update": self.parse_stmt("{v}=next({},{v})".format(s_container, v=s_var)),
                    "body":  parse_algorithm(line_list[i+1:e+1])  # скобки { } вокруг тела могут отсутствовать
                })
                ci = e + 1
                continue  # with next stmt on current level


            # {  // myseq-5  -  начало именованного следования
            m = re.match(r"\{\s+(?://|#)\s*(\S+)", line_list[ci].strip(), re.I)
            if m:
                if self.verbose: print("named sequence")
                name =   m.group(1),  # имя следования (пишется в комментарии)
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


# ap = AlgorithmParser(test_lines)
# ap.algorithm

class TraceParser:
    def __init__(self, line_list=None, alg_parser_obj=None, start_id=1, start_line=0, end_line=None, verbose=0):
        assert type(start_id) is int
        self._maxID = start_id - 1
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
        
        if line_list and self.alg_dict:
            self.parse(line_list, self.alg_dict, self.name2id, start_line, end_line)
            
    def get_alg_node_id(self, name):
        if isinstance(name, (list, set, tuple)):
            r = None
            for n in name:
                r = self.get_alg_node_id(n)
                if r:
                    break
        else:
            r = self.name2id.get(name, None)
            if not r and name[0]+name[-1] == "()":
                r = self.get_alg_node_id(name[1:-1])
            if not r:
                name = name.replace(' ','')
                if not self.name2id_no_whitespace:
                    # копия словаря с ключами, из которых вырезаны пробелы
                    self.name2id_no_whitespace = { n.replace(' ',''):v for n,v in self.name2id.items() }
                # поищем без пробелов
                r = self.name2id_no_whitespace.get(name, None)
                
        return r
            
    def newID(self, what=None, owerwrite=False):
        self._maxID += 1
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
        
        self.trace += self.parse_trace_by_alg(line_list, start_line, end_line)
        
        return self
        
    def parse_trace_by_alg(self, line_list: "list(str)", start_line=0, end_line=None) -> list:
        """Формирует плоский список объектов трассы в формате trace.json для ctrlstrct_run.py
            Функции автоматически добавляются в self.algorithm["functions"].
            Глобальный код возввращается списком statement'ов верхнего уровня.
        """
        
        # parse_trace = self.parse_trace_by_alg  # синоним для простоты написания

        result = []
        
        ci = start_line
        end_line = end_line or len(line_list)
        
        for line in line_list[ci:]:
        
            if ci >= end_line or not line:
                break
        
            line = line.strip()
            
            # ...  // comment
            m = re.search(r"\{\s+(?://|#)\s*(.+)$", line, re.I)
            comment = m and m.group(1) or ""
        
            # началась программа
            # закончилась программа
            m = re.match(r"(началась|закончилась)\s+программа", line, re.I)
            if m:
                if self.verbose: print("{} программа".format(m.group(1)))
                #   {"id": 32, "action": "программа", "executes": 25, "gen": "she", "phase": "started", "n": null},
                name = "программа"
                phase = "started"  if m.group(1) == "началась" else  "finished"
                alg_obj_id = self.get_alg_node_id(("algorithm","алгоритм"))
                assert alg_obj_id, "TraceError: no corresporning '{}' found for '{}'".format("algorithm' or 'алгоритм", name)
                result.append({
                      "id": self.newID(name),
                      # "action": name,
                      "name": name,
                      "executes": alg_obj_id,
                      "phase": phase,
                      # "n": None,
                      "text_line": ci,
                      "comment": comment,
                })
                ci += 1
                
                if phase == "finished":
                    break  # трасса построена до конца!
                
                continue  # with next act
        
            # началось следование global_code 1-й раз
            # закончилось следование global_code 1-й раз
            # начался цикл my-while-1 1-й раз
            # началась развилка my-alt-1 1-й раз
            # началась функция main 1-й раз
            # выполнилась функция main 1-й раз
            m = re.match(r"""(начал[оа]?с[ья]|закончил[оа]?с[ья]|выполнил[оа]?с[ья])  # 1 phase 
                \s+
                (следование|развилка|цикл|функция)   # 2 struct 
                \s+(\S+)                     # 3 name 
                (?:\s+(\d+)[-_]?й?\s+раз)?   # 4 ith  (optional)
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} {}".format(m.group(1), m.group(2)))
                #   {"id": 32, "action": "программа", "executes": 25, "gen": "she", "phase": "started", "n": null},
                struct = {
                            "следование":"sequence", 
                            "развилка":"alternative", 
                            "цикл":"loop", 
                            "функция":"func"
                         }[m.group(2)]
                name = m.group(3)
                ith = m.group(4)  if len(m.groups())>=4 else  None
                phase = "started"  if "начал" in m.group(1) else  ("finished"  if "закончил" in m.group(1) else  "performed")
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
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
                ci += 1
                continue  # with next act
        
            # условие развилки (цвет==зелёный) выполнилось 1-й раз - истина
            # условие цикла (while-cond-1) выполнилось 1-й раз - истина
            # условие (!!) (while-cond-1) выполнилось 1-й раз - истина
            m = re.match(r"""условие
                \s*
                (развилки|цикла)?  # 1 struct (optional)
                \s+
                (\(.+\)|\S+)   # 2 cond name 
                \s+
                выполнил[оа]?с[ья]
                (?:\s+(\d+)[-_]?й?\s+раз)?   # 3 ith  (optional)
                \s+
                -
                \s+
                (\S+)   # 4 value
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("условие {} {} выполнилось - {}".format(m.group(1) or "\b", m.group(2), m.group(4)))
                # struct = {"развилки":"alternative", "цикла":"loop", }.get(m.group(1))
                name = m.group(2)
                value = m.group(4)
                ith = m.group(3)  if len(m.groups())>=3 else  None
                phase = "performed"  # "started"  if "начал" in m.group(1) else  "finished"
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                result.append({
                      "id": self.newID(name),
                      # "expr": name,
                      "name": name,
                      "value": value,
                      "executes": alg_obj_id,
                      "phase": phase,
                      "n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                ci += 1
                continue  # with next act
            
            # ветка иначе началась 1-й раз
            # ветка иначе закончилась 1-й раз
            m = re.match(r"""ветка
                \s+
                ин[аa]ч[еe]   # транслит букв (раз начал использовать, нужно себя обезопасить)
                \s+
                (начал[оа]?с[ья]|закончил[оа]?с[ья])  # 1 phase
                (?:\s+(\d+)[-_]?й?\s+раз)?   # 2 ith  (optional)
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("ветка иначе {}".format(m.group(1)))
                # строка не хранит данных о развилке, найдём первую развилку выше ...
                else_branch_name = None
                for obj in reversed(result):
                    if "alternative" in obj:
                        else_branch_name = obj["alternative"] + "-else"  # используем правило формирования имени ветки "иначе"
                        break
                if else_branch_name is None:
                    # в трассе нет (ошибочная трасса!) - найдём первую попавшуюся ветку ИНАЧЕ в алгоритме (как часть развилки)
                    found = tuple(find_by_keyval_in("type", "else", self.alg_dict))
                    if found:
                        else_branch_name = found[0]["name"]
                    else:
                        raise ValueError("TraceError: no else_branch element found in algorithm to bound '{}' at line {}!".format("ветка иначе", ci))
                name = else_branch_name
                ith = m.group(2)  if len(m.groups())>=2 else  None
                phase = "started"  if "начал" in m.group(1) else  "finished"
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
                ci += 1
                continue  # with next act

            # ветка условия развилки (цвет==зелёный) началась 1-й раз
            # ветка условия развилки (цвет==зелёный) закончилась 1-й раз
            m = re.match(r"""ветка
                (?:\s+условия)?
                (?:\s+развилки)?
                \s+
                \(?(\S+?.*?)\)?  # 1 cond name (optional braces not inclusive)
                \s+
                (начал[оа]?с[ья]|закончил[оа]?с[ья])  # 2 phase
                (?:\s+(\d+)[-_]?й?\s+раз)?   # 3 ith  (optional)
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("ветка {} {}".format(m.group(1), m.group(2)))
                name = m.group(1)
                ith = m.group(3)  if len(m.groups())>=3 else  None
                phase = "started"  if "начал" in m.group(2) else  "finished"
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
                ci += 1
                continue  # with next act
                
            # началась итерация 1 цикла my-while-1
            # началась 1-я итерация цикла my-while-1
            m = re.match(r"""
                (начал[оа]?с[ья]|закончил[оа]?с[ья])  # 1 phase
                \s+
                (?:
                    итерация\s+(\d+)         # 2 numb_1
                    |
                    (\d+)[-_]?я?\s+итерация     # 3 numb_2
                )
                (?:\s+цикла)
                \s+
                (\S+)  # 4 loop name
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} итерация цикла {}".format(m.group(1), m.group(4)))
                loop_name = m.group(4)
                name = loop_name  # !!!! Используем имя цикла, Потому что тело цикла не сделано отдельной сущностью
                ith = m.group(2)  or  m.group(3)
                phase = "started"  if "начал" in m.group(1) else  "finished"
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format(name, ci)
                result.append({
                      "id": self.newID(name),
                      # "loop_name": name,    # имя цикла !
                      "name": name,    # имя цикла !
                      "executes": alg_obj_id,
                      "phase": phase,
                      "iteration_n": ith,
                      "text_line": ci,
                      "comment": comment,
                })
                ci += 1
                continue  # with next act
            
            # выполнилась инициализация (день = 1) 1-й раз
            # выполнился переход (день=день+1) 1-й раз
            m = re.match(r"""
                (выполнил[оа]?с[ья])  # 1 phase
                \s+
                (инициализация|переход)  # 2 struct
                \s+
                (\(.+\)|\S+)  # 2 name (optional braces inclusive!)
                (?:\s+(\d+)[-_]?й?\s+раз)?   # 3 ith  (optional)
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} {} {}".format(m.group(1), m.group(2), m.group(4)))
                struct = m.group(2)
                name = m.group(3)
                ith = m.group(4)  if len(m.groups())>=4 else  None
                phase = "performed"
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
                ci += 1
                continue  # with next act
            
                
            # что-то выполнилось 1-й раз
            m = re.match(r"""(\S+)   # 1 name
                \s+
                (выполнил[оа]?с[ья])  # 2 phase
                (?:\s+(\d+)[-_]?й?\s+раз)?   # 3 ith  (optional)
                """, line, re.I | re.VERBOSE)
            if m:
                if self.verbose: print("{} {}".format(m.group(1), m.group(2)))
                name = m.group(1)
                ith = m.group(3)  if len(m.groups())>=3 else  None
                phase = "performed"  # "started"  if "начал" in m.group(1) else  "finished"
                alg_obj_id = self.get_alg_node_id(name)
                assert alg_obj_id, "TraceError: no corresporning alg.element found for '{}' at line {}".format("ветка иначе", ci)
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
                ci += 1
                continue  # with next act

            
            # print("Warning: unknown trace line structure at line %d: "%ci, line)
            raise ValueError("TraceError: unknown trace line structure at line %d: %s"%(ci, line))
            ci += 1

        return result
       
    
# TraceParser(test_tr_lines, ap).trace


def word_in(words, text):
    if not isinstance(words, (list,tuple)): words = [words]
    rgx = "|".join([r"\b%s\b"%re.escape(w) for w in words])
    return re.search(rgx, text) is not None

def extract_alg_name(line) -> str:
    """Берём слово, стоящее за словом "алгоритм" """
    words = line.split()
    if "алгоритм" not in words:
        print("Warning: No", '"алгоритм"', "in line:", line)
        return None
    i = words.index("алгоритм")
    if i+1 == len(words):
        print("Warning: No algoritm name following", '"алгоритм"', "in line:", line)
        return None
    return words[i+1]

# extract_alg_name("line 15 // алгоритм 07_while (while в стиле foreach, с 2 действиями)")

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

    try:
        with open(txt_file_path, encoding=encoding) as f:
            text = f.read()
    except OSError as e:
        print(f"Error reading file {txt_file_path} :\n  " + str(e))
        return []

    text = text.replace("\t", " "*4)
    lines = text.split("\n")
    text = None
    
    
    print("="*40)
    print("Parsing algorithms and traces from".center(40))
    print(txt_file_path.center(40))
    print("="*40)
    
    # Алгоритмы ...
    
    last_line = len(lines)-2
    alg_data = {}

    for i in range(0, last_line):
        if word_in("алгоритм", lines[i]):
            # проверить начало алгоритма
            if not re.search(r"\{|функция", lines[i+1]):
                print("Ignored (no alg. begin): line", i, lines[i])
                continue
            # найти конец алгоритма
            for j in range(i + 3, last_line):
                if not lines[j+1].strip() or re.search(r"/\*|//|#", lines[j+1]):  # пустая или комментарий
                    if "}" in lines[j]:
                        # найдено
                        name = extract_alg_name(lines[i])
                        alg_data[name] = {
                            "lines":(i+1, j)  # строки текста алгоритма (вкл-но)
                        }
                        # print("line", i, name)  # , lines[i])
                    # иначе - не найдено
                    else:
                        print("Ignored: line", i, lines[i])
                    break



    # Трассы ....
                    
    last_line = len(lines)-1
    
    alg_names_rgx = "|".join([r"\b%s\b"%re.escape(w) for w in alg_data.keys()])
    alg_names_rgx = re.compile(alg_names_rgx)
    
    tr_data = {}

    for i in range(0, last_line):
        if word_in("началась программа", lines[i]):
            # найти имя трассы
            name = None
            for j in range(i-1, i-5, -1):  # проверяем 4 строки вверх
                m = alg_names_rgx.search(lines[j])
                if m:
                    alg_name = m.group(0)
                    # отбрасываем комментарий
                    name = re.sub(r"^\s*(?:/\*|//|#)\s*", "", lines[j])
    
                    break
            if not name:
                print("Ignored (no related algorithm found by name): line", i, lines[i])
                continue
            # найти конец трассы
            for j in range(i + 1, last_line):
                if "}" in lines[j+1]:  # закрывающая скобка
                    if word_in("закончилась программа", lines[j]):
                        # найдено
                        tr_data[name] = {
                            "alg_name": alg_name,
                            "lines":(i+1, j)  # строки текста трассы (вкл-но)
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
        
        if "alg_parser" not in alg_data[alg_name]:
            print("Skipping trace:", tr_name, ", because no corresporning algorithm parsed:", alg_name)
            continue
            
        print("Parsing trace:", tr_name, "...", end='\t')
        try:
            b,e = tr_dict["lines"]
            tr_dict["trace_parser"] = TraceParser(lines, alg_data[alg_name]["alg_parser"], start_line=b)
            print("Success")
            
        except Exception as e:
            print("Error !")
            print("Error parsing trace:", tr_name, ":")
            print(" ", e)
            
            
    valid_alg_trs = [{
        "trace_name"    : nm,
        "algorithm_name": trdct["alg_name"],
        "trace"         : trdct["trace_parser"].trace,
        "algorithm"     : alg_data[trdct["alg_name"]]["alg_parser"].algorithm,
        
    } for nm,trdct in tr_data.items() if "trace_parser" in trdct]
    
    print()
    print("Total in file (%s):" % txt_file_path)
    print("  Number of valid algorithms:", len( {nm for nm,adct in alg_data.items() if "erroneous" not in adct} ))
    print("  Number of valid traces:", len(valid_alg_trs))
    print()
    
    return valid_alg_trs
            

def parse_text_files(file_paths, encoding="utf8"):
    alg_trs = []
    
    for fpath in file_paths:
        alg_trs += parse_text_file(fpath, encoding=encoding)
    
    print("Number of traces with algorithms collected from", len(file_paths), "text file(s):", len(alg_trs))
    print()
    
    return alg_trs
            
def search_text_trace_files(directory="../handcrafted_traces/", file_extensions=(".txt", ".tr"), skip_starting_with_hypen=True):
    import os
    result_list = []
    file_list = os.listdir(directory)
    
    for fname in file_list:
        if not fname.endswith(file_extensions):
            continue
            
        if skip_starting_with_hypen and fname.startswith("-"):
            continue
            
        fpath = os.path.join(directory, fname)
        if not os.path.exists(fpath):
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


    parse_text_files( search_text_trace_files() )
    

if __name__ == '__main__':
	main()
