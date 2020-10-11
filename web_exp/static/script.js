
$(document).ready(function(){
	
    $("#new").click(function(){
        if ($('#alg').prop('disabled') == true)
        {
		    // Разблокировать
		    $('#alg').prop('disabled', false);
		    $('#trace').prop('disabled', false);
		    
	     //    $('#new-tip').toggleClass("active");
		    // $('#new-tip').slideToggle("slow");
		    // $('#new-tip').animate({ opacity: "show" }, 3000).animate({ opacity: "hide" }, 3000);
		    $("#new").html("New (clear both fields)")
		}
		else
		{
	        $("#alg").val("");
	        $("#trace").val("");
		}
    });
    
    $("#send").click(function(){
	    // Заблокировать
	    $('#alg').prop('disabled', true);
	    $('#trace').prop('disabled', true);
	    
	    // $('#new-tip').animate({ opacity: "hide" }, 3000);
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
        		// $('#status').html(JSON.stringify(data));
        		processing_callback(data)
        	},
        	error: function(data){
        		// alert("ajax FAIL");
        		processing_callback("fail")
        	}
        });
    });
    
    // // pass "alg" or "trace"
    // function load_field(field_name)
    $("#alg").val(load_field("alg"))
    $("#trace").val(load_field("trace"))

    
    // alert('Waw!')
    // $('#new-tip').animate({ opacity: "hide" }, 3000).animate({ opacity: "show" }, 3000);
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
		$('#status').html("Server could not send a response. Try again later ...");
		return
	}
	
	if(response.messages)
	{	
		messages = response.messages.join("\n")
		
		mistakes_count = 0
		if(response.mitakes)
			mistakes_count = response.mistakes.length
		
		$('#status').html("Server responded:\n" + messages + '\n' + mistakes_count + ` mistakes.`
			+ '\n' + JSON.stringify(response));
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

