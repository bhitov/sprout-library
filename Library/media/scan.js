$(document).ready(function() {
	$('button').click(function () {
		var barcode = $('input#id_barcode').val();
		$.post('/books/scana/', { "barcode": barcode }, function(data) {
			if (data.status === "S"){
				$('#books').html('<p class="success">' + data.message + "</p>");
			} else if (data.result == "NF") {
				$('#books').html('<p class="error">Book not found</p>');
			} else if (data.result == "L"){
				$('#books').html('<p class="error">That book is already marked as loaned</p>');
			} else {
				alert('view result = EE');
			}
		}).error( function() {
			alert('noooooo');
		});
		return false;
	});
});