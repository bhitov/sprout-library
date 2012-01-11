$(document).ready(function() {
	$('.borrow').click(function () {
		var id = $(this).attr('id');
		$.post("/books/"+id+"/borrowa/", function(data) {
			if (data.status==="S") {
				$('.book#' + id).html('<p class="success">' + data.message + "</p><hr />");
				//$('.book#' + id).html('<p class="success">' + data.title + " was borrowed successfully</p><hr />");
			} else if (data.status==="F") {
				alert('The book you are trying to loan was not found.');
			} else {
				alert('There was a problem with your loan. Please refresh the page and try again.');
			}
		})
		.error(function() { 
			alert('JSON error');
		});
		return false;
	});
});