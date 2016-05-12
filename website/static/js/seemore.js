/*author: Tao Liu and Xi Chen
Control the behavior of seemore button*/

$(document).ready(function(){
	$(".seemore").click(function(event){
		//get current category
		var parent = event.target.parentNode;
		var type = parent.firstElementChild.innerHTML;
		type = type.replace(/ /g, '').toLowerCase();
		//set href to that category and redirect
		var curElement = event.target;
		var redirectURL = "/"+type+"?page=1";
		console.log("see more");
		curElement.setAttribute("href", redirectURL);
		curElement.click();
	});
});
