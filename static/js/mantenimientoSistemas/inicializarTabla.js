
document.addEventListener('DOMContentLoaded', () => {
  // Inicializa DataTable y hazla accesible globalmente
  window.table = new DataTable("#myTable", {
    ajax: "/get_lavado_buzo_data/",
     pageLength: 25,
    columns: [
      { data: "sistema" },
      { data: "lavado_buzos", render: renderAll },
      { data: "lavado_celdas", render: renderAll },
      { data: "test_diagnostico", render: renderAll },
      { data: "mantenimiento", render: renderAll },
      { data: "calificacion", render: renderAll },
      { data: "editar" }
    ],
    columnDefs: [
      { targets: "_all", className: "text-center" }
    ],
    processing: true,
    deferRender: true,
    initComplete: function(settings, json) {
      const api = this.api();
      const hideEdit = json.data.length > 0 && !json.data[0].editar;
      api.column(6).visible(!hideEdit);
    }
  });

  // Función reutilizable para mostrar "No Aplica" si el <small> está vacío
  function renderAll(data) {
    const tmp = document.createElement('div');
    tmp.innerHTML = data || '';
    const small = tmp.querySelector('small');
    const text = small ? small.textContent.trim() : '';
     if (text === '') {
    return '<span style="color: purple;">No Aplica</span>';
  } else {
    return data;
  }
  }
});
