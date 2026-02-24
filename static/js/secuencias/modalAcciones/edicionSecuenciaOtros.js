
// ------------------------- EDITAR SECUENCIAS ---------------------------------------------------------//
  async function editarSecuenciaOtro(id) {
    if (!id) {
      Swal.fire("Error", "ID de secuencia no válido", "error");
      return;
    }

    const form = document.getElementById('myFormCreacionProtocoloOtro');
    const spinner = document.getElementById('spinner-carga');
    const modalEl = document.getElementById('crearSecuenciaModalOtro');
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
    // Mostrar spinner
//spinner para abrir
   Swal.fire({
      title: "Cargando datos...",
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => Swal.showLoading()
    });
  resetFormOtro();
   
    try {
      const res = await fetch(`/editar_secuencia/${id}/`);
      if (!res.ok) throw new Error(`Error HTTP: ${res.status}`);
      const data = await res.json();
      console.log("🎯 Data recibida:", data);
      form.nombre.value = data.nombre || '';
      form.fecha_Inicio.value = data.fecha_Inicio || '';
      sistemaOtroTS.setValue(data.sistema || '');
      metodoTS.setValue(data.metodo || '');
      form.observaciones.value = data.observaciones || '';
      form.dataset.secuenciaId = id;
      inicializarMuestrasOtroTS(false);

      // 🔁 Esperar carga de muestras
      const mRes = await fetch(`/listado_muestras/`);
      if (!mRes.ok) throw new Error("No se pudieron obtener las muestras");
      const mdata = await mRes.json();
      muestrasOtroTS.clear();
      muestrasOtroTS.clearOptions();

      if (mdata.muestras.length === 0) {
        muestrasOtroTS.addOption({ value: '', text: 'No hay muestras disponibles', disabled: true });
      } else {
        mdata.muestras.forEach(m => {
          muestrasOtroTS.addOption({ 
  value: m.id, 
text: `${m.nombre_muestra} Lote: ${m.lote_muestra || 'N/A'} Código interno: ${m.codigo_muestra_interno || 'N/A'} Código producto: ${m.codigo_muestra_producto || 'N/A'} Etapa: ${m.etapa_nombre || 'N/A'} Ensayo: ${m.ensayo_nombre || 'N/A'}`
});

        });
      }

      muestrasOtroTS.refreshOptions();
      setTimeout(() => {
  muestrasOtroTS.setValue(data.muestras || '');
  muestrasOtroTS.blur(); // Cierra el dropdown si se abrió automáticamente
}, 100); 
      
      // ✅ Mostrar modal
  document.getElementById('crearSecuenciaModalLabelOtros').textContent = "Editar Secuencia (Otros)";  
  document.getElementById('btnGuardarOActualizarOtros').textContent = "Editar Secuencia";        
      modal.show();

    } catch (error) {
      console.error("Error al cargar secuencia:", error);
      Swal.fire("Error", error.message || "No se pudo cargar la secuencia", "error");

    } finally {
 Swal.close();    }
  }

