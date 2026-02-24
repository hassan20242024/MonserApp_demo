document.getElementById('btnCambiarRegistrada').addEventListener('click', async () => {
  const checkboxes = Array.from(document.querySelectorAll('.checkbox-revisar:checked'));
  if (checkboxes.length === 0) {
    Swal.fire('Selecciona al menos una fila', '', 'info');
    return;
  }

  const secuencias = checkboxes.map(cb => ({
    id: cb.dataset.id,
    tipo: cb.dataset.tipo
  }));

  const confirmacion = await Swal.fire({
    title: '¿Estás seguro?',
    text: `Cambiarás ${secuencias.length} secuencia(s) a estado "Registrada".`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Sí, confirmar',
    cancelButtonText: 'Cancelar'
  });

  if (!confirmacion.isConfirmed) return;

  Swal.fire({
    title: 'Actualizando...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
    const res = await fetch('/retornar_estado_registrada/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({ secuencias })
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

      secuencias.forEach(item => {
        const fila = document.querySelector(`.checkbox-revisar[data-id="${item.id}"]`)?.closest('tr');
        if (fila) fila.remove();
      });
    } else {
      throw new Error(data.message || 'Error en el servidor');
    }

  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: error.message,
    });
  }
});
