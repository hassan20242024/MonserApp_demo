
let sistemaTS, protocoloTS, parametroTS;
let parametrosCargando = false;

function inicializarParametroTS(multiple = true) {
  if (parametroTS) parametroTS.destroy();

  parametroTS = new TomSelect('#parametro_sq', {
    placeholder: "Seleccione...",
    maxItems: multiple ? null : 1,
    closeAfterSelect: true,
    plugins: multiple ? ['remove_button'] : [],
    onItemAdd: function () {
      if (multiple) ocultarExcesoItems(this);
    },
    onItemRemove: function () {
      if (multiple) ocultarExcesoItems(this);
    }
  });

  if (multiple) ocultarExcesoItems(parametroTS);
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



function resetForm() {
  const form = document.getElementById('myFormCreacionProtocoloMetodo');
  form.reset();
  form.removeAttribute('data-secuencia-id');
  sistemaTS.clear();
  protocoloTS.clear();
  if (parametroTS) parametroTS.destroy(); // ❌ destruir instancia anterior
  inicializarParametroTS(true); 
  // Cambiar el título para creación
  document.getElementById('crearSecuenciaModalLabel').textContent = "Crear Secuencia Protocolo Metodo";  
    document.getElementById('btnGuardarOActualizarMetodo').textContent = "Guardar Secuencia";        
      
}

document.addEventListener('DOMContentLoaded', () => {
  sistemaTS = new TomSelect('#sistema', { placeholder: "Seleccione..." });
  protocoloTS = new TomSelect('#protocolo', { placeholder: "Seleccione..." });
inicializarParametroTS(true); // Creación: múltiple

  const submitBtn = document.querySelector("#myFormCreacionProtocoloMetodo button[type='submit']");

  protocoloTS.on("change", (value) => {
    parametroTS.clear();
    parametroTS.clearOptions();
    parametrosCargando = true;
    submitBtn.disabled = true;

    if (!value) return;

    parametroTS.addOption({ value: '__cargando__', text: 'Cargando...', disabled: true });
    parametroTS.refreshOptions();

    fetch(`/ajax/parametros/${value}/`)
      .then(res => res.json())
      .then(data => {
        parametroTS.clear();
        parametroTS.clearOptions();

        if (data.parametros.length === 0) {
          parametroTS.addOption({ value: '', text: 'No hay parámetros disponibles', disabled: true });
           parametroTS.refreshOptions();
           return

        } else {
          data.parametros.forEach(p => {
            parametroTS.addOption({ value: p.id, text: p.nombre });
          });
        }

        parametroTS.refreshOptions();
        parametrosCargando = false;
        submitBtn.disabled = false;
      })
      .catch(err => {
        console.error("Error al cargar parámetros:", err);
        parametroTS.clear();
        parametroTS.clearOptions();
        parametroTS.addOption({ value: '', text: 'Error al cargar', disabled: true });
        parametroTS.refreshOptions();

        Swal.fire("Error", "No se pudieron cargar los parámetros.", "error");
        parametrosCargando = false;
        submitBtn.disabled = false;
      });
  });

  const modalEl = document.getElementById('crearSecuenciaModal');
  const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
  modalEl.addEventListener('show.bs.modal', resetForm);
  modalEl.addEventListener('hidden.bs.modal', resetForm);

  // ✅ Form Submit
  document.getElementById('myFormCreacionProtocoloMetodo').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;

    const nombre = form["nombre"].value.trim();
    const fechaInicio = form.querySelector('[name="fecha_Inicio"]')?.value.trim();
    const sistema = sistemaTS.getValue();
    const protocolo = protocoloTS.getValue();
    const parametros = parametroTS.getValue();
    const observaciones = form["observaciones"].value.trim();
    const secuenciaId = form.dataset.secuenciaId || null;
    //console.log('Fecha Inicio:', fechaInicio);


    // 🟡 VALIDACIONES
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

    if (!protocolo) {
      Swal.fire("Campo obligatorio", "Debe seleccionar un protocolo", "warning");
      return;
    }

    // ✅ Verificar si parámetros están cargando o vacíos
    if (parametrosCargando) {
      Swal.fire("Espere", "Los parámetros aún se están cargando. Intente de nuevo en unos segundos.", "info");
      return;
    }

    if (!parametros || !Array.isArray(parametros) || parametros.length === 0 || parametros.includes('__cargando__')) {
      Swal.fire("Campo obligatorio", "Debe esperar a que los parámetros carguen completamente y seleccionar al menos uno.", "warning");
      return;
    }

    if (!observaciones) {
      Swal.fire("Campo obligatorio", "Debe ingresar observaciones", "warning");
      return;
    }

    // Confirmación
    const confirm = await Swal.fire({
      title: secuenciaId ? "¿Actualizar secuencia?" : "¿Crear secuencia?",
      text: secuenciaId ? "Estás por editar una secuencia existente." : "Estás por crear una nueva secuencia.",
      icon: "question",
      showCancelButton: true,
      confirmButtonText: "Sí, continuar",
      cancelButtonText: "Cancelar"
    });

    if (!confirm.isConfirmed) return;

   
    // Envío
    setTimeout(async () => {
      document.getElementById('spinner-carga').classList.remove('d-none');
      try {
        const formData = new FormData();
        formData.append("csrfmiddlewaretoken", form.querySelector('[name=csrfmiddlewaretoken]').value);
        formData.append("nombre", nombre);
        formData.append("fecha_Inicio", fechaInicio);
        formData.append("sistema", sistema);
        formData.append("protocolo", protocolo);
        formData.append("parametros", JSON.stringify(parametros));
        formData.append("observaciones", observaciones);
        // Si estoy editando (secuenciaId existe), solo mando un parámetro:
if (secuenciaId) {
  // parámetro puede ser string o array con un solo elemento, forzar string:
  let parametroEditar = Array.isArray(parametros) ? parametros[0] : parametros;
  formData.append("parametro_sq", parametroEditar);
} else {
  // creación: envía cada parámetro por separado para que backend reciba lista
  if (Array.isArray(parametros)) {
    parametros.forEach(p => formData.append("parametro_sq", p));
  } else {
    // si sólo es string, envía uno solo
    formData.append("parametro_sq", parametros);
  }
}

        formData.append("fecha_configuracion_protocolo_metodo", form.querySelector('[name="fecha_configuracion_protocolo_metodo"]').value);
        formData.append("fecha_configuracion_protocolo_proceso", form.querySelector('[name="fecha_configuracion_protocolo_proceso"]').value);

        const url = secuenciaId ? `/editar_secuencia/${secuenciaId}/` : '/crear_secuencias_protocolo_metodo/';
        const res = await fetch(url, {
          method: 'POST',
          headers: {
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
          },
          body: formData
        });

        const data = await res.json();
        console.log("Respuesta del backend:", data);

        if (!res.ok) throw new Error(data.message || "Error al guardar");

        Swal.fire({
          icon: 'success',
          title: '¡Éxito!',
          text: data.message || 'Secuencia guardada correctamente.',
          timer: 1500,
          showConfirmButton: false
        });

       if (secuenciaId) {
  const secuencia = data.secuencia;  // objeto, no lista
  const oldRow = document.querySelector(`tr td[data-id='${secuencia.id}']`)?.closest("tr");
  if (oldRow) oldRow.remove();
  addRowToTable(secuencia); // usa directamente el objeto
} else {
          data.secuencias.forEach(secuencia => {
            datosSecuencias.push(secuencia);
            addRowToTable(secuencia);
          });
        }
 bootstrap.Modal.getInstance(document.getElementById('crearSecuenciaModal')).hide();

      } catch (err) {
        Swal.fire("Error", err.message || "Ocurrió un error al guardar", "error");
      } finally {
        document.getElementById('spinner-carga').classList.add('d-none');
      }
    }, 300);
  });
});

