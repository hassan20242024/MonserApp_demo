

  async function editarSecuenciaMetodo(id) {
    
  if (!id) {
    Swal.fire("Error", "ID de secuencia no válido", "error");
    return;
  }

  const form = document.getElementById('myFormCreacionProtocoloMetodo');
  const spinner = document.getElementById('spinner-carga');
  const modalEl = document.getElementById('crearSecuenciaModal');
  const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
//spinner para abrir
   Swal.fire({
      title: "Cargando datos...",
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => Swal.showLoading()
    });
  resetForm();

  try {
    const res = await fetch(`/editar_secuencia/${id}/`);
    if (!res.ok) throw new Error(`Error HTTP: ${res.status}`);
    const data = await res.json();
   try {
    form.nombre.value = data.nombre || 'Nombre de prueba';
    form.fecha_Inicio.value = data.fecha_Inicio ? data.fecha_Inicio.slice(0,16) : '2025-07-08T14:45';
    form.observaciones.value = data.observaciones || 'Observaciones de prueba';

    console.log('Campos asignados:', form.nombre.value, form.fecha_Inicio.value, form.observaciones.value);
  } catch(e) {
    console.error('Error asignando campos:', e);
  }

    // ✅ Setear valores básicos
    form.nombre.value = data.nombre || '';
    form.fecha_Inicio.value = data.fecha_Inicio || '';
    form.observaciones.value = data.observaciones || '';
    form.dataset.secuenciaId = id;

    sistemaTS.setValue(data.sistema || '');
    protocoloTS.setValue(data.protocolo || '');
     inicializarParametroTS(false);

    // ✅ Esperar que se carguen los parámetros antes de setear el valor seleccionado
    const mRes = await fetch(`/ajax/parametros/${data.protocolo}/`);
    if (!mRes.ok) throw new Error("No se pudieron obtener los parámetros");
    const pdata = await mRes.json();


    parametroTS.clear();
    parametroTS.clearOptions();

    if (pdata.parametros.length === 0) {
      parametroTS.addOption({ value: '', text: 'No hay parámetros disponibles', disabled: true });
    } else {
      pdata.parametros.forEach(p => {
        parametroTS.addOption({ value: p.id, text: p.nombre });
      });
    }

    parametroTS.refreshOptions();

const parametroSeleccionado = data.parametro_sq || '';
const parametrosDisponibles = pdata.parametros.map(p => p.id.toString());

if (parametrosDisponibles.includes(parametroSeleccionado.toString())) {
  parametroTS.setValue([parametroSeleccionado.toString()]);
   parametroTS.close();
} else {
  console.warn("⚠️ El parámetro seleccionado no está en la lista de opciones cargadas.");
}

    // ✅ Mostrar modal
document.getElementById('crearSecuenciaModalLabel').textContent = "Editar Secuencia Protocolo Metodo";
document.getElementById('btnGuardarOActualizarMetodo').textContent = "Editar Secuencia";        
    modalEl.removeEventListener('show.bs.modal', resetForm);
    modal.show();

  } catch (error) {
    console.error("Error al cargar secuencia:", error);
    Swal.fire("Error", error.message || "No se pudo cargar la secuencia", "error");

  } finally {
   // Cerrar el spinner de carga
    Swal.close();
  }
}
