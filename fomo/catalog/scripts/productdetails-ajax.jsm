$(function(){

	$('#cart_count_span').html("${ request.user.get_cart_count() }");

	  var options = {
    target: '#purchase_container',

  };
	$('#cart_form').ajaxForm(options);







  if ($(".errorlist")[0])
  {
      $('#added_to_cart').hide()

      
  } 
    else 
    {

    $('#purchase_container1').hide()
  


  }

});//function