$(document).ready(function() {
	$('.return').click(function () {
		var id = $(this).attr('id');
		$.post("/books/"+id+"/returna/", function(data) {
			if (data.status==="S"){
				$('.book#' + id).html('<p class="success">' + data.message + "</p><hr />");
			} else if (data.status == "NF") {
				$('#books').html('<p class="error">Book not found</p>');
			} else if (data.status == "L"){
				$('#books').html('<p class="error">That book is already marked as loaned</p>');
			} else {
				alert('view result = E');
			}
		})
		.error( function() {
			alert('noooooo');
		});
		return false;
	});
});
	