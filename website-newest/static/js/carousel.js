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

});
