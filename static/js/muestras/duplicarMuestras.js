
  document.addEventListener("click", function(e) {
    const duplicarBtn = e.target.closest("a[href^='/duplicar_muestras/']");
    if (duplicarBtn) {
      e.preventDefault();
      const url = duplicarBtn.getAttribute("href");

      Swal.fire({
        title: 'Cargando formulario...',
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading()
      });

      fetch(url)
        .then(response => response.json())
        .then(data => {
          Swal.close();
          document.getElementById("modalMuestraContent").innerHTML = data.html_form;

          inicializarTomSelect("#id_etapa");

          // Forzar que el formulario vaya a ingresar_muestras (no a editar)
          const form = document.querySelector("#myModelForm");
          if (form) {
            form.setAttribute("action", "/ingresar_muestras/");
          }

          new bootstrap.Modal(document.getElementById("modalMuestra")).show();
          activarSubmitAjax();  // Reutiliza tu lógica de guardado
        })
        .catch(error => {
          console.error("Error al cargar duplicación:", error);
          Swal.fire("Error", "No se pudo cargar el formulario para duplicar", "error");
        });
    }
  });
