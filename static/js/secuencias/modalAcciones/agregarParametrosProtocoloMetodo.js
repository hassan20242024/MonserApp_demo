
async function duplicarSecuenciaMetodo(secuenciaId) {
  try {
     // Mostrar spinner de carga inicial
    Swal.fire({
      title: "Cargando datos...",
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => Swal.showLoading()
    });
    const res = await fetch(`/editar_secuencia/${secuenciaId}/`);
    if (!res.ok) throw new Error("No se pudo cargar la secuencia");
    const data = await res.json();

    const pRes = await fetch(`/ajax/parametros/${data.protocolo}/`);
    const pData = await pRes.json();
    const parametros = pData.parametros;
    // Cerrar el spinner de carga
    Swal.close();

    const { value: formConfirmed } = await Swal.fire({
      title: "Agregar Parámetros",
      html: `
        <label style="display:block; font-weight:bold; margin-bottom:6px;">Seleccione nuevos parámetros:</label>
        <select id="parametrosDuplicados" multiple style="width:100%; min-height:180px;"></select>
      `,
      didOpen: () => {
        const select = document.getElementById("parametrosDuplicados");
        parametros.forEach(p => {
          if (p.id != data.parametro_sq) {
            const option = new Option(p.nombre, p.id);
            select.appendChild(option);
          }
        });

        // Inicializar TomSelect con dropdownParent: 'body'
        window.tsDuplicar = new TomSelect(select, {
          plugins: ['remove_button'],
          placeholder: "Seleccione uno o más parámetros",
          maxItems: null,
          closeAfterSelect: true,
          dropdownParent: 'body',
        });

        // Aseguramos que el dropdown tenga z-index alto con CSS dinámico
        const style = document.createElement('style');
        style.innerHTML = `
          .ts-dropdown {
            z-index: 999999 !important;
          }
        `;
        document.head.appendChild(style);
      },
      preConfirm: () => {
        const seleccionados = document.getElementById("parametrosDuplicados").tomselect.getValue();
        if (!seleccionados || seleccionados.length === 0) {
          Swal.showValidationMessage("Debe seleccionar al menos un parámetro");
          return false;
        }
        return seleccionados;
      },
      showCancelButton: true,
      confirmButtonText: "Agregar",
      cancelButtonText: "Cancelar",
      width: '900px',
      // para más altura si quieres
      // heightAuto: false,
      // customClass: { popup: 'my-swal-custom-height' }
    });

    if (!formConfirmed) return;
    // Spinner mientras se guarda
   document.getElementById('spinner-carga').classList.remove('d-none'); // mostrar
    const resDup = await fetch(`/duplicar_secuencia_parametro/${secuenciaId}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify({
        parametros: formConfirmed
      })
    });

    const dupData = await resDup.json();
     document.getElementById('spinner-carga').classList.add('d-none');    // ocultar
    if (!resDup.ok) throw new Error(dupData.message || "Error duplicando");

    Swal.fire("¡Éxito!", dupData.message, "success");

    if (dupData.secuencias?.length) {
  dupData.secuencias.forEach(secuencia => {
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
    console.error("Error duplicando:", err);
    Swal.fire("Error", err.message || "No se pudo duplicar la secuencia", "error");
  }
}
