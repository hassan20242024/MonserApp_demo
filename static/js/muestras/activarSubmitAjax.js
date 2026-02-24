
    function activarSubmitAjax() {
      const form = document.getElementById("myModelForm");
      const spinner = document.getElementById("spinner-carga");
      const actionUrl = form.getAttribute("action"); // ← clave

      form.addEventListener("submit", async (e) => {
        e.preventDefault();
        spinner.classList.remove("d-none");

        const formData = new FormData(form);

        try {
          const res = await fetch(actionUrl, {
  method: "POST",
  body: new FormData(form),
  headers: { "X-Requested-With": "XMLHttpRequest" },
});

          const isJson = res.headers.get("Content-Type")?.includes("application/json");
          const data = isJson ? await res.json() : {};

          spinner.classList.add("d-none");

          if (res.status === 400) {
            if (data.message) {
              Swal.fire({
                icon: "warning",
                title: "Error de validación",
                html: `<p>${data.message}</p>`,
              });
            } else if (data.html_form) {
              document.getElementById("modalMuestraContent").innerHTML = data.html_form;
              inicializarTomSelect("#id_etapa");
              activarSubmitAjax(); // Reasignar evento
            } else {
              Swal.fire("Error", "Error de validación desconocido", "error");
            }
            return;
          }

          if (res.ok && data.success) {
            Swal.fire({
  icon: "success",
  title: "¡Éxito!",
  text: data.message,
  timer: 2500,
  timerProgressBar: true,
  showConfirmButton: false
});

            bootstrap.Modal.getInstance(document.getElementById("modalMuestra")).hide();

            // Limpiar tabla y recargar datos
            tabla.clear().draw();
            fetch('/muestras-json/')
              .then(response => response.json())
              .then(data => {
                data.data.forEach(p => {
                  tabla.row.add([
                    "",
                    p.fecha_ingreso,
                    p.nombre_muestra,
                    p.lote_muestra,
                    p.tipo_muestra,
                    p.etapa,
                    p.codigo_muestra_interno,
                    p.codigo_muestra_producto,
                    p.observaciones_muestras,
                    `<a class="btn btn-primary btn-sm" href="/duplicar_muestras/${p.pk}" title="Guardar como">
                       <i class="fa fa-clone" aria-hidden="true"></i>
                     </a>
                     <a class="btn btn-info btn-sm" href="/editar_muestras/${p.pk}" title="Editar">
                       <i class="fas fa-pencil-alt"></i>
                     </a>`
                  ]).draw(false);
                });
              })
              .catch(error => console.error('Error recargando tabla:', error));

          } else {
            Swal.fire("Error", data.message || "Error desconocido", "error");
          }
        } catch (err) {
          spinner.classList.add("d-none");
          console.error("Error en fetch:", err);
          Swal.fire("Error", err.message || "Error inesperado", "error");
        }
      });
    }

