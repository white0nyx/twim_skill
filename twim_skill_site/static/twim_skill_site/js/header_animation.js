var header = document.querySelector("header");
var content = document.querySelector(".contents");

var isScrolled = false;

var headerThreshold = header.clientHeight / 5;

window.addEventListener("scroll", function() {
    if (window.scrollY > 0 && window.scrollY > headerThreshold) {
        header.classList.add("scrolled");
        isScrolled = true;
    } else if (window.scrollY == 0 || window.scrollY < headerThreshold) {
        header.classList.remove("scrolled");
        isScrolled = false;
    }
});