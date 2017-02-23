// jQuery(); == $();
//Late execution
//DOM selectors
//Event handler on elements
//

$(function(){

  var contacttype = $('#id_contacttype')

  contacttype.change(function(){
    var value = contacttype.val()
    if(value == 'phone'){
      $('.contacttype-phone').closest('p').show()
      $('.contacttype-email').closest('p').hide()
    }else{
      $('.contacttype-phone').closest('p').hide()
      $('.contacttype-email').closest('p').show()

    }
  });
  contacttype.change();
});
// var contacttype = $('#id_contacttype');
//
// console.log(contacttype);
