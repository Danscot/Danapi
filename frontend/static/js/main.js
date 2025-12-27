const burger = document.getElementById("burger");
const nav = document.getElementById("navLinks");

// Toggle menu
burger.addEventListener("click", () => {
  burger.classList.toggle("open");
  nav.classList.toggle("show");
});

// Close menu when link is clicked (mobile UX)
document.querySelectorAll("#navLinks a").forEach(link => {
  link.addEventListener("click", () => {
    burger.classList.remove("open");
    nav.classList.remove("show");
  });
});
