
var cm_alg, cm_trace;  // CodeMirror objects
var e_alg, e_trace;  // CodeMirror editor objects

$(document).ready(function(){
    
    define_syntax_mode();  // создать подсветку "algtracemode"
    
    cm_config = {
      lineNumbers: true,
      theme: "elegant",
      mode: "algtracemode"
    }
  
    cm_alg = CodeMirror.fromTextArea(document.getElementById("code_editor"), cm_config);
    cm_trace = CodeMirror.fromTextArea(document.getElementById("trace_preview"), cm_config);
    
    cm_alg.setSize("70%", "20%");
    cm_trace.setSize("70%", "35%");
    e_alg = cm_alg.getDoc();
    e_trace = cm_trace.getDoc();
    
    var change_timer = null;
    
    cm_alg.on('changes', function(...args) {
      // debug log
      // console.log(args)
      plan_task_creation(1000);  // дать время на несколько операций редактирования
    })
    
    // запланировать send_task_creation через указанное время
    function plan_task_creation(delay=0) {
      if (change_timer) {
        clearTimeout(change_timer);
      }
      change_timer = setTimeout(send_task_creation, delay);
    }
    
    function send_task_creation() {
      change_timer = null;
      console.log('send_task_creation() !')
      
      data = {
        alg: e_alg.getValue(),
        trace_lines: 0,  // [пока константа]  N - число выбранных для инициализации решения строк трассы
      }
      
      $.ajax({
        url: '/creating_task', 
        method: 'post',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(data),
        beforeSend: function(data){
            $('#syntax_error_description').html('Проверка алгоритма...')
        },
        success: function(data){
          console.log("feedback from /creating_task:")
          console.log(data)
          if (data.errors !== undefined) {
            const err_msg = data.errors.join(",");
            $('#syntax_error_description').html(err_msg)
          }
        },
        error: function(data){
          $('#syntax_error_description').html('Ошибка на сервере ... :-\\')
        }
      });
    }

    
    $("#load-correct").click(function() {
        if (cm_alg.isReadOnly())
        {
        alert("Невозможно вставить данные примера сейчас.\nПоля вода деактивированы.")
        }
        else
        {
            e_alg.setValue(ALGORITHM);
            e_trace.setValue(CORRECT_TRACE)
        }
    });   
    
    // $("#load-incorrect").click(function(){
    //     if (cm_alg.isReadOnly())
    //     {
    //     alert("Невозможно вставить данные примера сейчас.\nСначала активируйте поля, нажав кнопку 'Редактировать'.")
    // }
    // else
    // {
    //     e_alg.setValue(ALGORITHM);
    //     e_trace.setValue(INCORRECT_TRACE)
    // }
    // // e_trace.addLineClass(3, "background", "error-line")
    // });   
    
    
    $("#send_text").click(function(){
        if (cm_alg.isReadOnly())
          // fields was not changed, so reset the values to the stored before previous send
          load_fields()
        
      // Заблокировать
      set_editors_enabled(false);
      
      $("#new").html("Редактировать (активировать поля)")
       
      data = {
          alg: e_alg.getValue(),
          trace: e_trace.getValue()
        }

      save_fields(data)  // alg, trace -> localStorage
      
        $.ajax({
          url: '/process_as_text', 
          method: 'post',
          dataType: 'json',
          contentType: "application/json",
          data: JSON.stringify(data),
          beforeSend: function(data){
            processing_callback("wait")
          },
          success: function(data){
            processing_callback(data)
          },
          error: function(data){
            processing_callback("fail")
          }
        });
    });

    $("#send_json").click(function(){
      data = JSON_example

        $.ajax({
          url: '/process_as_json', 
          method: 'post',
          dataType: 'json',
          contentType: "application/json",
          data: JSON.stringify(data),
          beforeSend: function(data){
            processing_callback("wait")
          },
          success: function(data){
            processing_callback(data)
          },
          error: function(data){
            processing_callback("fail")
          }
        });
      
    });
    
    
    // ТОЛЬКО ДЛЯ УДОБСТВА ОТЛАДКИ !
    // read text stored at localStorage
    load_fields()
});


