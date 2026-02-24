
let allData = [];
let currentPage = 1;
let itemsPerPage = 10;  // variable actualizable
let filteredData = [];

// Función para renderizar la tabla con paginación
function renderTable(data) {
  const tbody = document.getElementById("tbody");

  if (!data.length) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center text-muted">No hay datos disponibles.</td></tr>`;
    return;
  }

  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedData = data.slice(startIndex, endIndex);

  const rows = paginatedData.map(item => `
    <tr class="text-center">
      <td style="display:none;">${item.fecha_Inicio || ''}</td>
      <td class="btn-detalles icon-hover-zoom  text-secondary" data-id="${item.id}" title="Ver Detalles" style="cursor:pointer;">
        <span class="fa fa-camera-retro">${item.nombre}</span>
      </td>
      <td>${buildEstadoSpan(item)}</td>
      <td>${getMetodoProtocolo(item)}</td>
      <td>${limpiarNone(item.parametro)}</td>
      <td>${renderMuestra(item)}</td>
      <td>${item.sistema || ''}</td>
    </tr>
  `).join('');

  tbody.innerHTML = rows;

  renderPagination(data.length);
  attachEstadoEvents();
  attachDetalleEvents();
  attachExpandMuestraEvents(data);
}

// Event listener para el select de items por página
const selectItemsPerPage = document.getElementById('itemsPerPage');

selectItemsPerPage.addEventListener('change', (e) => {
  itemsPerPage = parseInt(e.target.value, 10);
  currentPage = 1; // reiniciar a página 1 cuando cambie el tamaño de página
  renderTable(filteredData.length ? filteredData : allData);
});
