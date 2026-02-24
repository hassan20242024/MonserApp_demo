
document.addEventListener('DOMContentLoaded', () => {

  const lavadoModal = new bootstrap.Modal(document.getElementById('lavadoModal'));
  const lavadoForm = document.getElementById('lavadoForm');
  const alerta = document.getElementById('alertaResultado');
  document.getElementById('btnCrearLavado').addEventListener('click', () => {
    lavadoForm.reset();
    lavadoForm.removeAttribute('data-id');
    alerta.classList.add('d-none');
    alerta.innerText = '';
  });

  lavadoForm.addEventListener('submit', function(e) {
    e.preventDefault();
    alerta.classList.add('d-none');
    alerta.innerText = '';

    const isEdit = lavadoForm.hasAttribute('data-id');
    const data = Object.fromEntries(new FormData(lavadoForm));
    const newSistemaText = lavadoForm.sistema.selectedOptions[0]?.text.trim().toLowerCase();
    function stripHtml(html) {
  const tmp = document.createElement("div");
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || "";
}

const existingSystems = table.column(0).data().toArray()
  .map(v => stripHtml(v).trim().toLowerCase());

    if (isEdit) {
      const old = lavadoForm.sistema.getAttribute('data-old-text');
      if (old) {
        const idx = existingSystems.indexOf(old.trim().toLowerCase());
        if (idx >= 0) existingSystems.splice(idx, 1);
      }
    }

    if (existingSystems.includes(newSistemaText)) {
      Swal.fire('Error', 'El sistema ya existe en la tabla.', 'error');
      return;
    }

    // Confirmación previa al envío
     Swal.fire({
        title: "¿Está seguro?",
        text: "Desea guardar los cambios?",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Confirmar"
    }).then(result => {
      if (!result.isConfirmed) return;

      // Alerta de carga durante el envío
      Swal.fire({
        title: 'Guardando...',
        html: 'Por favor espera.',
        allowOutsideClick: false,
        allowEscapeKey: false,
        showConfirmButton: false,
        didOpen: () => Swal.showLoading()
      });

      const id = lavadoForm.getAttribute('data-id');
      const url = isEdit ? `/ruta-api-editar/${id}/` : "/lavado/ajax/";
      const method = isEdit ? 'PUT' : 'POST';

      fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(data)
      })
      .then(res => res.json().then(json => ({ ok: res.ok, json })))
      .then(({ ok, json }) => {
        Swal.close(); // Cierra la alerta de carga

        if (!ok || json.error) {
          Swal.fire('Error', json.error || 'Error inesperado', 'error');
        } else {
          Swal.fire({
            icon: 'success',
            title: '¡Éxito!',
            text: json.message,
            timer: 1500,
            timerProgressBar: true,
            showConfirmButton: false
          });
          lavadoForm.reset();
          lavadoForm.removeAttribute('data-id');
          lavadoModal.hide();
          table.ajax.reload(null, false);
        }
      })
      .catch(err => {
        console.error(err);
        Swal.close();
        Swal.fire('Error', 'Error de red', 'error');
      });
    });
  });

  window.editarRegistro = function(id) {
    alerta.classList.add('d-none');
    alerta.innerText = '';
    fetch(`/ruta-api-detalle/${id}/`)
      .then(res => res.json())
      .then(data => {
        lavadoForm.setAttribute('data-id', id);
        lavadoForm.sistema.value = data.sistema;
        lavadoForm.sistema.setAttribute('data-old-text',
          lavadoForm.sistema.options[lavadoForm.sistema.selectedIndex].text);
        lavadoForm.fecha_lavado_buzo.value = data.fecha_lavado_buzo || '';
        lavadoForm.fecha_lavado_celda.value = data.fecha_lavado_celda || '';
        lavadoForm.fecha_test_diagnostico.value = data.fecha_test_diagnostico || '';
        lavadoForm.fecha_mantenimiento.value = data.fecha_mantenimiento || '';
        lavadoForm.fecha_calificacion.value = data.fecha_calificacion || '';
        lavadoForm.observaciones.value = data.observaciones || '';
        lavadoModal.show();
      })
      .catch(err => console.error("Error al cargar datos:", err));
  };
});
