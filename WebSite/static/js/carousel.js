$(document).ready(function(){
    //manage carousel
    $('#toprated, #lastyear, #recent, #locked').carousel({
    	dist: -30
    });
	$('#toprated').carousel('next');
	$('#toprated').carousel('next', [3]); // Move next n times.
	$('#toprated').carousel('prev');
	$('#toprated').carousel('prev', [4]); // Move prev n times.

	$('#lastyear').carousel('next');
	$('#lastyear').carousel('next', [3]); // Move next n times.
	$('#lastyear').carousel('prev');
	$('#lastyear').carousel('prev', [4]); // Move prev n times.

	$('#recent').carousel('next');
	$('#recent').carousel('next', [3]); // Move next n times.
	$('#recent').carousel('prev');
	$('#recent').carousel('prev', [4]); // Move prev n times.
});
