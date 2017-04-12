$(function(){

	$('#login-modal-button').click(function(){

		$.loadmodal('/account/login.modal/');

	});//click

	html = "<div class='container-fluid'>" +
           " <div class='row'>" +
                "<div class='col-lg-12'>" +
                    "<div class='intro-message'>" +
                        "<h1>Family Oriented Music Organization</h1>" +
                        "<h3>A Place For Family & Music</h3>" +
                        "<hr class='intro-divider'>" + 
                        "<ul class='list-inline intro-social-buttons'>" +
                            "<li>" +
                                "<a href='/catalog/index/' class='btn btn-default btn-lg'><i class='fa fa-shopping-cart' aria-hidden='true'></i> <span class='network-name'>Buy</span></a>" +
                            "</li>" +
                            "<li>"  +
                                "<a href='/catalog/index/' class='btn btn-default btn-lg'><i class='fa fa-music' aria-hidden='true'></i> <span class='network-name'>Rent</span></a>" +
                            "</li>" +
                            "<li>" +
                                "<a href='/homepage/about/' class='btn btn-default btn-lg'><i class='fa fa-child' aria-hidden='true'></i> <span class='network-name'>Learn</span></a>" +
                            "</li>" +
                        "</ul>" +
                    "</div>" +
                "</div>" +
            "</div>" +
        "</div>" 
	$('#load-pic').hide().append(html).fadeIn(2000);
	    


});//ready