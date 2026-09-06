document.addEventListener("DOMContentLoaded", function () {
    // Scroll suave para anclas internas
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener("click", function (e) {
            var targetId = this.getAttribute("href");
            if (!targetId || targetId === "#") return;
            var target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // Ocultar / mostrar navbar al hacer scroll
    var lastScrollTop = 0;
    var navbar = document.querySelector("header");
    if (!navbar) return;

    var navbarHeight = navbar.offsetHeight || 80;
    var scrollUpThreshold = 80;

    window.addEventListener("scroll", function () {
        var currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > lastScrollTop && currentScroll > navbarHeight) {
            navbar.classList.add("navbar-hidden");
        } else if (
            currentScroll < lastScrollTop &&
            (currentScroll < lastScrollTop - scrollUpThreshold || currentScroll <= 0)
        ) {
            navbar.classList.remove("navbar-hidden");
        }

        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll;
    });
});
