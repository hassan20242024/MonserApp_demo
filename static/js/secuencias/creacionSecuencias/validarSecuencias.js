// Escuchar cambios en los checkboxes
document.addEventListener('change', function (e) {
  if (e.target.classList.contains('checkbox-revisar')) {
    actualizarBotonRevisar();
  }
});

document.getElementById('btnCambiarRevisadas').addEventListener('click', async () => {
  const ids = Array.from(document.querySelectorAll('.checkbox-revisar:checked'))
    .map(cb => cb.dataset.id);
  if (ids.length === 0) {
    Swal.fire('Selecciona al menos una fila', '', 'info');
    return;
  }

  const confirmacion = await Swal.fire({
    title: '¿Estás seguro?',
    text: `Cambiarás ${ids.length} muestra(s) a estado "Revisada".`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, confirmar',
    cancelButtonText: 'Cancelar'
  });

  if (!confirmacion.isConfirmed) return;
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
    const res = await fetch('/cambiar_estado_revisar/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // Usa tu función para obtener el CSRF token
      },
      body: JSON.stringify({ ids: ids }),
    });

    const data = await res.json();

    if (data.success) {
  Swal.fire({
    icon: 'success',
    title: '¡Éxito!',
    text: data.message || 'Estado actualizado.',
    timer: 2000,
    showConfirmButton: false,
  });
  // Quitar filas afectadas sin recargar toda la tabla
  ids.forEach(id => {
    const fila = document.querySelector(`.select-item[data-id="${id}"]`)?.closest('tr');
    if (fila) fila.remove();
  });

} else {
  throw new Error(data.error || 'No se pudo cambiar el estado');
}

  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message,
    });
  }
});
