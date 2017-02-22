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
      $('#id_phone').closest('p').show()
      $('#id_cellnumber').closest('p').show()
      $('#id_email').closest('p').hide()
    }else{
      $('#id_phone').closest('p').hide()
      $('#id_cellnumber').closest('p').hide()
      $('#id_email').closest('p').show()

    }
  });
});
// var contacttype = $('#id_contacttype');
//
// console.log(contacttype);
