
$(document).ready(function(){
	
    $("#new").click(function(){
        if ($('#alg').prop('disabled') == true)
        {
		    // Разблокировать
		    $('#alg').prop('disabled', false);
		    $('#trace').prop('disabled', false);
		    
		    load_fields()  // reset the values to the stored at send
		    
		    $("#new").html("New (clear both fields)")
		}
		else
		{
	        $("#alg").val("");
	        $("#trace").val("");
		}
    });
    
    $("#send").click(function(){
        if ($('#alg').prop('disabled') == true)
        	// fields was not changed, so reset the values to the stored before previous send
        	load_fields()
        
	    // Заблокировать
	    $('#alg').prop('disabled', true);
	    $('#trace').prop('disabled', true);
	    
	    $("#new").html("Edit (enable fields)")
	     
	    data = {
            alg: $("#alg").val(),
            trace: $("#trace").val()
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
        		// alert("ajax OK");
        		processing_callback(data)
        	},
        	error: function(data){
        		// alert("ajax FAIL");
        		processing_callback("fail")
        	}
        });
    });
    
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
			$("#trace").val(lines.join("\n"))
		}
	}	
}


////// local storage //////

function save_fields(data=null)
{
	if(data === null)
	{
		data = {
			alg: $("#alg").val(),
			trace: $("#trace").val()
		}
	}
	
	localStorage.algtrace = JSON.stringify(data);
}

function load_fields()
{
    $("#alg").val(load_field("alg"))
    $("#trace").val(load_field("trace"))
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

