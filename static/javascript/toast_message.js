// Loading the toast notification when the page is loaded
  $(document).ready(function () {
    // Checking if there are messages inside the toast-body
    if ($(".toast-body").text().trim().length > 0) {
      $("#toast-container").show(); 
      $('.toast').toast('show'); 

      // Auto-dismissing the toast after 5 seconds
      setTimeout(function () {
        $('.toast').toast('hide');
      }, 5000);
    }

    //Creating a manual close button functionality
    $(".close").on("click", function () {
      $("#toast-container").hide();
    });
  });
