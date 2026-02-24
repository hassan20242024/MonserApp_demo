function confirmar(event) {
    event.preventDefault();

    let form = document.getElementById('myModelForm');
    let formData = new FormData(form);

    // Validaciones
    const tipos = ['item', 'itemCelda', 'itemTest', 'itemMantenimiento', 'itemCalificacion'];
    let checksSeleccionados = tipos.map(tipo => Array.from(formData.getAll(tipo)));
    let totalChecks = checksSeleccionados.reduce((acc, arr) => acc + arr.length, 0);
    let tiposSeleccionados = checksSeleccionados.filter(arr => arr.length > 0).length;

    if (totalChecks === 0) {
    Swal.fire({
        icon: 'warning',
        title: 'Atención',
        text: 'Debe seleccionar al menos un registro.',
        confirmButtonText: 'Aceptar'
    });
    return;
}

    if (tiposSeleccionados > 1) {
    Swal.fire({
        icon: 'error',
        title: 'Actividad inválida',
        text: 'Debe seleccionar una sola clase de actividad.',
        confirmButtonText: 'Entendido'
    });
    return;
}

    Swal.fire({
        title: "¿Está seguro?",
        text: "Por favor, confirme la actualización de registros",
        icon: "question",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Confirmar"
    }).then((result) => {
        if (result.isConfirmed) {
           Swal.fire({
      title: "Cargando...",
      html: "Espere un momento por favor",
      allowOutsideClick: false,
      allowEscapeKey: false,
      showConfirmButton: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });
            fetch("/mantenimientos_buzos_Check_form/", {
                method: "POST",
                headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: "success",
                        title: "¡Éxito!",
                        text: data.message,
                        timer: 1500,
                        timerProgressBar: true,
                        showConfirmButton: false
                    });
                    // Aquí recargas la tabla
                    table.ajax.reload(null, false); // false para no resetear la paginación
                } else {
                    Swal.fire("Error", data.message || "Ocurrió un error", "error");
                }
            })
            .catch(error => {
                console.error("Error en el fetch:", error);
                Swal.close()
                Swal.fire("Error", "Hubo un error de red", "error");
            });
        }
    });
}