function processing_callback(response="wait")
{
  if(response == "wait")
  {
    $('#status').html("Подождите ...");
    return
  }
  
  if(response == "fail")
  {
    $('#status').html("Произошла ошибка при запросе к серверу (он мог поймать ошибку, быть занят или недоступен). Пожалуйста, попробуйте еще раз.<br>(обратите внимание, что сервер работает в режиме отладки, поэтому может реагировать медленно и зависать на параллельных запросах.)");
    return
  }
  
  if(response.messages)
  { 
    mistakes_count = 0
    if(response.mistakes)
      mistakes_count = response.mistakes.length
    
    explanations = []
    
    if(response.mistakes)
    {
      // add mistakes annotation to the end of each trace lines
      line2names = {}
      for(let m of response.mistakes)
      {
        if(m["text_line"])
        {
          const line = parseInt(m["text_line"])
          if(!line2names[line])
            line2names[line] = m["names"]
          else
            line2names[line] = line2names[line].concat(m["names"])
  
          if(m["explanation"])
          {
            // explanations = explanations.concat(m["explanations"])
            explanations.push([line, "Строка <b>" + line + "</b>: " + m["explanation"]])
          }
        }
      }
      
      explanations.sort(function compare(a, b) {return a[0] - b[0]})
      explanations = explanations.map( function(a) {return a[1]} )
      
      lines = load_field("trace").split('\n')
      for(let i in line2names)
      {
        if(1 <= i && i <= lines.length)
        {
          names = [...new Set(line2names[i])]
          names.sort()
          addition = '  // error: ' + names.join(', ')
          if(! lines[i-1].endsWith(addition))
            lines[i-1] += addition
        }
        else
          console.warn({i, lines_length: lines.length})
      }
      var text = lines.join("\n")
      e_trace.setValue(text)
    }
    
    messages = (response.messages.concat(explanations)).join("\n<br>")
    
    $('#status').html("Ответ сервера:\n" + messages + '\n<br>' 
      + mistakes_count + ` ошибок (во внутреннем представлении).`
      // + '\n<br>' + JSON.stringify(response)
      );
    
  } 
}


function set_editors_enabled(enabled=true)
{
  cm_alg.setOption("readOnly", !enabled)
  cm_trace.setOption("readOnly", !enabled)
  const color = enabled? "#fff" : "#eee";
  $('.CodeMirror').css('background', color);
}


////// local storage //////

function save_fields(data=null)
{
  if(data === null)
  {
    data = {
      alg: e_alg.getValue(),
      trace: e_trace.getValue()
      
    }
  }
  
  localStorage.algtrace = JSON.stringify(data);
}

function load_fields()
{
    e_alg.setValue(load_field("alg"))
    e_trace.setValue(load_field("trace"))
}

// pass "alg" or "trace"
function load_field(field_name)
{
  str = localStorage.algtrace
  if(!str)
  {
    return ''
  }
  
  let data = JSON.parse( str );
  return data[field_name]
}



////////// CM : Custom syntax //////////


