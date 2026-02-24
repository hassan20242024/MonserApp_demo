// Instancia única del modal
const detalleModal = new bootstrap.Modal(document.getElementById('detalleModal'));

// Elementos usados
const modalNombre = document.getElementById('modalNombre');
const modalStatusSpan = document.getElementById('modalStatus');
const modalSistema = document.getElementById('modalSistema');
const responsablesSection = document.getElementById('responsablesSection');
const registradaItem = document.getElementById('registradaItem');
const impresaItem = document.getElementById('impresaItem');
const reportadaItem = document.getElementById('reportadaItem');
const auditadaItem = document.getElementById('auditadaItem');
const invalidadItem = document.getElementById('invalidadItem');
const descripcionContenedor = document.getElementById('modalDescripcion');
const observacionesTextarea = document.getElementById('modalObservaciones');

// Limpiar modal antes de cargar
function limpiarModal() {
  modalNombre.textContent = '';
  modalStatusSpan.textContent = '';
  modalStatusSpan.className = 'estado-dinamico badge rounded-pill';
  modalStatusSpan.dataset.id = '';
  modalStatusSpan.dataset.status = '';
  modalSistema.textContent = '';
  observacionesTextarea.value = '';

  // Ocultar campos técnicos
  ['grupoProtocolo', 'grupoMetodo', 'grupoParametro', 'grupoProceso'].forEach(id => {
    const grupo = document.getElementById(id);
    if (grupo) grupo.style.display = 'none';
  });

  // Ocultar responsables
  [registradaItem, impresaItem, reportadaItem, auditadaItem, invalidadItem].forEach(el => el.style.display = 'none');
  responsablesSection.classList.add('d-none');

  descripcionContenedor.innerHTML = '';
}

// Mostrar/ocultar campos técnicos
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

// Limpiar valor "None"
function limpiarNone(valor, reemplazo = 'No definido') {
  return (valor && valor !== 'None') ? valor : reemplazo;
}

// Formatear y asignar responsable
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

// Evento click para cambiar estado (se añade solo una vez)
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
modalStatusSpan.addEventListener('click', modalStatusClickHandler);


// Función principal
function attachDetalleEvents() {
  document.querySelectorAll('.btn-detalles').forEach(button => {
button.addEventListener('click', async () => {
  limpiarModal();

  // Mostrar alerta de carga
  Swal.fire({
    title: 'Cargando...',
    text: 'Espere un momento por favor',
    allowOutsideClick: false,
    allowEscapeKey: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  const id = button.getAttribute('data-id');
  const endpoint = button.getAttribute('data-endpoint') || '/crear_secuencias_en_curso/listado_secuencias_registradas';

  try {
    const res = await fetch(endpoint);
    if (!res.ok) throw new Error('Error al obtener datos');

    const data = await res.json();
    const item = data.find(seq => seq.id === parseInt(id));
    if (!item) throw new Error('Secuencia no encontrada');

    currentEditingId = item.id;

    // Datos generales
    modalNombre.textContent = item.nombre || '';

    modalStatusSpan.textContent = item.status || '';
    modalStatusSpan.className = 'estado-dinamico badge rounded-pill ' + getBadgeClass(item.status || '');
    modalStatusSpan.dataset.id = item.id;
    modalStatusSpan.dataset.status = item.status || '';
    if (item.status === 'Auditada') modalStatusSpan.textContent += ' 🔒';

    modalSistema.textContent = item.sistema || '';

    // Mostrar campos técnicos
    mostrarCampo(item.protocolo, 'grupoProtocolo', 'modalProtocolo');
    mostrarCampo(item.metodo, 'grupoMetodo', 'modalMetodo');
    mostrarCampo(item.parametro, 'grupoParametro', 'modalParametro');
    mostrarCampo(item.protocolo_proceso, 'grupoProceso', 'modalProceso');

    // Limpieza de valores "None"
    document.getElementById('modalProtocolo').textContent = limpiarNone(item.protocolo);
    document.getElementById('modalMetodo').textContent = limpiarNone(item.metodo);
    document.getElementById('modalParametro').textContent = limpiarNone(item.parametro, 'No aplica');
    document.getElementById('modalProceso').textContent = limpiarNone(item.protocolo_proceso);

    // Responsables
    const mostrarRegistrada = setResponsable(item, 'registrada_por', 'fecha_registro', registradaItem, 'modalRegistradaPor');
    const mostrarImpresa = setResponsable(item, 'impresa_por', 'fecha_impresion', impresaItem, 'modalImpresaPor');
    const mostrarReportada = setResponsable(item, 'reportada_por', 'fecha_reporte', reportadaItem, 'modalReportadaPor');
    const mostrarAuditada = setResponsable(item, 'auditada_por', 'fecha_auditoria', auditadaItem, 'modalAuditadaPor');
    const mostrarInvalida = setResponsable(item, 'invalidada_por', 'fecha_invalidez', invalidadItem, 'modalInvalidadaPor');

    if (mostrarRegistrada || mostrarImpresa || mostrarReportada || mostrarAuditada || mostrarInvalida) {
      responsablesSection.classList.remove('d-none');
    } else {
      responsablesSection.classList.add('d-none');
    }

    // Descripción dinámica
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

    // Observaciones
    observacionesTextarea.value = item.observaciones || '';

    // Cerrar loader y mostrar modal
    Swal.close();
    detalleModal.show();

  } catch (error) {
    // Cerrar loader y mostrar error
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

function getBadgeClass(status) {
  switch (status) {
    case 'Revisada': return 'bg-danger text-white';
    case 'Impresa': return 'bg-warning text-dark';
    case 'Reportada': return 'bg-success text-white';
    case 'Auditada': return 'bg-primary text-white';
    case 'Ensayo': return 'bg-info text-dark';
    case 'Registrada':
    case 'Invalida':
    default:
      return 'bg-secondary text-white';
  }
}
