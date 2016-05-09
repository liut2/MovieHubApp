$(document).ready(function(){
	var totalPages = parseInt(document.getElementById("total-num").className);
	//console.log(pageCount);
	$('#pagination-demo').twbsPagination({
		startPage:1,
        totalPages: totalPages,
        visiblePages: 5,
        href: '?page={{number}}'
    });
});