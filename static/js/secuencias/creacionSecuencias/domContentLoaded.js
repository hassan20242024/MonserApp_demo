  
document.addEventListener('DOMContentLoaded', () => {
 const userDataEl = document.getElementById('user-data') || document.body;
  const USER_ROLE = userDataEl.dataset.userRole;

  console.log("Rol del usuario:", USER_ROLE);
  // Botón de creación, permiso solo Analista
 const btnNuevaSecuencia = document.getElementById('btnNuevaSecuencia');
  if (USER_ROLE === 'Analista' && btnNuevaSecuencia) {
    btnNuevaSecuencia.classList.remove('hidden-role');
  }
  // Bloques
  // Si no es Analista, ocultar ambos grupos y salir
  if (USER_ROLE !== 'Analista') {
    if (grupoInvalidar) grupoInvalidar.style.display = 'none';
    if (grupoRevisar) grupoRevisar.style.display = 'none';
    return; // Salimos para no agregar listeners
  }

  // Cuando se cambia toggleInvalidar
  toggleInvalidar.addEventListener('change', () => {
    if (toggleInvalidar.checked) {
      toggleRevisar.checked = false;
      if (grupoRevisar) grupoRevisar.classList.add('hidden');
    } else {
      if (grupoRevisar) grupoRevisar.classList.remove('hidden');
    }

    // Mostrar/ocultar columnas Invalidar
    document.querySelectorAll('.col-invalida').forEach(el => {
      el.classList.toggle('hidden-col', !toggleInvalidar.checked);
    });
  });

  // Cuando se cambia toggleRevisar
  toggleRevisar.addEventListener('change', () => {
    if (toggleRevisar.checked) {
      toggleInvalidar.checked = false;
      if (grupoInvalidar) grupoInvalidar.classList.add('hidden');
    } else {
      if (grupoInvalidar) grupoInvalidar.classList.remove('hidden');
    }

    // Mostrar/ocultar columnas Revisar
    document.querySelectorAll('.col-revisar').forEach(el => {
      el.classList.toggle('d-none', !toggleRevisar.checked);
    });
  });
});
