// Instancia única del modal
const detalleModal = new bootstrap.Modal(document.getElementById('detalleModal'));

// Elementos reutilizados..
const modalStatusSpan = document.getElementById('modalStatus');
const btnGuardar = document.getElementById('btnGuardarCambios');
const nombreInput = document.getElementById('modalNombreInput');
const sistemaInput = document.getElementById('modalSistemaInput');
const observacionesTextarea = document.getElementById('modalObservaciones');
const responsablesSection = document.getElementById('responsablesSection');
const registradaItem = document.getElementById('registradaItem');
const validadaItem = document.getElementById('validadaItem');
const impresaItem = document.getElementById('impresaItem');
const reportadaItem = document.getElementById('reportadaItem');
const auditadaItem = document.getElementById('auditadaItem');
const descripcionContenedor = document.getElementById('modalDescripcion');

// Función para limpiar modal antes de abrirlo
function limpiarModal() {
  nombreInput.value = '';
  modalStatusSpan.textContent = '';
  modalStatusSpan.className = 'estado-dinamico badge rounded-pill';
  modalStatusSpan.dataset.status = '';
  modalStatusSpan.dataset.id = '';
  sistemaInput.innerHTML = '<option value="">Seleccione un sistema</option>';
  observacionesTextarea.value = '';
  responsablesSection.classList.add('d-none');
  registradaItem.style.display = 'none';
  validadaItem.style.display = 'none';
  impresaItem.style.display = 'none';
  reportadaItem.style.display = 'none';
  auditadaItem.style.display = 'none';
  descripcionContenedor.innerHTML = '';
  observacionesTextarea.removeAttribute('readonly');
  nombreInput.removeAttribute('readonly');
  sistemaInput.disabled = false;
  btnGuardar.style.display = 'inline-block';
}

// Función para asignar responsables y mostrar u ocultar filas
function setResponsable(item, usuarioKey, fechaKey, el, labelId) {
  const usuario = item[usuarioKey];
  const fecha = item[fechaKey];

  if (usuario && usuario !== 'None') {
    let fechaFormateada = '';
    if (fecha && fecha !== 'None') {
      const fechaObj = new Date(fecha);
      const dia = String(fechaObj.getDate()).padStart(2, '0');
      const mes = String(fechaObj.getMonth() + 1).padStart(2, '0');
      const anio = fechaObj.getFullYear();
      const hora = String(fechaObj.getHours()).padStart(2, '0');
      const minutos = String(fechaObj.getMinutes()).padStart(2, '0');
      
      fechaFormateada = ` el ${anio}/${mes}/${dia} ${hora}:${minutos}`;
    }
    document.getElementById(labelId).textContent = `${usuario}${fechaFormateada}`;
    el.style.display = 'list-item';
    return true;
  } else {
    el.style.display = 'none';
    return false;
  }
}

// Función para cargar opciones sistema y seleccionar el correcto
async function cargarOpcionesSistema(nombreSistema = null) {
  sistemaInput.innerHTML = '<option value="">Seleccione un sistema</option>';

  try {
    const res = await fetch('/listado_sistemas');
    if (!res.ok) throw new Error('Error cargando sistemas');
    const data = await res.json();
    const sistemas = data.sistemas;

    sistemas.forEach(sistema => {
      const option = document.createElement('option');
      option.value = sistema.id;
      option.textContent = sistema.nombre;
      if (nombreSistema && sistema.nombre === nombreSistema) {
        option.selected = true;
      }
      sistemaInput.appendChild(option);
    });
  } catch (error) {
    console.error('Error cargando sistemas:', error);
  }
}

// Handler para cambiar status al hacer click una sola vez
function modalStatusClickHandler(e) {
  e.stopPropagation();
  const status = modalStatusSpan.dataset.status;
  if (['Revisada', 'Impresa', 'Reportada'].includes(status)) {
    const nuevoStatus = 'Ensayo';
    modalStatusSpan.textContent = nuevoStatus;
    modalStatusSpan.className = 'estado-dinamico badge rounded-pill ' + getBadgeClass(nuevoStatus);
    modalStatusSpan.dataset.status = nuevoStatus;
    modalStatusSpan.removeEventListener('click', modalStatusClickHandler);
  }
}

// Añadimos el listener solo una vez
modalStatusSpan.addEventListener('click', modalStatusClickHandler);

