
function getMetodoProtocolo(item) {
  const opciones = [item.metodo, item.protocolo, item.protocolo_proceso];
  for (const valor of opciones) {
    if (valor && valor !== 'None') {
      return valor;
    }
  }
  return 'No definido';
}
function renderPagination(totalItems) {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const totalPages = Math.ceil(totalItems / itemsPerPage);
  if (totalPages <= 1) return;

  for (let i = 1; i <= totalPages; i++) {
    const btn = document.createElement("button");
    btn.textContent = i;
    btn.className = `btn btn-sm mx-1 ${i === currentPage ? "btn-primary" : "btn-outline-secondary"}`;
    btn.addEventListener("click", () => {
      currentPage = i;
      renderTable(filteredData);
    });
    pagination.appendChild(btn);
  }
}
function aplicarFiltrosPorColumna() {
  const filtroNombre = document.getElementById('filtroNombre').value.toLowerCase();
  const filtroEstado = document.getElementById('filtroEstado').value;
  const filtroMetodo = document.getElementById('filtroMetodo').value.toLowerCase();
  const filtroParametro = document.getElementById('filtroParametro').value.toLowerCase();
  const filtroSistema = document.getElementById('filtroSistema').value.toLowerCase();
  const filtroMuestra = document.getElementById('filtroMuestra').value.toLowerCase();

  filteredData = allData.filter(item => {
    const nombre = (item.nombre || '').toLowerCase();
    const estado = item.status || '';
    const metodo = getMetodoProtocolo(item).toLowerCase();
    const parametro = (item.parametro || '').toLowerCase();
    const sistema = (item.sistema || '').toLowerCase();

    // Extraer texto oculto de muestra
    let muestraTexto = '';
    const tieneProtocolo = item.protocolo && item.protocolo !== 'None';
    const tieneMetodoOProceso = (item.metodo && item.metodo !== 'None') || (item.protocolo_proceso && item.protocolo_proceso !== 'None');

    if (tieneProtocolo && Array.isArray(item.descripcion)) {
      muestraTexto = item.descripcion.map(d => d.join(' ')).join(' ').toLowerCase();
    } else if (tieneMetodoOProceso && item.muestra_proceso) {
      const m = item.muestra_proceso;
      muestraTexto = `${m.nombre || ''} ${m.lote || ''} ${m.codigo_producto || ''} ${m.etapa || ''}`.toLowerCase();
    }

    return (
      nombre.includes(filtroNombre) &&
      (filtroEstado === '' || estado === filtroEstado) &&
      metodo.includes(filtroMetodo) &&
      parametro.includes(filtroParametro) &&
      sistema.includes(filtroSistema) &&
      muestraTexto.includes(filtroMuestra)
    );
  });

  currentPage = 1;
  renderTable(filteredData);
}

[
  'filtroNombre',
  'filtroEstado',
  'filtroMetodo',
  'filtroParametro',
  'filtroSistema',
  'filtroMuestra'
].forEach(id => {
  const el = document.getElementById(id);
  if (el) {
    const eventType = el.tagName === 'SELECT' ? 'change' : 'input';
    el.addEventListener(eventType, aplicarFiltrosPorColumna);
  }
});


document.getElementById('filtroEstado').addEventListener('change', aplicarFiltrosPorColumna);
