$(function(){

  $('.delete_link2').click(function(event) {
    //cancel the default behavior
    event.preventDefault();

    //open the modal
    $('#myModal2').modal({
        //no options

    });


    var href = $(this).attr('href');
    $('#really-delete-link2').attr('href', href)
    console.log(href);

  });//onclick




});//ready
