

  async function editarSecuenciaProceso(id) {
    if (!id) {
      Swal.fire("Error", "ID de secuencia no válido", "error");
      return;
    }

    const form = document.getElementById('myFormCreacionProtocoloProceso');
    const spinner = document.getElementById('spinner-carga');
    const modalEl = document.getElementById('crearSecuenciaModalProceso');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    // Mostrar spinner
//spinner para abrir
   Swal.fire({
      title: "Cargando datos...",
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => Swal.showLoading()
    });
  resetForm();
    resetFormProceso();
    try {
      const res = await fetch(`/editar_secuencia/${id}/`);
      if (!res.ok) throw new Error(`Error HTTP: ${res.status}`);
      const data = await res.json();
      // ✅ Llenar campos del formulario
      form.nombre.value = data.nombre || '';
      form.fecha_Inicio.value = data.fecha_Inicio || '';
      sistemaPrTS.setValue(data.sistema || '');
      protocoloPrTS.setValue(data.protocolo_proceso || '');
      form.observaciones.value = data.observaciones || '';
      form.dataset.secuenciaId = id;
      inicializarMuestrasPrTS(false);

      // 🔁 Esperar carga de muestras
      const mRes = await fetch(`/ajax/muestras/${data.protocolo_proceso}/`);
      if (!mRes.ok) throw new Error("No se pudieron obtener las muestras");
      const mdata = await mRes.json();
      muestrasPrTS.clear();
      muestrasPrTS.clearOptions();

      if (mdata.muestras.length === 0) {
        muestrasPrTS.addOption({ value: '', text: 'No hay muestras disponibles', disabled: true });
      } else {
        mdata.muestras.forEach(m => {
          muestrasPrTS.addOption({ value: m.id, text: m.nombre });
        });
      }

      muestrasPrTS.refreshOptions();
      muestrasPrTS.setValue(data.muestras || '');
      // ✅ Mostrar modal
      document.getElementById('modalProcesoTitulo').textContent = 'Editar Secuencia Protocolo Proceso';
      document.getElementById('btnGuardarSecuencia').textContent = 'Editar Secuencia';
      modal.show();

    } catch (error) {
      console.error("Error al cargar secuencia:", error);
      Swal.fire("Error", error.message || "No se pudo cargar la secuencia", "error");

    } finally {
 Swal.close();    }
  }
