$(function(){ // on dom ready

  $("#BuildTreeButton").click(function() {
    if ( $( "#SearchFormInput" ).val() === "Steve Jobs" ) {
      $.post($SCRIPT_ROOT + '/test2');
      return;
    }
    if ( $( "#SearchFormInput" ).val() === "Bill Gates" ) {
    $.post($SCRIPT_ROOT + '/test');
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
