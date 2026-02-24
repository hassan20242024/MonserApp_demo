
// Función para mostrar u ocultar "+ más..." basado en la cantidad de items seleccionados
function actualizarMasTexto(ts) {
  const control = ts.control;
  const items = control.querySelectorAll('.item');

  // Elimina cualquier "+ más..." anterior
  const existente = control.querySelector('.ts-mas');
  if (existente) existente.remove();

  if (items.length > 3) {
    const span = document.createElement('span');
    span.textContent = ' + más...';
    span.className = 'ts-mas';
    control.appendChild(span);
  }
}
