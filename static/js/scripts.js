document.addEventListener("DOMContentLoaded", function () {
    console.log("Sitio cargado correctamente 🚀");

    // Ejemplo: animación de scroll suave en botones
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute("href"))
                .scrollIntoView({ behavior: "smooth" });
        });
    });
});