// Función principal para asignar eventos y abrir modal con datos
function attachDetalleEvents() {
  document.querySelectorAll('.btn-detalles').forEach(button => {
button.addEventListener('click', async () => {
  limpiarModal();

  // Mostrar SweetAlert de carga
  Swal.fire({
    title: 'Cargando...',
    text: 'Por favor espere',
    allowOutsideClick: false,
    allowEscapeKey: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  const id = button.getAttribute('data-id');

  try {
    const res = await fetch('./listado_secuencias_validadas');
    if (!res.ok) throw new Error('Error al obtener datos');
    const data = await res.json();
    const item = data.find(seq => seq.id === parseInt(id));
    if (!item) throw new Error('Secuencia no encontrada');

    currentEditingId = item.id;

    // Asignar campos del modal
    nombreInput.value = item.nombre || '';
    modalStatusSpan.textContent = item.status || '';
    modalStatusSpan.className = 'estado-dinamico badge rounded-pill ' + getBadgeClass(item.status || '');
    modalStatusSpan.dataset.id = item.id;
    modalStatusSpan.dataset.status = item.status || '';
    if(item.status === 'Auditada') modalStatusSpan.textContent += ' 🔒';

    await cargarOpcionesSistema(item.sistema);

    function mostrarCampo(valor, idGrupo, idSpan) {
      const grupo = document.getElementById(idGrupo);
      const span = document.getElementById(idSpan);
      if (valor && valor !== 'None') {
        span.textContent = valor;
        grupo.style.display = '';
      } else {
        grupo.style.display = 'none';
      }
    }

    mostrarCampo(item.protocolo, 'grupoProtocolo', 'modalProtocolo');
    mostrarCampo(item.metodo, 'grupoMetodo', 'modalMetodo');
    mostrarCampo(item.parametro, 'grupoParametro', 'modalParametro');
    mostrarCampo(item.protocolo_proceso, 'grupoProceso', 'modalProceso');

    const mostrarRegistrada = setResponsable(item, 'registrada_por', 'fecha_registro', registradaItem, 'modalRegistradaPor');
    const mostrarValidada = setResponsable(item, 'validada_por', 'fecha_validacion', validadaItem, 'modalValidadaPor');
    const mostrarImpresa = setResponsable(item, 'impresa_por', 'fecha_impresion', impresaItem, 'modalImpresaPor');
    const mostrarReportada = setResponsable(item, 'reportada_por', 'fecha_reporte', reportadaItem, 'modalReportadaPor');
    const mostrarAuditada = setResponsable(item, 'auditada_por', 'fecha_auditoria', auditadaItem, 'modalAuditadaPor');

    if (mostrarRegistrada || mostrarValidada || mostrarImpresa || mostrarReportada || mostrarAuditada) {
      responsablesSection.classList.remove('d-none');
    } else {
      responsablesSection.classList.add('d-none');
    }

    descripcionContenedor.innerHTML = '';
    const tieneProtocolo = item.protocolo && item.protocolo !== 'None';
    const tieneMetodoOProceso = (item.metodo && item.metodo !== 'None') || (item.protocolo_proceso && item.protocolo_proceso !== 'None');

    if (tieneProtocolo && Array.isArray(item.descripcion)) {
      const html = item.descripcion.map(d => `
        <div class="mb-2 border-bottom pb-1">
          <strong>${d[0]}</strong><br>
          Lote: ${d[1]}<br>
          Código: ${d[2]}<br>
          Etiqueta: ${d[3]}
        </div>
      `).join('');
      descripcionContenedor.innerHTML = html;
    } else if (tieneMetodoOProceso && item.muestra_proceso) {
      const m = item.muestra_proceso;
      descripcionContenedor.innerHTML = `
        <div>
          <strong>${m.nombre || ''}</strong><br>
          Lote: ${m.lote || ''}<br>
          Código: ${m.codigo_producto || ''}<br>
          Etapa: ${m.etapa || ''}
        </div>
      `;
    } else {
      descripcionContenedor.innerHTML = '<span class="text-muted">No disponible</span>';
    }

    observacionesTextarea.value = item.observaciones || '';

    if (item.status === 'Auditada') {
      observacionesTextarea.setAttribute('readonly', true);
      nombreInput.setAttribute('readonly', true);
      sistemaInput.disabled = true;
      btnGuardar.style.display = 'none';
    } else {
      observacionesTextarea.removeAttribute('readonly');
      nombreInput.removeAttribute('readonly');
      sistemaInput.disabled = false;
      btnGuardar.style.display = 'inline-block';
    }

    // Cerrar SweetAlert y mostrar modal
    Swal.close();
    detalleModal.show();

  } catch (error) {
    // Cerrar SweetAlert en caso de error
    Swal.close();
    Swal.fire({
      icon: 'error',
      title: 'Error cargando detalles',
      text: error.message,
    });
  }
});
  });
}
