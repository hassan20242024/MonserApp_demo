
// 🔧 Función para obtener cookies por nombre
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Comprueba si esta cookie comienza con el nombre buscado
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener('DOMContentLoaded', getDataAndRender);

// Botón guardar del modal
document.getElementById('btnGuardarCambios').addEventListener('click', async () => {
    const statusActual = document.getElementById('modalStatus').dataset.status;
  if (statusActual === 'Auditada') {
    Swal.fire({
      icon: 'warning',
      title: 'Edición no permitida',
      text: 'No se pueden guardar cambios en una secuencia auditada.',
    });
    return;
  }

  const id = currentEditingId;
  const newStatus = document.getElementById('modalStatus').textContent.trim();
  const newObservaciones = document.getElementById('modalObservaciones').value.trim();
  const newNombre = document.getElementById('modalNombreInput').value.trim();
const newSistema = document.getElementById('modalSistemaInput').value; // ya es un ID
   // 🚫 Validar campos obligatorios
  if (!newNombre || !newSistema) {
    Swal.fire({
      icon: 'warning',
      title: 'Campos obligatorios',
      text: 'Los campos "Nombre" y "Sistema" no pueden estar vacíos.',
    });
    return;
  }
   Swal.fire({
    title: 'Guardando cambios...',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  try {
    const res = await fetch(`/api/secuencias/${id}/actualizar/`, {
      
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: JSON.stringify({
        status: newStatus,
        observaciones: newObservaciones,
        nombre: newNombre,
        sistema: newSistema
      }),
    });

    const data = await res.json();

    if (data.success) {
      Swal.fire({
        icon: 'success',
        title: 'Cambios guardados',
        timer: 1500,
        showConfirmButton: false,
      });

      // Actualizar la tabla para reflejar el cambio en status
      getDataAndRender();

      // Cerrar modal
      const modalInstance = bootstrap.Modal.getInstance(document.getElementById('detalleModal'));
      
document.activeElement.blur(); 


      modalInstance.hide();
    } else {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: data.error || 'No se pudo guardar el cambio',
      });
    }
  } catch (err) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Error en la comunicación con el servidor',
    });
  }
})
