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
    console.log("Navbar element:", navbar);
    var navbarHeight = navbar.offsetHeight;
    console.log("Navbar height:", navbarHeight);

    window.addEventListener('scroll', function() {
        var currentScroll = window.pageYOffset || document.documentElement.scrollTop;

        if (currentScroll > lastScrollTop && currentScroll > navbarHeight) {
            // Scrolling down
            if (!navbar.classList.contains('navbar-hidden')) {
                navbar.classList.add('navbar-hidden');
                console.log("Adding navbar-hidden class");
            }
        } else if (currentScroll < lastScrollTop) {
            // Scrolling up
            if (navbar.classList.contains('navbar-hidden')) {
                navbar.classList.remove('navbar-hidden');
                console.log("Removing navbar-hidden class");
            }
        }
        lastScrollTop = currentScroll <= 0 ? 0 : currentScroll; // Para evitar valores negativos
    });
});
