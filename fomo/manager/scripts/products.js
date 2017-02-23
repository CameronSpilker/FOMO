$(function(){

  $('.delete_link').click(function(event) {
    //cancel the default behavior
    event.preventDefault();

    //open the modal
    $('#myModal').modal({
        //no options

    });


    var href = $(this).attr('href');
    $('#really-delete-link').attr('href', href)
    console.log(href);

  });//onclick


  $('.update_quantity_button').click(function(){
    var button = $(this);
    var url = '/manager/products.get_quantity/' + button.attr('data-pid');

    //call ajax
    // $.ajax()
    //up button.closest("")
    //down button.find("")
    //sibling button.siblings("")
    button.siblings('.quantity_text').load(url);


  });


});//ready
