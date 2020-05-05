function finishPreload() {
  gsap.to(".preloader-main", {
    opacity: 0,
    display: "none",
    duration: .4
  })
}


var x = window.matchMedia("(max-width: 600px)")

function openNav() {

  /* Set the width of the side navigation to 400px */

  if (x.matches) {
    document.getElementById("side-menu").style.width = "100%";
    document.getElementById("menu-items").style.width = "100%";
    document.getElementById("menu-items").style.display = "flex";
    document.getElementById("closebtn").style.display = "flex";
  } else {
    document.getElementById("side-menu").style.width = "400px";
    document.getElementById("menu-items").style.width = "400px";
    gsap.to("#side-menu-overlay", {
      opacity: 1,
      duration: .4,
      display: "block"
    });
    document.getElementById("menu-items").style.display = "flex";
    document.getElementById("closebtn").style.display = "flex";
  }

}

/* Set the width of the side navigation to 0 */
function closeNav() {
  document.getElementById("side-menu").style.width = "0";
  document.getElementById("menu-items").style.width = "0";
  gsap.to("#side-menu-overlay", {
    opacity: 0,
    duration: .4,
    display: "none"
  });
  document.getElementById("menu-items").style.display = "none";
  document.getElementById("closebtn").style.display = "none";
}