
  async function duplicarSecuenciaMuestras(secuenciaId) {
  try {
    Swal.fire({ title: "Cargando...", allowOutsideClick: false, didOpen: () => Swal.showLoading() });
    
    const res = await fetch(`/editar_secuencia/${secuenciaId}/`);
    if (!res.ok) throw new Error("No se pudo cargar la secuencia");
    const data = await res.json();

    const mRes = await fetch(`/ajax/muestras/${data.protocolo_proceso || data.metodo}/`);
    const mData = await mRes.json();
    const muestras = mData.muestras || [];
    
    Swal.close();

    const { value: seleccionadas } = await Swal.fire({
      title: "Agregar Muestra(s)",
      html: `
        <label style="font-weight: bold;">Seleccione nuevas muestras:</label>
        <select id="duplicarMuestras" multiple style="width:100%; min-height:180px;"></select>
      `,
      didOpen: () => {
        const select = document.getElementById("duplicarMuestras");
        muestras.forEach(m => {
          if (m.id != data.muestras) {
            const option = new Option(m.nombre, m.id);
            select.appendChild(option);
          }
        });
        new TomSelect(select, {
          plugins: ['remove_button'],
          dropdownParent: 'body',
          maxItems: null,
          closeAfterSelect: true,
          placeholder: "Seleccione una o más muestras"
        });
        const style = document.createElement('style');
  style.innerHTML = `
    .ts-dropdown {
      z-index: 999999 !important;
    }
  `;
  document.head.appendChild(style);
      },
      preConfirm: () => {
        const val = document.getElementById("duplicarMuestras").tomselect.getValue();
        if (!val || val.length === 0) {
          Swal.showValidationMessage("Debe seleccionar al menos una muestra");
          return false;
        }
        return val;
      },
      showCancelButton: true,
      confirmButtonText: "Agregar",
      cancelButtonText: "Cancelar",
      width: '800px'
    });

    if (!seleccionadas) return;

    document.getElementById('spinner-carga').classList.remove('d-none');
    const resDup = await fetch(`/duplicar_secuencia_muestras/${secuenciaId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({ muestras: seleccionadas })
    });

    const result = await resDup.json();
    document.getElementById('spinner-carga').classList.add('d-none');

    if (!resDup.ok) throw new Error(result.message || "Error al duplicar muestras");

    Swal.fire("¡Éxito!", result.message, "success");

    if (result.secuencias?.length) {
  result.secuencias.forEach(secuencia => {
    // Elimina fila anterior si ya existía (por ID)
    const existingRow = document.querySelector(`tr td[data-id='${secuencia.id}']`)?.closest("tr");
    if (existingRow) existingRow.remove();

    // Opcional: actualiza tu array de datos si usas uno
    datosSecuencias.push(secuencia);

    // Agrega fila nueva
    addRowToTable(secuencia);
  });
}
  } catch (err) {
    console.error(err);
    Swal.fire("Error", err.message || "Fallo al duplicar", "error");
  }
}

