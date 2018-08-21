$(document).ready(function() {

  // get year for footer
  var thisYear = new Date();
      thisYear = thisYear.getFullYear();
  $('.current-year').html(thisYear);

  $(".preloader").fadeOut();
});
