
$(document).ready(function() {
	var oTable = $('#filesTable').dataTable( {
		"bJQueryUI": true,
		"aaSorting": [[ 1, "desc" ]]
	}
	);

	$('#filesTable').css('background-color','black');

	

	$('#banner').click(function() {
		window.location.href = '/';
	});


	$('#baseDirectoryButton').click(function(){
		window.location = "/files/";
	});

    $('#upButton').click(function(){
		parent.history.back();
	});    

} );

