/*global $ */

$( window ).load(function() {
 
  
  $.getJSON('/profiles', function(data) {
  alert(data);
});
});


 

