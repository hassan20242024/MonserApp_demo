
// ------------------------- CREAR SECUENCIAS ---------------------------------------------------------//
  let sistemaOtroTS, metodoTS, muestrasOtroTS;
function inicializarMuestrasOtroTS(multiple = true) {
  if (muestrasOtroTS) muestrasOtroTS.destroy();

  muestrasOtroTS = new TomSelect('#muestrasOtro', {
    placeholder: "Seleccione...",
    maxItems: multiple ? null : 1,   // Permite múltiples o uno solo
    closeAfterSelect: true,
    plugins: multiple ? ['remove_button'] : [],
    onItemAdd: function() {
      if (multiple) ocultarExcesoItems(this);
    },
    onItemRemove: function() {
      if (multiple) ocultarExcesoItems(this);
    }
  });

  if (multiple) ocultarExcesoItems(muestrasOtroTS);
}

function ocultarExcesoItems(tsInstance) {
  const items = tsInstance.control.querySelectorAll('.item');
  const maxVisibles = 3; // Mostrar solo los primeros 3 seleccionados

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
    document.querySelector("#sistemaOtro").value = sistemaOtroTS.getValue();
    document.querySelector("#metodo").value = metodoTS.getValue();
    document.querySelector("#muestrasOtro").value = muestrasOtroTS.getValue();
    // Aquí agregaríamos el valor de fecha_Inicio
    document.querySelector("#fecha_Inicio").value = document.querySelector("#fecha_Inicio").value;  // Usamos el valor que el usuario haya elegido
  }

  function resetFormOtro() {
  
    // Restablecer el formulario HTML
    const form = document.getElementById('myFormCreacionProtocoloOtro'); 
    form.reset(); // Restablecer los valores de los campos de texto, radio buttons, etc.
    

    // Limpiar los campos TomSelect
    sistemaOtroTS.clear();
    metodoTS.clear();
  if (muestrasOtroTS) muestrasOtroTS.destroy(); // ❌ destruir instancia anterior
  inicializarMuestrasOtroTS(true);  
  // Cambiar el título para creación
  }

document.addEventListener('DOMContentLoaded', () => {

  sistemaOtroTS = new TomSelect('#sistemaOtro', {
    placeholder: "Seleccione...",
    classNames: {
      control: 'form-select',
      dropdown: 'dropdown-menu',
      option: 'dropdown-item',
    }
  });
  metodoTS = new TomSelect('#metodo', {
    placeholder: "Seleccione...",
    classNames: {
      control: 'form-select',
      dropdown: 'dropdown-menu',
      option: 'dropdown-item',
    }
  });

  inicializarMuestrasOtroTS(true);           // ✅ volver a modo múltiple por defecto (creación)
  const modalEl = document.getElementById('crearSecuenciaModalOtro');
  const modal = bootstrap.Modal.getOrCreateInstance(modalEl);


//Titulo Modal Crear
modalEl.addEventListener('show.bs.modal', function () {
  const form = document.getElementById('myFormCreacionProtocoloOtro');

  if (!form.dataset.secuenciaId) {
    document.getElementById('crearSecuenciaModalLabelOtros').textContent = "Crear Secuencia (Otros)";
    document.getElementById('btnGuardarOActualizarOtros').textContent = "Guardar Secuencia";

    // Reinicializar TomSelect
    if (muestrasOtroTS) muestrasOtroTS.destroy();
    inicializarMuestrasOtroTS(true);

    fetch('/listado_muestras/')
      .then(res => {
        if (!res.ok) throw new Error("No se pudieron cargar las muestras");
        return res.json();
      })
      .then(data => {
        muestrasOtroTS.clearOptions();

        if (data.muestras.length === 0) {
          muestrasOtroTS.addOption({
            value: '',
            text: 'No hay muestras disponibles',
            disabled: true
          });
        } else {
          data.muestras.forEach(m => {
            muestrasOtroTS.addOption({
              value: m.id,
              text: `${m.nombre_muestra} Lote: ${m.lote_muestra || 'N/A'} Código interno: ${m.codigo_muestra_interno || 'N/A'} Código producto: ${m.codigo_muestra_producto || 'N/A'} Etapa: ${m.etapa_nombre || 'N/A'} Ensayo: ${m.ensayo_nombre || 'N/A'}`
            });
          });
        }

        muestrasOtroTS.refreshOptions();

        // ✅ Aseguramos cerrar el dropdown después de que se haya abierto automáticamente
        setTimeout(() => {
          muestrasOtroTS.close();
        }, 100);
      })
      .catch(error => {
        console.error("Error cargando muestras:", error);
        Swal.fire("Error", "No se pudieron cargar las muestras", "error");
      });
  }
});
  
function resetFormOtro() {
  const form = document.getElementById('myFormCreacionProtocoloOtro');
  form.reset();
  sistemaOtroTS.clear();
  metodoTS.clear();

  // 🔁 Siempre reinicia en modo múltiple (crear)
  if (muestrasOtroTS) muestrasOtroTS.destroy();
  inicializarMuestrasOtroTS(true);

  // 🧹 Limpia dataset de edición (si existía)
  delete form.dataset.secuenciaId;

  document.getElementById('crearSecuenciaModalLabelOtros').textContent = "Crear Secuencia (Otros)";  
  document.getElementById('btnGuardarOActualizarOtros').textContent = "Guardar Secuencia";        
}

  

  // Resetear el formulario cuando se cierra o muestra el modal
  //modalEl.addEventListener('show.bs.modal', resetFormOtro); 
  modalEl.addEventListener('hidden.bs.modal', resetFormOtro);

  //Funcion Submit
document.getElementById('myFormCreacionProtocoloOtro').addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;

  const nombre = form.querySelector('[name="nombre"]').value.trim();
  const fechaInicio = form.querySelector('[name="fecha_Inicio"]').value.trim();
  const sistema = sistemaOtroTS.getValue();
  const muestras = muestrasOtroTS.getValue();
  const metodo = metodoTS.getValue();
  const observaciones = form.querySelector('[name="observaciones"]').value.trim();
  const secuenciaId = form.dataset.secuenciaId || null;

  if (!nombre || nombre.length < 8) {
    Swal.fire("Error", "El nombre debe tener al menos 8 caracteres", "warning");
    return;
  }
  if (!fechaInicio || !sistema || !muestras || !metodo || !observaciones) {
    Swal.fire("Faltan campos", "Completa todos los campos obligatorios", "warning");
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
      formData.append("metodo", metodo);
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

  
     if (secuenciaId) {
  const secuencia = data.secuencia;  
  const oldRow = document.querySelector(`tr td[data-id='${secuencia.id}']`)?.closest("tr");
  if (oldRow) oldRow.remove();
  addRowToTable(secuencia); // usa directamente el objeto
} else {
          data.secuencias.forEach(secuencia => {
            datosSecuencias.push(secuencia);
            addRowToTable(secuencia);
          });
        }
      resetFormOtro();
 const modal = bootstrap.Modal.getInstance(document.getElementById("crearSecuenciaModalOtro"));
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
