
var cm_alg, cm_trace;
var e_alg, e_trace;

$(document).ready(function(){
	
    $("#new").click(function(){
        if (cm_alg.isReadOnly())
        {
		    // Разблокировать
		    cm_alg.setOption("readOnly", false)
		    cm_trace.setOption("readOnly", false)
		    
		    load_fields()  // reset the values to the stored at send
		    
		    $("#new").html("New (clear both fields)")
		}
		else
		{
		    e_alg.setValue("")
		    e_trace.setValue("")
		}
		
    }); 	
    
    $("#send").click(function(){
        if (cm_alg.isReadOnly())
        	// fields was not changed, so reset the values to the stored before previous send
        	load_fields()
        
	    // Заблокировать
	    cm_alg.setOption("readOnly", true)
	    cm_trace.setOption("readOnly", true)
	    
	    $("#new").html("Edit (enable fields)")
	     
	    data = {
	        alg: e_alg.getValue(),
	        trace: e_trace.getValue()
        }
        
	        
	    save_fields(data)  // alg, trace -> localStorage
	    
        $.ajax({
        	url: '/process', 
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
    
    
    cm_config = {
    	lineNumbers: true,
    	theme: "elegant"
    }
    
	cm_alg = CodeMirror.fromTextArea(document.getElementById("alg"), cm_config);
	cm_trace = CodeMirror.fromTextArea(document.getElementById("trace"), cm_config);
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
		$('#status').html("An error occured while requesting the server (it can be busy or inaccessible). Please try again.");
		return
	}
	
	if(response.messages)
	{	
		messages = response.messages.join("\n<br>")
		
		mistakes_count = 0
		if(response.mistakes)
			mistakes_count = response.mistakes.length
		
		$('#status').html("Server's response:\n" + messages + '\n<br>' + mistakes_count + ` mistakes.`
			+ '\n<br>' + JSON.stringify(response));
		
		if(response.mistakes)
		{
			// add mistakes annotation to the end of each trace lines
			line2names = {}
			for(let m of response.mistakes)
			{
				if(m["text_line"])
				{
					line = parseInt(m["text_line"])
					if(!line2names[line])
						line2names[line] = m["names"]
					else
						line2names[line] = line2names[line].concat(m["names"])
				}
			}
			
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
	}	
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

