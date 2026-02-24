  
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

})
