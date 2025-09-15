document.addEventListener("DOMContentLoaded", function () {
    console.log("Sitio cargado correctamente 🚀");

    // Animación de scroll suave en botones
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href"))
                .scrollIntoView({ behavior: "smooth" });
        });
    });

    // Lógica para ocultar/mostrar la barra de navegación en scroll
    var lastScrollTop = 0;
    var navbar = document.querySelector('header'); // Selecciona el elemento header
    var navbarHeight = navbar.offsetHeight;

    window.addEventListener('scroll', function() {
        var currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > lastScrollTop && currentScroll > navbarHeight) {
            // Scrolling down
            navbar.classList.add('navbar-hidden');
        } else if (currentScroll < lastScrollTop) {
            // Scrolling up
            navbar.classList.remove('navbar-hidden');
        }
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // Para evitar valores negativos
    });
});
