$(document).ready(function(){
    //manage carousel
    genres = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
    genre_str = ""
    for (var i = 0; i < genres.length; i++){
    	genre_str += "#"+genres[i]+","
    }
    genre_str = genre_str.substring(0, genre_str.length - 1)
    console.log(genre_str)
    $('#toprated, #lastyear, #recent, #locked,' + genre_str).carousel({
    	dist: -20
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

	genres = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	/*for (genre : genres){
		$("#"+genre).carousel({
			dist: -30
		});
		$('#'+genre).carousel('next');
		$('#'+genre).carousel('next', [3]); // Move next n times.
		$('#'+genre).carousel('prev');
		$('#'+genre).carousel('prev', [4]); // Move prev n times.
	}*/
});