function define_syntax_mode() {

  keyword_re = /(?:начался|началась|началось|began|закончился|закончилась|закончилось|ended|выполнился|выполнилась|выполнилось|executed|evaluated|calculated|если|иначе|делать|пока|для|от|до|шаг|с\s+шагом|if|else|do|while|for|from|to|with\s+step|step|каждого|в|из|по|к|foreach|each|in)(?:\s|$)/i
  
  struct_re = /развилка|развилки|альтернативная|ветка|branch|alternative|условия|переход|update|итерация|iteration|иначe|условие|цикла|condition|of|loop|инициализация|init|initialization|цикл|следование|sequence/i
  
  // выполнилось
  CodeMirror.defineSimpleMode("algtracemode", {
    // The start state contains the rules that are intially used
    start: [
      {regex: keyword_re, token: "keyword"},
      {regex: /true|false|ложь|истина/i, token: "atom"},
      {regex: /\d+(?:st|nd|rd|th)?/i,
        // /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
       token: "number"},
      {regex: /(?:\/\/|#).*/, token: "comment"},
      {regex: struct_re, token: "struct"},
      {regex: /действие|action/i, token: "action"},
      {regex: /программа|program/i, token: "program"},
      {regex: /функция|function/i, token: "function"},
      {regex: /й|раз|time/i, token: null},
      {regex: /[\wа-яё]+/i, token: "variable"}
    ],
    meta: {
      dontIndentStates: ["comment"],
      lineComment: "//"
    }
  });
}


//////// Debug ////////

const ALGORITHM = `пока не_зелёный -> истина,истина,ложь  // ожидание
{
    если цвет_красный -> истина,ложь  // по_цвету
  {
    ждать
  }
    иначе если цвет_жёлтый -> ложь
  {
        приготовиться
  }
}
`;
const CORRECT_TRACE = `началась программа
начался цикл ожидание 1-й раз
условие цикла (не_зелёный) выполнилось 1-й раз - истина
началась итерация 1 цикла ожидание
началась развилка по_цвету 1-й раз
условие развилки (цвет_красный) выполнилось 1-й раз - истина
ветка условия развилки (цвет_красный) началась 1-й раз
ждать выполнилось 1-й раз
ветка условия развилки (цвет_красный) закончилась 1-й раз
закончилась развилка по_цвету 1-й раз
закончилась итерация 1 цикла ожидание
условие цикла (не_зелёный) выполнилось 2-й раз - истина
началась итерация 2 цикла ожидание
началась развилка по_цвету 2-й раз
условие развилки (цвет_красный) выполнилось 2-й раз - ложь
условие развилки (цвет_жёлтый) выполнилось 1-й раз - ложь
закончилась развилка по_цвету 2-й раз
закончилась итерация 2 цикла ожидание
условие цикла (не_зелёный) выполнилось 3-й раз - ложь
закончился цикл ожидание 1-й раз
закончилась программа
`;
const INCORRECT_TRACE = `началась программа
начался цикл ожидание 1-й раз
началась итерация 1 цикла ожидание  // error: DisplacedAct
условие цикла (не_зелёный) выполнилось 1-й раз - истина  // error: MisplacedDeeper, DisplacedAct
началась развилка по_цвету 1-й раз  // error: MissingIterationAfterSuccessfulCondition, TooEarly
условие развилки (цвет_красный) выполнилось 1-й раз - истина
ветка условия развилки (цвет_красный) началась 1-й раз
ждать выполнилось 1-й раз
ветка условия развилки (цвет_красный) закончилась 1-й раз
закончилась развилка по_цвету 1-й раз
закончилась итерация 1 цикла ожидание
условие цикла (не_зелёный) выполнилось 2-й раз - истина
началась итерация 2 цикла ожидание
началась развилка по_цвету 2-й раз
условие развилки (цвет_красный) выполнилось 2-й раз - ложь
условие развилки (цвет_жёлтый) выполнилось 1-й раз - ложь
закончилась развилка по_цвету 2-й раз
закончилась итерация 2 цикла ожидание
условие цикла (не_зелёный) выполнилось 3-й раз - ложь
закончился цикл ожидание 1-й раз
закончилась программа
`;


JSON_example = {"algorithm": {"expr_values": {"не_зелёный": [true, true, false],
                                 "цвет_жёлтый": [false],
                                 "цвет_красный": [true, false]},
                 "functions": [],
                 "global_code": {"body": [{"body": {"body": [{"branches": [{"body": [{"id": 9,
                                          "name": "ждать",
                                          "type": "stmt"}],
                                      "cond": {"id": 8,
                                           "name": "цвет_красный",
                                           "type": "expr"},
                                      "id": 7,
                                      "name": "if-цвет_красный",
                                      "type": "if"},
                                     {"body": [{"id": 12,
                                          "name": "приготовиться",
                                          "type": "stmt"}],
                                      "cond": {"id": 11,
                                           "name": "цвет_жёлтый",
                                           "type": "expr"},
                                      "id": 10,
                                      "name": "elseif-цвет_жёлтый",
                                      "type": "else-if"}],
                              "id": 6,
                              "name": "по_цвету",
                              "type": "alternative"}],
                          "id": 13,
                          "name": "ожидание_loop_body",
                          "type": "sequence"},
                     "cond": {"id": 5,
                          "name": "не_зелёный",
                          "type": "expr"},
                     "id": 4,
                     "name": "ожидание",
                     "type": "while_loop"}],
                 "id": 3,
                 "name": "global_code",
                 "type": "sequence"},
         "id": 2,
         "name": "algorithm",
         "type": "algorithm"},
 "algorithm_name": "alg",
 "header_boolean_chain": [],
 "trace": [{"comment": "",
            "executes": 3,
            "id": 15,
            "n": 1,
            "name": "program", "phase": "started",
            "text_line": 13},
             {"comment": "",
            "executes": 4, "id": 17,
            "n": "1",
            "name": "ожидание", "phase": "started",
            "text_line": 15},
               {"comment": "",
              "executes": 5, "id": 18,
              "n": "1",
              "name": "(не_зелёный)", "phase": "performed",
              "text_line": 16,
              "value": true},
             {"comment": "",
            "executes": 13,
            "id": 19, "iteration_n": 1,
            "n": 1,
            "name": "ожидание_loop_body", "phase": "started",
            "text_line": 17},
             {"comment": "",
            "executes": 6, "id": 20,
            "n": "1",
            "name": "по_цвету", "phase": "started",
            "text_line": 18},
             {"comment": "",
            "executes": 8, "id": 21,
            "n": "1",
            "name": "(цвет_красный)", "phase": "performed",
            "text_line": 19,
            "value": true},
             {"comment": "",
            "executes": 7, "id": 22,
            "n": "1",
            "name": "цвет_красный", "phase": "started",
            "text_line": 20},
             {"comment": "",
            "executes": 9, "id": 23,
            "n": "1",
            "name": "ждать", "phase": "performed",
            "text_line": 21},
             {"comment": "",
            "executes": 7, "id": 24,
            "n": "1",
            "name": "цвет_красный", "phase": "finished",
            "text_line": 22},
             {"comment": "",
            "executes": 6, "id": 25,
            "n": "1",
            "name": "по_цвету", "phase": "finished",
            "text_line": 23},
             {"comment": "",
            "executes": 13,
            "id": 26, "iteration_n": 1,
            "n": 1,
            "name": "ожидание_loop_body", "phase": "finished",
            "text_line": 24},
             {"comment": "",
            "executes": 5, "id": 27,
            "n": "2",
            "name": "(не_зелёный)", "phase": "performed",
            "text_line": 25,
            "value": true},
             {"comment": "",
            "executes": 13,
            "id": 28, "iteration_n": 2,
            "n": 2,
            "name": "ожидание_loop_body", "phase": "started",
            "text_line": 26},
             {"comment": "",
            "executes": 6, "id": 29,
            "n": "2",
            "name": "по_цвету", "phase": "started",
            "text_line": 27},
             {"comment": "",
            "executes": 8, "id": 30,
            "n": "2",
            "name": "(цвет_красный)", "phase": "performed",
            "text_line": 28,
            "value": false},
             {"comment": "",
            "executes": 11, "id": 31,
            "n": "1",
            "name": "(цвет_жёлтый)", "phase": "performed",
            "text_line": 29,
            "value": false},
             {"comment": "",
            "executes": 6, "id": 32,
            "n": "2",
            "name": "по_цвету", "phase": "finished",
            "text_line": 30},
             {"comment": "",
            "executes": 13,
            "id": 33, "iteration_n": 2,
            "n": 2,
            "name": "ожидание_loop_body", "phase": "finished",
            "text_line": 31},
             {"comment": "",
            "executes": 5, "id": 34,
            "n": "3",
            "name": "(не_зелёный)", "phase": "performed",
            "text_line": 32,
            "value": false},
             {"comment": "",
            "executes": 13,
            "id": 128, "iteration_n": 3,
            "n": 3,
            "name": "ожидание_loop_body", "phase": "started",
            "text_line": 26},
             {"comment": "",
            "executes": 6, "id": 129,
            "n": "3",
            "name": "по_цвету", "phase": "started",
            "text_line": 27},
             {"comment": "",
            "executes": 8, "id": 130,
            "n": "3",
            "name": "(цвет_красный)", "phase": "performed",
            "text_line": 28,
            "value": false},
             {"comment": "",
            "executes": 11, "id": 131,
            "n": "2",
            "name": "(цвет_жёлтый)", "phase": "performed",
            "text_line": 29,
            "value": false},
             {"comment": "",
            "executes": 6, "id": 132,
            "n": "3",
            "name": "по_цвету", "phase": "finished",
            "text_line": 30},
             {"comment": "",
            "executes": 13,
            "id": 133, "iteration_n": 3,
            "n": 3,
            "name": "ожидание_loop_body", "phase": "finished",
            "text_line": 31},
             {"comment": "",
            "executes": 4, "id": 35,
            "n": "1",
            "name": "ожидание", "phase": "finished",
            "text_line": 33},
             {"comment": "",
            "executes": 3, "id": 37,
            "n": 1,
            "name": "program", "phase": "finished",
            "text_line": 35}
           ],
 "trace_name": "alg трасса "};
