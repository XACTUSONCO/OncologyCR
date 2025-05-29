$(document).ready(function(){
	
	$( '.responsive' ).slick( {
	  autoplay: true,
	  autoplaySpeed: 1000,
	  slidesToShow: 5,
	  slidesToScroll: 1,
	  arrows: true,
	  responsive: [
		{
		  breakpoint: 1200,
		  settings: {
			slidesToShow: 5
		  }
		},
		{
		  breakpoint: 991,
		  settings: {
			slidesToShow: 4
		  }
		},
		{
		  breakpoint: 768,
		  settings: {
			slidesToShow: 3
		  }
		},
		{
		  breakpoint: 600,
		  settings: {
			slidesToShow: 2
		  }
		},
		{
		  breakpoint: 480,
		  settings: {
			slidesToShow: 1
		  }
		}
	  ]
	} );


});
