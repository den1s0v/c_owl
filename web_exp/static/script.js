
$(document).ready(function(){
	
    $("#new").click(function(){
        if ($('#alg').prop('disabled') == true)
        {
		    // Разблокировать
		    $('#alg').prop('disabled', false);
		    $('#trace').prop('disabled', false);
		    
	     //    $('#new-tip').toggleClass("active");
		    // $('#new-tip').slideToggle("slow");
		    $('#new-tip').animate({ opacity: "show" }, 3000).animate({ opacity: "hide" }, 3000);
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
	    
	    $('#new-tip').animate({ opacity: "hide" }, 3000);
	     
	    data = {
	            alg: $("#alg").val(),
	            trace: $("#trace").val()
	        }
	        
        $.ajax({
        	url: '/process', 
        	method: 'post',
        	dataType: 'json',
        	data: data,
        	success: function(data){
        		alert("ajax OK");
        		$('#status').html(JSON.stringify(data));
        	},
        	error: function(data){
        		alert("ajax FAIL");
        	}
        });
    });
    
    // alert('Waw!')
    $('#new-tip').animate({ opacity: "hide" }, 3000).animate({ opacity: "show" }, 3000);
});
