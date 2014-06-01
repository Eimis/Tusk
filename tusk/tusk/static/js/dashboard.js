$(document).ready(function() {


// disable Submit button when submitting empty form

$('.newProjectButton').attr('disabled', 'disabled');


$('.newProject').keyup(function() {

	var empty = false;
	$('.newProject').each(function() {
		if ($(this).val().length == 0) {
			empty = true;
		}
	});

	if (empty) {
		$('.newProjectButton').attr('disabled', 'disabled');
	} else {
		$('.newProjectButton').removeAttr('disabled');
	}
});






});