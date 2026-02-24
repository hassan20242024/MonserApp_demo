

  let sistemaPrTS, protocoloPrTS, muestrasPrTS;
  let muestrasPrCargando = false;
function inicializarMuestrasPrTS(multiple = true) {
  if (muestrasPrTS) muestrasPrTS.destroy();

  muestrasPrTS = new TomSelect('#muestrasPr', {
    placeholder: "Seleccione...",
    maxItems: multiple ? null : 1,
    closeAfterSelect: true,
    plugins: multiple ? ['remove_button'] : [],
    onItemAdd: function() {
      if (multiple) ocultarExcesoItems(this);
    },
    onItemRemove: function() {
      if (multiple) ocultarExcesoItems(this);
    }
  });

  if (multiple) ocultarExcesoItems(muestrasPrTS);
}

function ocultarExcesoItems(tsInstance) {
  const items = tsInstance.control.querySelectorAll('.item');
  const maxVisibles = 3;

  items.forEach((item, index) => {
    item.style.display = index < maxVisibles ? 'inline-block' : 'none';
  });

  const contadorExistente = tsInstance.control.querySelector('.contador-seleccionados');
  if (contadorExistente) contadorExistente.remove();

  if (items.length > maxVisibles) {
    const contador = document.createElement('span');
    contador.className = 'contador-seleccionados text-muted';
    contador.textContent = `+${items.length - maxVisibles} más`;
    contador.style.marginLeft = '6px';
    tsInstance.control.appendChild(contador);
  }
}


  function syncTomSelectFields() {
    document.querySelector("#sistemaPr").value = sistemaPrTS.getValue();
    document.querySelector("#protocoloPr").value = protocoloPrTS.getValue();
    document.querySelector("#muestrasPr").value = muestrasPrTS.getValue();
  }

