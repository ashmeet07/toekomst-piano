var nav = document.querySelector("nav");

if (nav) {
  // Get the offset position of the navigation bar
  var sticky = nav.offsetTop;

  // Function to add or remove the 'sticky' class based on scroll position
  function handleScroll() {
    if (window.pageYOffset > sticky) {
      nav.classList.add("sticky");
    } else {
      nav.classList.remove("sticky");
    }
  }

  // Attach the function to the 'scroll' event
  window.onscroll = function () {
    handleScroll();
  };
} else {
  console.error("The navigation bar element was not found in the document.");
}
