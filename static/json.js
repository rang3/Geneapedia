$(function(){ // on dom ready

  $("#BuildTreeButton").click(function() {
    if ( $( "#SearchFormInput" ).val() === "Steve Jobs" ) {
    console.log('Steve Jobs Validated');
    return;
    }
    if ( $( "#SearchFormInput" ).val() === "Bill Gates" ) {
    console.log('Bill Gates Validated');
    return;
    }
    if ( $( "#SearchFormInput" ).val() === "Elon Musk" ) {
    console.log('Elon Musk Validated');
    return;
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
