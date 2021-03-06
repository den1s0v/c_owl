# -*- coding: utf-8 -*-
# blockly_helpers.py


### import xml.dom.minidom
from collections import OrderedDict

import xmltodict  # pip install xmltodict

try:
    from trace_gen.txt2algntr import AlgorithmParser, select_translation
except ModuleNotFounError:
    from txt2algntr import AlgorithmParser


SAMPLE_XML = """<xml xmlns="https://developers.google.com/blockly/xml">
  <block type="controls_named_if" id="Oa0Hq*ML|D*%YXrWRv:?" x="175" y="0">
    <mutation elseif="1"></mutation>
    <value name="NAME">
      <shadow type="text" id="u:xgnxdiRE)[dFP3+T=O">
        <field name="TEXT">A1</field>
      </shadow>
    </value>
    <value name="IF0">
      <block type="condition_with_values_block" id="s|ofuee1svxYDr~;XF].">
        <field name="COND_NAME">условие1</field>
        <field name="VALUES">0,1,1,(0)</field>
      </block>
    </value>
    <statement name="DO0">
      <block type="action" id="y=f=fO2waXj1Pvm=L]73">
        <field name="NAME">выполнить</field>
        <next>
          <block type="action" id=";|7JCCtdvDI#]P-#giUI">
            <field name="NAME">выполнить</field>
            <next>
              <block type="action" id="5m9BqTz(d%QtV|*4Ww}(">
                <field name="NAME">выполнить</field>
              </block>
            </next>
          </block>
        </next>
      </block>
    </statement>
    <value name="IF1">
      <block type="condition_with_values_block" id="/[2h.mCXtu,d7BLcitz$">
        <field name="COND_NAME">условие1</field>
        <field name="VALUES">0,1,1,(0)</field>
      </block>
    </value>
    <statement name="DO1">
      <block type="text_print" id="krpj`S||v(h`A8Z#UsdP">
        <value name="TEXT">
          <shadow type="text" id="Rt9g60j.l@.d(x0OC+dM">
            <field name="TEXT">Ветка ИНАЧЕ</field>
          </shadow>
        </value>
      </block>
    </statement>
    <next>
      <block type="controls_named_whileUntil" id="N,V]::HibT7kwWj6jP=q">
        <field name="MODE">WHILE</field>
        <value name="NAME">
          <shadow type="text" id="=_lTs1p,iUq`Du|{:C?.">
            <field name="TEXT">L1</field>
          </shadow>
        </value>
        <value name="BOOL">
          <block type="condition_with_values_block" id="x8qQt(+V5]gF$VNvGn:N">
            <field name="COND_NAME">условие2</field>
            <field name="VALUES">0,1,1,(0)</field>
          </block>
        </value>
        <statement name="DO">
          <block type="text_print" id=":IHk!Of*?_z2;AGt(}7p">
            <value name="TEXT">
              <shadow type="text" id="H?)kq!vV2qIlAaEBY|-:">
                <field name="TEXT">Wow</field>
              </shadow>
            </value>
            <next>
              <block type="text_print" id=":JlHlx9aI^9}KWXO3zxf">
                <value name="TEXT">
                  <shadow type="text" id="gYsmfDV.cPBUKhJmG,^0">
                    <field name="TEXT">Wow</field>
                  </shadow>
                </value>
                <next>
                  <block type="text_print" id="v]UQlIGU-{DLnk==L=w6">
                    <value name="TEXT">
                      <shadow type="text" id="k6F:bgIg*:8C:aGj7|3T">
                        <field name="TEXT">Wow</field>
                      </shadow>
                    </value>
                  </block>
                </next>
              </block>
            </next>
          </block>
        </statement>
        <next>
          <block type="controls_named_doWhileUntil" id="}=/^4VkY9|BE%40vYv_2">
            <field name="MODE">WHILE</field>
            <value name="NAME">
              <shadow type="text" id=";IJFiKa0oHr#Zl51BNPA">
                <field name="TEXT">L2</field>
              </shadow>
            </value>
            <statement name="DO">
              <block type="action" id="{JxF!S`oo-_i^T8Gf=pG">
                <field name="NAME">выполнить2</field>
                <next>
                  <block type="action" id="sb0YT@s7NAWbaHVnnf[@">
                    <field name="NAME">выполнить2</field>
                    <next>
                      <block type="action" id="enBpe`RAO:Hm;HKqWO6^">
                        <field name="NAME">выполнить2</field>
                      </block>
                    </next>
                  </block>
                </next>
              </block>
            </statement>
            <value name="BOOL">
              <block type="condition_with_values_block" id="_0~}mua1Qsy/_}o{%;mv">
                <field name="COND_NAME">условие3</field>
                <field name="VALUES">0,1,1,(0)</field>
              </block>
            </value>
          </block>
        </next>
      </block>
    </next>
  </block>
</xml>"""



