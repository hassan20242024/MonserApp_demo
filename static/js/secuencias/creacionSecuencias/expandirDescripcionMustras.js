
function attachExpandMuestraEvents(data) {
  document.querySelectorAll('.muestra-resumen').forEach(el => {
    el.addEventListener('click', function () {
      const id = parseInt(this.dataset.id);
      const parentRow = this.closest('tr');

      const alreadyOpen = parentRow.nextElementSibling?.classList.contains('detalle-row');
      const icon = this.querySelector('.toggle-icon');

      // Si ya está abierto, lo cerramos
if (alreadyOpen) {
  parentRow.nextElementSibling.remove();
  icon.classList.remove('rotated');  // Quita la rotación al colapsar
  return;
}
icon.classList.add('rotated');
      // Cerramos cualquier otro abierto
      document.querySelectorAll('.detalle-row').forEach(r => r.remove());

      const item = data.find(i => i.id === id);
      let detalleHtml = '';

      const tieneProtocolo = item.protocolo && item.protocolo !== 'None';
      const tieneMetodoOProceso = (item.metodo && item.metodo !== 'None') || (item.protocolo_proceso && item.protocolo_proceso !== 'None');

      if (tieneProtocolo && Array.isArray(item.descripcion)) {
        detalleHtml = item.descripcion.map(d => `
          <div class="mb-1">
            <strong>${d[0]}</strong><br>
            Lote: ${d[1]}<br>
            Código: ${d[2]}<br>
            Etiqueta: ${d[3]}
          </div>
        `).join('');
      } else if (tieneMetodoOProceso && item.muestra_proceso) {
        const m = item.muestra_proceso;
        detalleHtml = `
          <div>
            <strong>${m.nombre || ''}</strong><br>
            Lote: ${m.lote || ''}<br>
            Código: ${m.codigo_producto || ''}<br>
            Etapa: ${m.etapa || ''}
          </div>
        `;
      } else {
        detalleHtml = '<span class="text-muted">No disponible</span>';
      }

      const detalleRow = document.createElement('tr');
      detalleRow.classList.add('detalle-row');
      detalleRow.innerHTML = `
        <td colspan="8">
          <div class="text-start p-2 bg-light border rounded">
            ${detalleHtml}
          </div>
        </td>
      `;
      parentRow.parentNode.insertBefore(detalleRow, parentRow.nextSibling);
    });
  });
}
