  $(document).ready(function() {
	  var book_skel = $('#dummy').clone();
	  $('#dummy').hide();
	  $('#debug').append('<p>test</p>');
	  $('button').click(function () {
		  $('#books').html('');
		  $('#debug').append('<p>pass1</p>');
	      var barcode = $('input#id_barcode').val();
	      $('#debug').append('<p>barcode: ' + barcode + '</p>');
			$.post('/books/searcha/', { "barcode": ""+barcode }, function(data) {
				$('#debug').append('<p>pass2</p>');
				var book_html = book_skel.clone();
				var image_link = data.book_list[0].image_link;
				var author = data.book_list[0].author;
				var title = data.book_list[0].title;
				//alert(title);
				
				book_html.find('.image_link').attr('src', image_link);
				book_html.find('.title').html('Title: ' + title);
				book_html.find('.author').html('Author: ' + author);
				
				//var image_link = data.books[0].image_link;
				//var author = data.books[0].author;
				//var title = data.books[0].title;
				//var barc =  data.books[0].barcode;
								
				book_html.find('input#image_link').val(image_link);
				book_html.find('input#author').val(author);
				book_html.find('input#title').val(title);
				book_html.find('input#barcode').val(barcode);
				book_html.find('button#sub').click( function() {
					$('#debug').append('<p>click bind</p>');
					$.post('/books/createa/', {'image_link' : image_link,
						'author' : author, 'title' : title,
						'barcode' : barcode}, function(data) {
							if (data.result == 'S') {
								$('#book_list').html('<p class="success">' + title + " added</p>");
							} else {
								alert('ajax create error');
							}
						}).error( function(){
							alert('ajax create response error');
						});
					return false;
				});
				//alert(book_html.find('.title').html());
				//alert("I should work");
				book_html.show();
				$('#book_list').append(book_html);
			})
			.error( function() {
				alert('error');
			});
			return false
		});
      });