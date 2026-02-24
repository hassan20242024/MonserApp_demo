
  document.addEventListener("click", function(e) {
  const editarBtn = e.target.closest("a[href^='/editar_muestras/']");
  if (editarBtn) {
    e.preventDefault();
    const url = editarBtn.getAttribute("href");

    Swal.fire({
      title: 'Cargando...',
      allowOutsideClick: false,
      didOpen: () => Swal.showLoading()
    });

    fetch(url)
      .then(response => response.json())
      .then(data => {
        Swal.close();
        document.getElementById("modalMuestraContent").innerHTML = data.html_form;

        // Re-activar elementos dinámicos
        inicializarTomSelect("#id_etapa");
        new bootstrap.Modal(document.getElementById("modalMuestra")).show();
        activarSubmitAjax();  // reutiliza tu lógica para manejar el submit
      })
      .catch(error => {
        console.error("Error al cargar edición:", error);
        Swal.fire("Error", "No se pudo cargar el formulario de edición", "error");
      });
  }
});
