/*author: Tao Liu and Xi Chen
Control the behavior of pagination*/

$(document).ready(function(){
	$(".page").click(function(event){
		var redirectURL;
		//get current page
		var parent = event.target.parentNode;
		var page = parent.firstElementChild.innerHTML;
		page = page.replace(/ /g, '').toLowerCase();
		// get the current category
		category = document.getElementById("search-content").className.toLowerCase();
		if (category == "search"){
			string = document.getElementById("search-content").innerText;
			redirectURL = "/search?query="+string + "&page=" + page;
		}else{ 
			redirectURL = "/"+category +"?page="+page;
		}
		//set href to that category and redirect
		var curElement = event.target;
		curElement.setAttribute("href", redirectURL);
		curElement.click();
	});
	$(".next").click(function(event){
		//get next page
		cur_page = document.getElementById("cur").innerText;
		cur_page = parseInt(cur_page) + 1;
		// get the current category
		category = document.getElementById("search-content").className.toLowerCase();
		//set href to that category and redirect
		var curElement = event.target.parentNode;
		if (category == "search"){
			// get the string that is searched
			string = document.getElementById("search-content").innerText;
			redirectURL = "/search?query="+string + "&page=" + cur_page;
		}else{ 
			redirectURL = "/"+category +"?page="+cur_page;
		}
		curElement.setAttribute("href", redirectURL);
		curElement.click();
	});
	$(".prev").click(function(event){
		//get the previous page
		cur_page = document.getElementById("cur").innerText;
		cur_page = parseInt(cur_page) - 1;
		// get the current category
		category = document.getElementById("search-content").className.toLowerCase();
		//set href to that category and redirect
		var curElement = event.target.parentNode;
		if (category == "search"){
			// get the string that is searched
			string = document.getElementById("search-content").innerText;
			redirectURL = "/search?query="+string + "&page=" + cur_page;
		}else{ 
			redirectURL = "/"+category +"?page="+cur_page;
		}
		curElement.setAttribute("href", redirectURL);
		curElement.click();
	});	
});
