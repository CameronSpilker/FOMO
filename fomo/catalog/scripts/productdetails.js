$(function(){
    
	// $.loadmodal('/homepage/index/');
	console.log($.loadmodal);


	$('#product-picture-modal').click(function(){

		console.log('hi');
		var button = $(this);
		var url = '/catalog/productdetails.modal/'+ button.attr('data-pid');

		$.loadmodal(url);

	});//click

        $('#search-button').click(function(){
        console.log('hi')
        var search = $('#search-input').val()
        console.log(search)
        var url = '/catalog/searchresults/' + search
        window.location.replace(url);
    
   // var search = $('.searchinput').val();
   // var url = '/catalog/searchresults/' + search
   // //alert('search='+search+ ' url='+url);
   //  load(url);
});//click



// 	//plugin bootstrap minus and plus
// //http://jsfiddle.net/laelitenetwork/puJ6G/
// $('.btn-number').click(function(e){
//     e.preventDefault();
    
//     fieldName = $(this).attr('data-field');
//     type      = $(this).attr('data-type');
//     var input = $("input[name='"+fieldName+"']");
//     var currentVal = parseInt(input.val());
//     if (!isNaN(currentVal)) {
//         if(type == 'minus') {
            
//             if(currentVal > input.attr('min')) {
//                 input.val(currentVal - 1).change();
//             } 
//             if(parseInt(input.val()) == input.attr('min')) {
//                 $(this).attr('disabled', true);
//             }

//         } else if(type == 'plus') {

//             if(currentVal < input.attr('max')) {
//                 input.val(currentVal + 1).change();
//             }
//             if(parseInt(input.val()) == input.attr('max')) {
//                 $(this).attr('disabled', true);
//             }

//         }
//     } else {
//         input.val(0);
//     }
// });
// $('.input-number').focusin(function(){
//    $(this).data('oldValue', $(this).val());
// });
// $('.input-number').change(function() {
    
//     minValue =  parseInt($(this).attr('min'));
//     maxValue =  parseInt($(this).attr('max'));
//     valueCurrent = parseInt($(this).val());
    
//     name = $(this).attr('name');
//     if(valueCurrent >= minValue) {
//         $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
//     } else {
//         alert('Sorry, the minimum value was reached');
//         $(this).val($(this).data('oldValue'));
//     }
//     if(valueCurrent <= maxValue) {
//         $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
//     } else {
//         alert('Sorry, the maximum value was reached');
//         $(this).val($(this).data('oldValue'));
//     }
    
    
// });
// $(".input-number").keydown(function (e) {
//         // Allow: backspace, delete, tab, escape, enter and .
//         if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
//              // Allow: Ctrl+A
//             (e.keyCode == 65 && e.ctrlKey === true) || 
//              // Allow: home, end, left, right
//             (e.keyCode >= 35 && e.keyCode <= 39)) {
//                  // let it happen, don't do anything
//                  return;
//         }
//         // Ensure that it is a number and stop the keypress
//         if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
//             e.preventDefault();
//         }
//     });




});//ready



$(function(){

  var options = {
    target: '#purchase_container',
  };

    $('#cart_form').ajaxForm(options);//ajax form


    //$('#cart_form').ajaxForm({target: '#purchase_container'});
    //Ajax Form


});//ready