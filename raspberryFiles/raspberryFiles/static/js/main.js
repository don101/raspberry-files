
$(document).ready(function() {
	var oTable = $('#filesTable').dataTable({
		"bJQueryUI": true,
		"bPaginate": false,
		"bLengthChange": false,
		"bInfo": false
	}

	);



	$('#uploadDownload').hide();
	

	$('#banner').click(function() {
		window.location.href = '/';
	});


	$('#baseDirectoryButton').click(function(){
		window.location = "/files/";
	});

	$('#upButton').click(function(){
    	//alert(document.location.href);
    	document.location.href = '..'; 
    });  


	$("#addFilesButton").click(function () {
		$("#uploadDownload").slideToggle();
	});  



} );

