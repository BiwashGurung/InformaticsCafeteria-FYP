// Disabling the scrolling of the webpage when the popup is shown
function disableScroll() {
    document.body.style.overflow = 'hidden'; 
  }
  // Restoring the  scrolling when the popup is closed
  function enableScroll() {
    document.body.style.overflow = ''; 
  }
  
  function closePopup() {
    document.querySelector(".popup-main").style.display = "none";
    // Enabling the scroll of the webpage when the popup is closed
    enableScroll(); 
  }
  
  // Calling disableScroll function  when the popup is shown
  window.onload = function () {
    if (document.getElementById("popup-main")) {
      disableScroll();
    }
  };
  