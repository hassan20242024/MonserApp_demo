
const renderMuestra = (item) => {
  const tieneProtocolo = item.protocolo && item.protocolo !== 'None';
  const tieneMetodoOProceso = (item.metodo && item.metodo !== 'None') || (item.protocolo_proceso && item.protocolo_proceso !== 'None');

  let visibleText = '';
  let hiddenText = '';

  if (tieneProtocolo && Array.isArray(item.descripcion) && item.descripcion.length > 0) {
    const d = item.descripcion[0];
    visibleText = `${d[0]} - Lote: ${d[1]}`;  // Ej: "NombreMuestra - Lote: 1234"
    // Concateno el resto con comas, para mejor lectura:
    hiddenText = item.descripcion.map(desc => desc.join(' - ')).join(', ');
  } else if (tieneMetodoOProceso && item.muestra_proceso) {
    const m = item.muestra_proceso;
    visibleText = `${m.nombre || ''} - Lote: ${m.lote || ''}`;
    hiddenText = [
      m.nombre,
      m.lote,
      m.codigo_producto,
      m.etapa
    ].filter(Boolean).join(', ');
  } else {
    return '<span class="text-muted">No disponible</span>';
  }

  return `
    <div class="muestra-resumen d-flex justify-content-between align-items-center" data-id="${item.id}" style="cursor:pointer;">
      <span>${visibleText}</span>
      <span class="detalle-muestra d-none" style="white-space: nowrap; overflow-x: auto; max-width: 60%;">${hiddenText}</span>
      <i class="bi-arrow-bar-down text-success toggle-icon ms-2" title="Ver más detalles"></i>
    </div>
  `;
};
