$(function(){ // on dom ready

  $("#SearchForm").submit(function() {
    if ( $( "#SearchFormInput" ).val() === "Steve Jobs" ) {
    console.log('Steve Jobs Validated');
    }
    $.when(
      //get parent
      $.getJSON($SCRIPT_ROOT + '/buildTree', {
      thisguy: $('#SearchFormInput').val(),
      relation: "parent"
      }),

      $.getJSON($SCRIPT_ROOT + '/buildTree', {
      thisguy: $('#SearchFormInput').val(),
      relation: "child"
      }),

      $.getJSON($SCRIPT_ROOT + '/buildTree', {
      thisguy: $('#SearchFormInput').val(),
      relation: "spouse"
      })

    ).then(function(parent, child, spouse) {
      console.log(parent);
      console.log(child);
      console.log(spouse);
    });
      
  });

});