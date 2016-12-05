$(function(){ // on dom ready

  $("#SearchForm").submit(function() {
    if ( $( "#SearchFormInput" ).val() === "Steve Jobs" ) {
    console.log('Steve Jobs Validated');
    }

      //get parent
      $.getJSON($SCRIPT_ROOT + '/buildTree', {
      thisguy: $('#SearchFormInput').val(),
      relation: "parent"
      }, function(data) {
	console.log(data.result);
	
	});

      $.getJSON($SCRIPT_ROOT + '/buildTree', {
      thisguy: $('#SearchFormInput').val(),
      relation: "child"
      }, function(data) {
	console.log(data.result);
	});

      $.getJSON($SCRIPT_ROOT + '/buildTree', {
      thisguy: $('#SearchFormInput').val(),
      relation: "spouse"
      }, function(data) {
	console.log(data.result);
	});
      
  });

});