function resetFormProceso() {
  const form = document.getElementById('myFormCreacionProtocoloProceso'); // o usa querySelector
  form.reset();
  sistemaPrTS.clear();
  protocoloPrTS.clear();
  if (muestrasPrTS) muestrasPrTS.destroy(); // ❌ destruir instancia anterior
  inicializarMuestrasPrTS(true);           // ✅ volver a modo múltiple por defecto (creación)
}

  document.addEventListener('DOMContentLoaded', () => {

    sistemaPrTS = new TomSelect('#sistemaPr', {
      placeholder: "Seleccione...",
      classNames: {
        control: 'form-select',
        dropdown: 'dropdown-menu',
        option: 'dropdown-item',
      }
    });

         protocoloPrTS = new TomSelect('#protocoloPr', {
      placeholder: "Seleccione...",
      classNames: {
        control: 'form-select',
        dropdown: 'dropdown-menu',
        option: 'dropdown-item',
      }
    });

   inicializarMuestrasPrTS(true);   

  const submitBtn = document.querySelector("#myFormCreacionProtocoloProceso button[type='submit']");
   
  protocoloPrTS.on("change", (value) => {
     muestrasPrTS.clear();         // Limpia selección actual
     muestrasPrTS.clearOptions();  // Elimina todas las opciones, incluidas previas
     muestrasPrCargando = true;
    submitBtn.disabled = true;

  if (!value) return;

 
  muestrasPrTS.addOption({ value: '__cargando__', text: 'Cargando...', disabled: true });
  muestrasPrTS.refreshOptions();


  fetch(`/ajax/muestras/${value}/`)
    .then(res => res.json())
    .then(data => {
      muestrasPrTS.clear();         // Limpia cualquier selección
      muestrasPrTS.clearOptions();  // Elimina "Cargando..."

      if (data.muestras.length === 0) {
        muestrasPrTS.addOption({ value: '', text: 'No hay muestras disponibles', disabled: true });
        muestrasPrTS.refreshOptions();
        return;
      }

      data.muestras.forEach(m => {
        muestrasPrTS.addOption({ value: m.id, text: m.nombre });
      });

      muestrasPrTS.refreshOptions();
      muestrasPrCargando = false;
      submitBtn.disabled = false;
    })
    .catch(err => {
      console.error("Error al cargar muestras:", err);
      muestrasPrTS.clear();
      muestrasPrTS.clearOptions();
      muestrasPrTS.addOption({ value: '', text: 'Error al cargar', disabled: true });
      muestrasPrTS.refreshOptions();
      Swal.fire("Error", "No se pudieron cargar las muestras.", "error");
      muestrasPrCargando = false;
      submitBtn.disabled = false;
    });
});
    const modalEl = document.getElementById('crearSecuenciaModalProceso');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);

    //Titulo Modal Crear
modalEl.addEventListener('show.bs.modal', function () {
  const form = document.getElementById('myFormCreacionProtocoloProceso');
  if (!form.dataset.secuenciaId) {
    document.getElementById('modalProcesoTitulo').textContent = 'Crear Secuencia Protocolo Proceso';
    document.getElementById('btnGuardarSecuencia').textContent = 'Guardar Secuencia';
    
    // Reinicializar TomSelect para múltiples muestras
    if (muestrasPrTS) muestrasPrTS.destroy();
    inicializarMuestrasPrTS(true);  // 👈 vuelve a activar modo múltiple
  }
});
  
function resetFormProceso() {
  const form = document.getElementById('myFormCreacionProtocoloProceso');
  form.reset();
  sistemaPrTS.clear();
  protocoloPrTS.clear();

  // 🔁 Siempre reinicia en modo múltiple (crear)
  if (muestrasPrTS) muestrasPrTS.destroy();
  inicializarMuestrasPrTS(true);

  // 🧹 Limpia dataset de edición (si existía)
  delete form.dataset.secuenciaId;

  document.getElementById('modalProcesoTitulo').textContent = 'Crear Secuencia Protocolo Proceso';
  document.getElementById('btnGuardarSecuencia').textContent = 'Guardar Secuencia';
}

//modalEl.addEventListener('show.bs.modal', resetFormProceso);
modalEl.addEventListener('hidden.bs.modal', resetFormProceso);

//Funcion Submit
document.getElementById('myFormCreacionProtocoloProceso').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;

  const nombre = form.querySelector('[name="nombre"]').value.trim();
  const fechaInicio = form.querySelector('[name="fecha_Inicio"]').value.trim();
  const sistema = sistemaPrTS.getValue();
  const muestras = muestrasPrTS.getValue();
  const protocoloProceso = protocoloPrTS.getValue();
  const observaciones = form.querySelector('[name="observaciones"]').value.trim();
  const secuenciaId = form.dataset.secuenciaId || null;

    if (!nombre || nombre.length < 8) {
      Swal.fire("Campo inválido", "El nombre debe tener al menos 8 caracteres", "warning");
      return;
    }

    if (!fechaInicio) {
      Swal.fire("Campo obligatorio", "Debe ingresar la fecha de inicio", "warning");
      return;
    }

    if (!sistema) {
      Swal.fire("Campo obligatorio", "Debe seleccionar un sistema", "warning");
      return;
    }

    if (!protocoloProceso) {
      Swal.fire("Campo obligatorio", "Debe seleccionar un protocolo", "warning");
      return;
    }

    // ✅ Verificar si parámetros están cargando o vacíos
    if (muestrasPrCargando) {
      Swal.fire("Espere", "La muestras aún se están cargando. Intente de nuevo en unos segundos.", "info");
      return;
    }

    if (!muestras || !Array.isArray(muestras) || muestras.length === 0 || muestras.includes('__cargando__')) {
      Swal.fire("Campo obligatorio", "Debe esperar a que las muestras carguen completamente y seleccionar al menos una.", "warning");
      return;
    }

    if (!observaciones) {
      Swal.fire("Campo obligatorio", "Debe ingresar observaciones", "warning");
      return;
    }

  const confirm = await Swal.fire({
    title: secuenciaId ? "¿Actualizar secuencia?" : "¿Crear secuencia?",
    text: secuenciaId ? "Estás por editar una secuencia existente." : "Estás por crear una nueva secuencia.",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Sí, continuar",
    cancelButtonText: "Cancelar"
  });

  if (!confirm.isConfirmed) return;

 
  setTimeout(async () => {
    document.getElementById('spinner-carga').classList.remove('d-none');
    try {
      const formData = new FormData();
      formData.append("csrfmiddlewaretoken", form.querySelector('[name=csrfmiddlewaretoken]').value);
      formData.append("nombre", nombre);
      formData.append("fecha_Inicio", fechaInicio);
      formData.append("observaciones", observaciones);
      formData.append("sistema", sistema);
      muestras.forEach(m => formData.append("muestras", m));
      formData.append("protocolo_proceso", protocoloProceso);
       formData.append("fecha_configuracion_protocolo_metodo", form.querySelector('[name="fecha_configuracion_protocolo_metodo"]').value);
        formData.append("fecha_configuracion_protocolo_proceso", form.querySelector('[name="fecha_configuracion_protocolo_proceso"]').value);

      // ✅ Ruta correcta según sea edición o creación
      const url = secuenciaId ? `/editar_secuencia/${secuenciaId}/` : '/crear_secuencias_protocolo_metodo/';
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: formData
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.message || 'Error');

      Swal.fire({
        icon: 'success',
        title: '¡Éxito!',
        text: data.message || 'Secuencia actualizada.',
        timer: 1500,
        showConfirmButton: false
      });

      // Actualiza la tabla si es edición o agrega si es nuevo
     if (secuenciaId) {
  const secuencia = data.secuencia;  // objeto, no lista
  const oldRowp = document.querySelector(`tr td[data-id='${secuencia.id}']`)?.closest("tr");
  if (oldRowp) oldRowp.remove();
  addRowToTable(secuencia); 
} else {
          data.secuencias.forEach(secuencia => {
            datosSecuencias.push(secuencia);
            addRowToTable(secuencia);
           // renderTable(filteredData.length ? filteredData : allData);
          });
        }
  document.getElementById('modalProcesoTitulo').textContent = 'Crear Secuencia protocolo Proceso';
      resetFormProceso();
 const modal = bootstrap.Modal.getInstance(document.getElementById("crearSecuenciaModalProceso"));
  modal.hide();
    } catch (err) {
      Swal.fire("Error", err.message || "Error al procesar la solicitud", "error");
    } finally {
      document.getElementById('spinner-carga').classList.add('d-none');
      // Limpia el dataset después de editar
      delete form.dataset.secuenciaId;
    }
  }, 300);
});

  });
