$(function(){

	// $('#login-modal-form > form').ajaxForm({
	// 	target: '#jquery-loadmodal-js-body',
	// });//jquery - div above teh form div

	var images = $('.product_picture');
	images.hide();
	var current = 0;
	$(images[0]).show();


	$('#picture_button_next').click(function(){
		$(images[current]).hide();
		++current;
		if(current >= images.length) {
			current = 0;
		}//if
		$(images[current]).show();
	});//click

	$('#picture_button_previous').click(function(){

		$(images[current]).hide();
		--current;
		if(current < 0) {
			current = images.length - 1;
		}//if
		$(images[current]).show();

	});//click

});//function