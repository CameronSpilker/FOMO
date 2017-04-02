$(function() {


// pk_test_ir6aB1QiP7s8LDbK8zXWslUS Roll Key
//token.id
var handler = StripeCheckout.configure({
  key: 'pk_test_ir6aB1QiP7s8LDbK8zXWslUS',
  image: '/static/homepage/media/Logo.png',
  locale: 'auto',
  token: function(token) {
  	console.log(token);
  	$('#id_stripe_token').val(token.id)
    // You can access the token ID with `token.id`.
    // Get the token ID to your server-side code for use.
  }
});

 $('#checkout_form').submit(function(e) {
  // Open Checkout with further options:
  	if($('#id_stripe_token').val() != ''){
 		$('#checkout_form').submit();
  		return;
  	}
  handler.open({
    name: 'FOMO',
    description: '2 widgets',
    amount: "${ round((request.user.calc_total() * 100), 2) }"
  });
  e.preventDefault();
});

// Close Checkout on page navigation:
window.addEventListener('popstate', function() {
  handler.close();
});


})//ready