def parse_xml(xml_string):
    doc = xmltodict.parse(xml_string)
    return doc



class AlgorithmXMLParser(AlgorithmParser):
    def __init__(self, xml_tree=None, start_id=1, verbose=0):
        super().__init__(xml_tree, start_id, verbose)
        # assert type(start_id) is int
        # self._maxID = max(start_id - 1, _maxAlgID)
        # self.verbose = verbose
        # self.clear()
        # if line_list:
        #     self.parse(line_list)


    # def newID(self, what=None):
    #     self._maxID += 1
    #     global _maxAlgID; _maxAlgID = self._maxID
    #     if what:
    #         if what in self.name2id:
    #             print("Warning: multiple objects named as '%s' !"%what,
    #                   "Old id/new id:", self.name2id[what],"/", self._maxID, "; Overriding with latter one.")
    #         self.name2id[what] = self._maxID
    #     return self._maxID


    def parse(self, xml_tree: OrderedDict):
        self.algorithm["global_code"]["body"] += self.parse_algorithm_ids(xml_tree)
        # найдём точку входа
        for func in self.algorithm["functions"]:
            if func["is_entry"]:
                self.algorithm["entry_point"] = func  # надеемся, что объект с id сформируется в ссылку на функцию ...
                break
        else:  # нет функции
            self.algorithm["entry_point"] = self.algorithm["global_code"]  # надеемся с id


    # def parse_expr(self, name: str, values=None) -> dict:
    #     "Нововведение: самостоятельный объект для выражений (пока - только условия)"
    #     if values:
    #         self.algorithm["expr_values"][name] = parse_expr_values(values)
    #     return {
    #         "id": self.newID(name),
    #         "type": "expr",
    #         "name": name,
    #         "act_name": select_translation(ru=f"условие '{name}'", en=f"condition '{name}'"),
    #     }

    # def parse_stmt(self, name:str) -> dict:
    #     ""
    #     return {
    #         "id": self.newID(name),
    #         "type": "stmt",
    #         "name": name,
    #         "act_name": select_translation(ru=f"действие '{name}'", en=f"statement '{name}'"),
    #     }

    def parse_algorithm_ids(self, xml_tree: OrderedDict) -> list:
        """Формирует список словарей объектов алгоритма в формате alg.json для ctrlstrct_run.py
            Функции автоматически добавляются в self.algorithm["functions"].
            Глобальный код возввращается списком statement'ов верхнего уровня.
        """
        
        # if self.verbose: print("begin  with", xml_tree.keys())
        
        parse_algorithm = self.parse_algorithm_ids  # синоним для простоты написания
        
        def make_loop_body(loop_name, stmt_List):
            name = loop_name + "_loop_body"
            return {
                    "id": self.newID(name),
                    "type": "sequence",
                    "name": name,
                    "act_name": select_translation(ru=f"итерация цикла '{loop_name}'", en=f"iteration of loop '{loop_name}'"),
                    "body": stmt_List,
            }

        if 'xml' in xml_tree:  # root
            xml = xml_tree['xml']
            if 'block' in xml:
                block = xml['block']
                # выбрать только первый корень, если создано несколько стопок (блоков)
                block = block[0] if isinstance(block, list) else block
                return parse_algorithm(block)
            else:
                if self.verbose: print("empty Algorithm XML!")
                return []
                
        if 'block' in xml_tree:
            block = xml_tree['block']
            # выбрать только первый корень, если создано несколько стопок (блоков)
            block = block[0] if isinstance(block, list) else block
            return parse_algorithm(block)
                
        block_NAME = None
        
        def get_named_member(node_list, name, name_field='@name'):
            if not isinstance(node_list, list):
                node_list = [node_list]
            for node in node_list:
                if name_field in node and (not name or node[name_field] == name):
                    return node
            return None
                
        # extract block's NAME
        if 'value' in xml_tree:
            value_NAME = get_named_member(xml_tree['value'], 'NAME')
            if value_NAME:
                text_key = next(iter({'shadow', 'block'} & set(value_NAME.keys())))
                block_NAME = value_NAME[text_key]['field']['#text']
                
                if self.verbose: print("block_NAME:", block_NAME)
        
        
        result = []
        # suggest_corrections = []

        # for entry_i in range(len(current_level_stmt_line_idx) - 1):
        if True:
            
            # функция main
            # ...

            # если цвет==зелёный  // my-alt-1
            # if color==green -> true,false,true // my-alt-1
            # если условие (цвет==зелёный) -> 101 // my-alt-1
            # if condition (color==green) -> 1(01) // my-alt-1
            if '@type' in xml_tree and xml_tree['@type'] == 'controls_named_if':
                if self.verbose: print("alt if")
                assert block_NAME
                result.append({
                    "id": self.newID(block_NAME),
                    "type": "alternative",
                    "name": block_NAME,
                    "act_name": select_translation(ru=f"альтернатива '{block_NAME}'", en=f"alternative '{block_NAME}'"),
                    "branches": []
                })
                # alt branches
                branch_type = "if"
                for i in range(20):  # максимум 20 веток у альтернативы
                    block_IFn = get_named_member(xml_tree['value'], 'IF%d' % i) if 'value' in xml_tree else None
                    block_DOn = get_named_member(xml_tree['statement'], 'DO%d' % i) if 'statement' in xml_tree else None
                    if not block_IFn and not block_DOn:
                        break  # ветки кончились
                    if bool(block_IFn) != bool(block_DOn):
                        print("XML WARNING (ignoring): IF{i} {not1}exists, DO{i} {not2}exists.".format(i=i, not1='' if block_IFn else "not ", not2='' if block_DOn else "not "))
                        break  # ошибка, прерываем просмотр
                        
                    assert bool(block_IFn) and bool(block_DOn), i
                    
                    block_key = next(iter({'shadow', 'block'} & set(block_IFn.keys())))
                    block_COND_VALUES = block_IFn[block_key]
                    
                    block_COND_NAME = get_named_member(block_COND_VALUES['field'], "COND_NAME")
                    cond_name = block_COND_NAME['#text']
                    branch_name = branch_type + "-" + cond_name
                    
                    block_VALUES = get_named_member(block_COND_VALUES['field'], "VALUES")
                    values = block_VALUES['#text']
                    
                    result[-1]["branches"] += [ {
                        "id": self.newID(branch_name),
                        "type": branch_type,
                        "name": branch_name,
                        "act_name": select_translation(ru=f"ветка ЕСЛИ с условием '{cond_name}'", en=f"IF branch with condition '{cond_name}'"),
                        "cond":  self.parse_expr(cond_name, values=values),
                        "body": parse_algorithm(block_DOn['block'] if 'block' in block_DOn else [])
                    } ]
                    
                    branch_type = "else-if"
                

                # иначе если цвет==желтый
                # иначе если условие (цвет==желтый)  -> true,false,true
                # else if color==yellow  -> 101
                # else if condition (color==yellow)
                # ...

                # иначе
                # else
                block_ELSE = get_named_member(xml_tree['statement'], 'ELSE') if 'statement' in xml_tree else None
                if block_ELSE:
                    if self.verbose: print("alt else")
                    branch_type = "else"
                    alt_name = block_NAME
                    branch_name = alt_name + "-" + branch_type  # имя ветки должно отличаться от имени ветвления
                    alt_obj = result[-1]
                    alt_obj["branches"] += [ {
                        "id": self.newID(branch_name),
                        "type": branch_type,
                        "name": branch_name,
                        "act_name": select_translation(ru=f"ветка ИНАЧЕ альтернативы '{alt_name}'", en=f"ELSE branch of alternative '{alt_name}'"),
                        "body": parse_algorithm(block_ELSE['block'] if 'block' in block_ELSE else [])
                        } ]


            # пока while-cond-1  // my-while-1
            # while my-cond-2   -> 101 // my-while-2
            if '@type' in xml_tree and xml_tree['@type'] == 'controls_named_whileUntil':
                if self.verbose: print("while")
                name = block_NAME  # имя цикла (пишется в комментарии)
                block_BOOL = get_named_member(xml_tree['value'], 'BOOL') if 'value' in xml_tree else None
                if not block_BOOL:
                    raise ValueError('Algorithm error: Missing condition of "%s" loop!' % block_NAME)

                block_DO = get_named_member(xml_tree['statement'], 'DO') if 'statement' in xml_tree else None
                if not block_DO:
                    raise ValueError('Algorithm error: Missing body of "%s" loop!' % block_NAME)
                    
                block_key = next(iter({'shadow', 'block'} & set(block_BOOL.keys())))
                block_COND_VALUES = block_BOOL[block_key]
                block_COND_NAME = get_named_member(block_COND_VALUES['field'], "COND_NAME")
                block_VALUES = get_named_member(block_COND_VALUES['field'], "VALUES")
                
                cond_name = block_COND_NAME['#text']  # условие цикла
                values = block_VALUES['#text']  # значения, принимаемые выражением по мере выполнения программы (опционально)
                result.append({
                    "id": self.newID(name),
                    "type": "while_loop",
                    "name": name,
                    "act_name": select_translation(ru=f"цикл '{name}'", en=f"loop '{name}'"),
                    "cond": self.parse_expr(cond_name, values=values),
                    "body":  make_loop_body(
                                name,
                                parse_algorithm(block_DO['block'] if 'block' in block_DO else [])
                            )
                })

            # делать   // my-dowhile-2
            #    ...
            # пока dowhile-cond-2
            # 
            # 
            # do   // my-dowhile-3
            #    ...
            # while dowhile-cond-3  -> 100011100
            if '@type' in xml_tree and xml_tree['@type'] == 'controls_named_doWhileUntil':
                if self.verbose: print("do while")
                name = block_NAME  # имя цикла (пишется в комментарии)
                
                loop_type = "do_while_loop"  # the default
                # field_MODE = get_named_member(xml_tree['field'], "MODE")  # the field removed from the Block
                # if field_MODE and '#text' in field_MODE and field_MODE['#text'] == 'UNTIL':
                #     loop_type = "do_until_loop"

                block_BOOL = get_named_member(xml_tree['value'], 'BOOL') if 'value' in xml_tree else None
                if not block_BOOL:
                    raise ValueError('Algorithm error: Missing condition of "%s" loop!' % block_NAME)

                block_DO = get_named_member(xml_tree['statement'], 'DO') if 'statement' in xml_tree else None
                if not block_DO:
                    raise ValueError('Algorithm error: Missing body of "%s" loop!' % block_NAME)
                    
                    
                block_key = next(iter({'shadow', 'block'} & set(block_BOOL.keys())))
                block_COND_VALUES = block_BOOL[block_key]
                block_COND_NAME = get_named_member(block_COND_VALUES['field'], "COND_NAME")
                block_VALUES = get_named_member(block_COND_VALUES['field'], "VALUES")
                
                cond_name = block_COND_NAME['#text']  # условие цикла
                values = block_VALUES['#text']  # значения, принимаемые выражением по мере выполнения программы (опционально)
                result.append({
                    "id": self.newID(name),
                    "type": loop_type,
                    "name": name,
                    "act_name": select_translation(ru=f"цикл '{name}'", en=f"loop '{name}'"),
                    "cond": self.parse_expr(cond_name, values=values),
                    "body": make_loop_body(
                                name,
                                parse_algorithm(block_DO['block'] if 'block' in block_DO else [])
                            )
                })


            # для день от 1 до 5 с шагом +1  // my-for-3
            # for day from 1 to 5 step +1  // my-for-4
            # ...

            # для каждого x в list  // my-for-in-4
            # foreach x in list -> 1110110  // my-for-in-5
            # for each x in list  // my-for-in-5
            # ...

            # {  // myseq-5  -  начало именованного следования
            # ...

            # одно слово - имя действия: "бежать"
            if '@type' in xml_tree and xml_tree['@type'] == 'action':
                if self.verbose: print("action")
                name = xml_tree['field']['#text']
                result.append( self.parse_stmt(name) )

            # print ( TEXT )
            if '@type' in xml_tree and xml_tree['@type'] == 'text_print':
                if self.verbose: print("print ( TEXT )")
                value_TEXT = get_named_member(xml_tree['value'], 'TEXT')
                if value_TEXT:
                    text_key = next(iter({'shadow', 'block'} & set(value_TEXT.keys())))
                    name = value_TEXT[text_key]['field']['#text']
                name = 'print("%s")' % name
                result.append( self.parse_stmt(name) )

            # # print("Warning: unknown control structure: ")
            # suggest = ""
            # if suggest_corrections:
            #     suggest = "\nThis syntax constructs may help:\n\t" + ('\n\t'.join(suggest_corrections))
            # raise ValueError("AlgorithmError: unknown control structure at line %d: '%s'%s"%(1 + ci + start_line, current_line, suggest))

        if 'next' in xml_tree:
            # a subsequent statement exists
            # if self.verbose: print("Entering next ...")
            result += parse_algorithm(xml_tree['next'])

        return result




def create_algorithm_from_blockly_xml(xml_string) -> AlgorithmParser:
    'just a wrapper for AlgorithmParser constructor'
    try:
        return AlgorithmXMLParser(parse_xml(xml_string))
    except Exception as e:
        print("Error !")
        print("Error parsing algorithm:")
        print(" ", e)
        raise e  # useful for debugging
        return str(e)

if __name__ == '__main__':
    # test it
    res = create_algorithm_from_blockly_xml(SAMPLE_XML)
    
    print(res.algorithm)
