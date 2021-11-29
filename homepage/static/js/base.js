window.addEventListener("scroll", function() {

  let button = document.getElementById("scroll-button");
  let navbar = document.getElementById("navbar");

  if (window.pageYOffset > 0) {
    button.style.bottom = '10px';
    navbar.classList.add("sticky");
  } else {
    button.style.bottom = '-50px';
    navbar.classList.remove("sticky");
  }

});