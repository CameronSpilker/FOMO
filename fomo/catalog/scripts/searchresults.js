$(function(){

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



});//ready function