// jQuery(); == $();
//Late execution
//DOM selectors
//Event handler on elements
//

$(function(){

  var producttype = $('#id_producttype')

  producttype.change(function(){
    var value = producttype.val()
    if(value == 'bulk'){
      $('.producttype-bulk').closest('p').show()
      $('.producttype-not').closest('p').hide()
    }else{
      $('.producttype-bulk').closest('p').hide()
      $('.producttype-not').closest('p').show()

    }
  });
  producttype.change();
});
// var contacttype = $('#id_contacttype');
//
// console.log(contacttype);
