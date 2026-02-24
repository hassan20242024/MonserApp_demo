document.getElementById('btnMarcarInvalida').addEventListener('click', async () => {
  const seleccionados = [...document.querySelectorAll('.select-item:checked')].map(cb => cb.dataset.id);

  if (seleccionados.length === 0) {
    Swal.fire('Selecciona al menos una fila', '', 'info');
    return;
  }

  // Opciones de causa (solo texto legible)
  const causasOptions = [
    "Problemas de equipo (Equipo presionado, Línea base defectuosa)",
    "Problemas de equipo (Otros: Caídas de presión, Picos fantasmas; Problemas de software/hardware...)",
    "Problemas de columna",
    "Incumplimiento de System (RSD)",
    "Incumplimiento de System (Otros: Resolución, Asimetría, Platos teóricos, Señal ruido)",
    "Incumplimiento de System (Correlación)",
    "Problemas de Fases Móviles (TR Corridos, FM saturada, Otros...)",
    "Problemas de red",
    "Fallas de Fluido Eléctrico",
    "Otros (definir en observaciones)"
  ];

  const html = causasOptions.map((text, idx) => `
    <div class="form-check text-start mb-1">
      <input class="form-check-input causa-radio" type="radio" name="causa" id="causa${idx}" value="${text}">
      <label class="form-check-label" for="causa${idx}">${text}</label>
    </div>
  `).join('');

  const { value: causaSeleccionada } = await Swal.fire({
    title: 'Selecciona una causa de invalidez',
    html: `<form id="formCausas">${html}</form>`,
    showCancelButton: true,
    confirmButtonText: 'Continuar',
    preConfirm: () => {
      const seleccion = document.querySelector('.causa-radio:checked');
      if (!seleccion) {
        Swal.showValidationMessage('Debes seleccionar una causa');
        return false;
      }
      return seleccion.value;
    }
  });

  if (!causaSeleccionada) return;

  // Confirmación final
  const confirmar = await Swal.fire({
    title: '¿Estás seguro?',
    text: `Se marcarán ${seleccionados.length} fila(s) como inválidas por: "${causaSeleccionada}"`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, continuar',
    cancelButtonText: 'Cancelar'
  });

  if (!confirmar.isConfirmed) return;

  // Enviar al backend
  const csrftoken = getCookie('csrftoken');
  Swal.fire({
  title: 'Actualizando...',
  allowOutsideClick: false,
  didOpen: () => {
    Swal.showLoading();
  }
});
  try {
    const res = await fetch('/cambiar_estado_invalida/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({ ids: seleccionados, causa: causaSeleccionada })
    });

    const data = await res.json();

    if (data.success) {
      Swal.fire({
        icon: 'success',
        title: 'Actualizado correctamente',
        showConfirmButton: false,
        timer: 2000 // se cierra solo
      });
      getDataAndRender();
    } else {
      Swal.fire('Error al actualizar', data.error || '', 'error');
    }

  } catch (error) {
    Swal.fire('Error', 'No se pudo conectar con el servidor.', 'error');
  }
}
);
