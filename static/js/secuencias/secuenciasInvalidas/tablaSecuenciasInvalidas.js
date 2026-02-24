const seleccionados = new Set();
let datosSecuencias = [];
let allData = [];
let filteredData = [];
let currentPage = 1;
let itemsPerPage = 10;

// 🔁 Aplicar visibilidad según switches de columna

// ✅ Agregar fila a tabla (nuevo o reemplazo)
function addRowToTable(item) {
  item.protocolo = item.protocolo || "None";
  item.metodo = item.metodo || "None";
  item.protocolo_proceso = item.protocolo_proceso || "None";

  const index = allData.findIndex(i => i.id === item.id);
  if (index !== -1) {
    allData[index] = item;
  } else {
    allData.push(item);
  }

  aplicarFiltrosPorColumna();
  renderTable(filteredData.length ? filteredData : allData);
}

// ⚙️ Obtener valor de cookie CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// 🔄 Reemplazo de valores vacíos o 'None'
function limpiarNone(valor, reemplazo = 'No aplica') {
  return (valor && valor !== 'None') ? valor : reemplazo;
}

// 🔧 Extraer mejor nombre: método, protocolo o proceso
function getMetodoProtocolo(item) {
  const opciones = [item.metodo, item.protocolo, item.protocolo_proceso];
  for (const valor of opciones) {
    if (valor && valor !== 'None') return valor;
  }
  return 'No definido';
}

// 🧾 Renderizar la tabla con paginación
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
<td class="btn-detalles icon-hover-zoom text-secondary"
    data-id="${item.id}"
    data-endpoint="/crear_secuencias_en_curso/listado_secuencias_invalidas"
    title="Ver Detalles"
    style="cursor:pointer;">
  <span class="fa fa-camera-retro">${item.nombre}</span>
</td>
      <td>${getMetodoProtocolo(item)}</td>
      <td>${limpiarNone(item.parametro)}</td>
      <td>${renderMuestra(item)}</td>
      <td>${item.sistema || ''}</td>
      <td>${item.invalidar_Secuencia || ''}</td>
      <td >
        ${
          item.protocolo === "None" && item.metodo === "None"
            ? `<input type="checkbox" class="checkbox-revisar" data-id="${item.id}" data-tipo="protocolo_proceso">`
            : item.protocolo === "None" && item.protocolo_proceso === "None"
            ? `<input type="checkbox" class="checkbox-revisar" data-id="${item.id}" data-tipo="otro">`
            : item.protocolo !== "None"
            ? `<input type="checkbox" class="checkbox-revisar" data-id="${item.id}" data-tipo="protocolo_metodo">`
            : ''
        }
      </td>
    </tr>
  `).join('');

  tbody.innerHTML = rows;

  renderPagination(data.length);
  attachEstadoEvents();
  attachDetalleEvents();
  attachExpandMuestraEvents(data);
}

// 🔢 Renderizar paginación
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

// 🧹 Filtros por columnas
function aplicarFiltrosPorColumna() {
  const filtroNombre = document.getElementById('filtroNombre').value.toLowerCase();
  const filtroMetodo = document.getElementById('filtroMetodo').value.toLowerCase();
  const filtroParametro = document.getElementById('filtroParametro').value.toLowerCase();
  const filtroSistema = document.getElementById('filtroSistema').value.toLowerCase();
  const filtroMuestra = document.getElementById('filtroMuestra').value.toLowerCase();

  filteredData = allData.filter(item => {
    const nombre = (item.nombre || '').toLowerCase();
    const metodo = getMetodoProtocolo(item).toLowerCase();
    const parametro = (item.parametro || '').toLowerCase();
    const sistema = (item.sistema || '').toLowerCase();

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
      metodo.includes(filtroMetodo) &&
      parametro.includes(filtroParametro) &&
      sistema.includes(filtroSistema) &&
      muestraTexto.includes(filtroMuestra)
    );
  });

  currentPage = 1;
  renderTable(filteredData);
}

// 🎛 Eventos para filtros
[
  'filtroNombre',
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

// 📦 Cargar datos desde servidor
async function getDataAndRender() {
  try {
    const response = await fetch("/crear_secuencias_en_curso/listado_secuencias_invalidas");
    const data = await response.json();
    allData = data;
    filteredData = allData;
    renderTable(filteredData);
  } catch (error) {
    document.getElementById('tbody').innerHTML = `<tr><td colspan="8">Error cargando datos</td></tr>`;
    console.error(error);
  } finally {
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  }
}

// 📌 Adjuntar eventos
function attachEstadoEvents() {
  // Intencionalmente vacía: se ha deshabilitado el cambio de estado desde la tabla
}

document.querySelectorAll('.estado-checkboxes input[type="checkbox"]').forEach(checkbox => {
  checkbox.addEventListener('change', function () {
    if (this.checked) {
      document.querySelectorAll('.estado-checkboxes input[type="checkbox"]').forEach(cb => {
        if (cb !== this) cb.checked = false;
      });
    }
  });
});

// 🔁 Selector de cantidad por página
document.getElementById('itemsPerPage').addEventListener('change', (e) => {
  itemsPerPage = parseInt(e.target.value, 10);
  currentPage = 1;
  renderTable(filteredData.length ? filteredData : allData);
});

// ▶️ Ejecutar al cargar
document.addEventListener('DOMContentLoaded', getDataAndRender);
