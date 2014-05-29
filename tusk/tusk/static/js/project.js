

// filters Tasks by iteration
$(document).ready(function(){






	$('.iterationDropdown').change(function() {


		$.ajaxSetup({ 
			beforeSend: function(xhr, settings) {
				function getCookie(name) {
					var cookieValue = null;
					if (document.cookie && document.cookie != '') {
						var cookies = document.cookie.split(';');
						for (var i = 0; i < cookies.length; i++) {
							var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                     if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     	break;
                     }
                 }
             }
             return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
 });





		var pathname = window.location.pathname;

		$.ajax({
			url: pathname + "get_tasks/",
			type: "post",
			csrfmiddlewaretoken:'{{ csrf_token }}',

			data: $(".iterationDropdownForm").serialize(),
			success: function(responseData) {
				$(".tasks").html("")
				$.each(responseData, function(key, value){
					$(".tasks").append("<p><a href =" + pathname + "task/" + value[1] + ">" + value[0] + "</a></p>")
				})
			}
		})
	});





});




/*
var clicknum = 0;
	var pathname = window.location.pathname;
	var selected = $('.iterationDropdown').val();
	$(".iterationDropdown").click(function(){
		form = $(".iterationDropdownForm")

		clicknum++;
		if(clicknum == 1){

			
			$.ajax({
				url: pathname + "get_tasks/",
				type: "post",
				data: form,
				csrfmiddlewaretoken: $(".csrf").val(),
				success: function(responseData) {
					var tasks = responseData.tasks;
					$(".tasks").html(tasks)
				}
			})

			clicknum = 0;
		}
	});*/