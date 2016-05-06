$(document).ready(function(){
	$("#signup-modal").click(function(){
        $("#modal1").openModal();
    });

    $("#loginbutton").click(function(){
    	$("#modal1").closeModal();
    });
});