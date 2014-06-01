

// filters Tasks by Iteration
$(document).ready(function(){



	$('.iterationDropdown').change(function() {
		$.ajaxSetup({ 
			// this script handles the csrf_token validaition when retrieving tasks by selecting iteration in dropdown
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


// disable Submit button when submitting empty form (new_story)

$('.newStoryButton').attr('disabled', 'disabled');
$('.newStory').keyup(function() {

	var empty = false;
	$('.newStory').each(function() {
		if ($(this).val().length == 0) {
			empty = true;
		}
	});

	if (empty) {
		$('.newStoryButton').attr('disabled', 'disabled');
	} else {
		$('.newStoryButton').removeAttr('disabled');
	}
});


// disable Submit button when submitting empty form (new_iteration)

$('.newIterationButton').attr('disabled', 'disabled');
$('.newIterationInput').keyup(function() {

	var empty = false;
	$('.newIterationInput').each(function() {
		if ($(this).val().length == 0) {
			empty = true;
		}
	});

	if (empty) {
		$('.newIterationButton').attr('disabled', 'disabled');
	} else {
		$('.newIterationButton').removeAttr('disabled');
	}
});



// disable Submit button when submitting empty form (new_developer)

$('.addDevButton').attr('disabled', 'disabled');
$('.addDev').keyup(function() {

	var empty = false;
	$('.addDev').each(function() {
		if ($(this).val().length == 0) {
			empty = true;
		}
	});

	if (empty) {
		$('.addDevButton').attr('disabled', 'disabled');
	} else {
		$('.addDevButton').removeAttr('disabled');
	}
});


// disable Submit button when submitting empty form (new_task)
// var hasValue = $("select option[value='---------']").attr('[selected]');


$('.newTaskButton').attr('disabled', 'disabled');
$('.newTask').keyup(function() {

	var empty = false;
	$('.newTask').each(function() {
		if ($(this).val().length == 0) {
			empty = true;
		}
	});

	if (empty) {
		$('.newTaskButton').attr('disabled', 'disabled');
	} else {
		$('.newTaskButton').removeAttr('disabled');
	}
});


}); // end




