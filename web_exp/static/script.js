
var cm_alg, cm_trace;
var e_alg, e_trace;

$(document).ready(function(){
	
    $("#new").click(function(){
        if (cm_alg.isReadOnly())
        {
		    // Разблокировать
		    set_editors_enabled(true);
		    
		    load_fields()  // reset the values to the stored at send
		    
		    $("#new").html("New (clear both fields)")
		}
		else
		{
		    e_alg.setValue("")
		    e_trace.setValue("")
		}
		
    }); 	
    
    
    $("#load-correct").click(function(){
        if (cm_alg.isReadOnly())
        {
		    alert("Cannot insert the example data now.\nPlease enable the fields first by clicking 'Edit' button.")
		}
		else
		{
		    e_alg.setValue(`while not_green  // waiting
  if color_is_red  // over_color
    wait
`);
		    e_trace.setValue(`program began  // The trace is initially correct. Modify it to introduce mistakes, and then press "Send" button
  loop waiting began 1st time
    condition of loop (not_green) evaluated 1st time - true
    iteration 1 of loop waiting began
      alternative over_color began 1st time
        condition (color_is_red) evaluated 1st time - true
        branch of condition (color_is_red) began 1st time
          wait executed 1st time
        branch of condition (color_is_red) ended 1st time
      alternative over_color ended 1st time
    iteration 1 of loop waiting ended
    condition of loop (not_green) evaluated 2nd time - true
    iteration 2 of loop waiting began
      alternative over_color began 2nd time
        condition (color_is_red) evaluated 2nd time - false
      alternative over_color ended 2nd time
    iteration 2 of loop waiting ended
    condition of loop (not_green) evaluated 3rd time - false
  loop waiting ended 1st time
program ended  // Don't know where to start? Try deleting rows other than the first and last one ones.
`)
		}
		
    }); 	
    
    $("#load-incorrect").click(function(){
        if (cm_alg.isReadOnly())
        {
		    alert("Cannot insert the example data now.\nPlease enable the fields first by clicking 'Edit' button.")
		}
		else
		{
		    e_alg.setValue(`while not_green  // waiting
  if color_is_red  // over_color
    wait
`);
		    e_trace.setValue(`program began
  loop waiting began 1st time
    condition of loop (not_green) evaluated 1st time - true
    iteration 1 of loop waiting began
      alternative over_color began 1st time
        condition (color_is_red) evaluated 1st time - false
        branch of condition (color_is_red) began 1st time
          wait executed 1st time
        branch of condition (color_is_red) ended 1st time
      alternative over_color ended 1st time
    iteration 1 of loop waiting ended
    condition of loop (not_green) evaluated 2nd time - true
  loop waiting ended 1st time
program ended`)
		}
		// e_trace.addLineClass(3, "background", "error-line")
    }); 	
    
    
    $("#send_text").on("click", function() {
        if (cm_alg.isReadOnly())
        	// fields was not changed, so reset the values to the stored before previous send
        	load_fields()
        
	    // Заблокировать
	    set_editors_enabled(false);
	    
	    $("#new").html("Edit (enable fields)")
	     
	    let data = {
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
	    let data = JSON_example;

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
    
    
    define_syntax_mode();
    
    let cm_config = {
    	lineNumbers: true,
    	theme: "elegant"
    }
    
	cm_alg = CodeMirror.fromTextArea(document.getElementById("alg"), cm_config);
	cm_trace = CodeMirror.fromTextArea(document.getElementById("trace"), cm_config);
	cm_alg.setSize("70%", "20%");
	cm_trace.setSize("70%", "35%");
	e_alg = cm_alg.getDoc();
	e_trace = cm_trace.getDoc();
	
	
    load_fields()  // read text stored at localStorage
});


function processing_callback(response="wait")
{
	if(response == "wait")
	{
		$('#status').html("Please wait ...");
		return
	}
	
	if(response == "fail")
	{
		$('#status').html("An error occurred while requesting the server (it can fail with the request, be busy or inaccessible). Please try again.<br>(Note that current environment is in debugging mode so can be slow and hang on concurrent requests.)");
		return
	}
	
	if(response.messages)
	{	
		let mistakes_count = 0;
		if(response.mistakes)
			mistakes_count = response.mistakes.length
		
		let explanations = [];
		
		if(response.mistakes)
		{
			// add mistakes annotation to the end of each trace lines
			let line2names = {};
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
						explanations.push([line, "Line <b>" + line + "</b>: " + m["explanation"]])
					}
				}
			}
			
			explanations.sort(function compare(a, b) {return a[0] - b[0]})
			explanations = explanations.map( function(a) {return a[1]} )
			
			let lines = load_field("trace").split('\n')
			for(let key in line2names)
			{
        const i = parseInt(key);
				if(1 <= i && i <= lines.length)
				{
					let names = [...new Set(line2names[i])]
					names.sort()
					const addition = '  // error: ' + names.join(', ')
					if(! lines[i-1].endsWith(addition))
						lines[i-1] += addition
				}
				else
					console.warn({i, lines_length: lines.length})
			}
			var text = lines.join("\n")
			e_trace.setValue(text)
		}
		
		const messages = (response.messages.concat(explanations)).join("\n<br>")
		
		$('#status').html("Server's response:\n" + messages + '\n<br>' 
			+ mistakes_count + ` mistakes (in internal representation).`
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
	const str = localStorage.algtrace
  if (!str) {
    return ''
  }

	let data = JSON.parse( str );
	return data[field_name]
}



////////// CM : Custom syntax //////////


function define_syntax_mode() {

	const keyword_re = /(?:начался|началась|началось|began|закончился|закончилась|закончилось|ended|выполнился|выполнилась|выполнилось|executed|evaluated|calculated|если|иначе|делать|пока|для|от|до|шаг|с\s+шагом|if|else|do|while|for|from|to|with\s+step|step|каждого|в|из|по|к|foreach|each|in)(?:\s|$)/i
	
	const struct_re = /развилка|развилки|альтернативная|ветка|branch|alternative|условия|переход|update|итерация|iteration|иначe|условие|цикла|condition|of|loop|инициализация|init|initialization|цикл|следование|sequence/i
	
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


const JSON_example = {"algorithm": {"expr_values": {"не_зелёный": [true, true, false],
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
