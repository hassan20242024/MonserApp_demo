
let tabla;
function formatDetalle(p) {
  return `
    <div class="p-2">
      <strong>Fecha de ingreso:</strong> ${p.fecha_ingreso || 'N/A'}<br>
      <strong>Tipo de muestra:</strong> ${p.tipo_muestra || 'N/A'}<br>
      <strong>Observaciones:</strong> ${p.observaciones_muestras || 'N/A'}
    </div>
  `;
}

document.addEventListener('DOMContentLoaded', function () {
  const spinner = document.getElementById('spinner-carga');
  const contenido = document.getElementById('contenido-cargado');

tabla = new DataTable('#example3', {
  searching: true,
  paging: true,
  lengthChange: true,
  info: false,
  autoWidth: false,
  responsive: true,
  columnDefs: [
    {
      className: 'details-control',
      orderable: false,
      targets: 0
    },
    {
      targets: [1, 4, 8], // Oculta las columnas 
      visible: false,
   
    }
  ],
  order: [[1, 'desc']]
});

  spinner.classList.remove('d-none');
  contenido.classList.add('d-none');

  fetch('/muestras-json/')
    .then(response => response.json())
    .then(data => {
      data.data.forEach(p => {
        tabla.row.add([
          '', // celda del botón de expandir
          p.fecha_ingreso,
          p.nombre_muestra,
          p.lote_muestra,
          p.tipo_muestra,
          p.etapa,
          p.codigo_muestra_interno,
          p.codigo_muestra_producto,
          p.observaciones_muestras,
          `<a class="btn btn-primary btn-sm" href="/duplicar_muestras/${p.pk}" title="Guardar como">
             <i class="fa fa-clone" aria-hidden="true"></i>
           </a>
           <a class="btn btn-info btn-sm" href="/editar_muestras/${p.pk}" title="Editar">
             <i class="fas fa-pencil-alt"></i>
           </a>`
        ]).draw(false);
      });

      spinner.classList.add('d-none');
      contenido.classList.remove('d-none');
    })
    .catch(error => {
      console.error('Error cargando las muestras:', error);
      spinner.innerHTML = '<p class="text-danger">Error al cargar los datos.</p>';
    });

  // Expand/Collapse detalles
  $('#example3 tbody').on('click', 'td.details-control', function () {
    var tr = $(this).closest('tr');
    var row = tabla.row(tr);

    if (row.child.isShown()) {
      row.child.hide();
      tr.removeClass('shown');
    } else {
      const data = row.data();
      const index = row.index();
      const rawData = tabla.row(index).data(); // los datos crudos
      const item = {
        fecha_ingreso: rawData[1],
        tipo_muestra: rawData[4],
        observaciones_muestras: rawData[8]
      };
      row.child(formatDetalle(item)).show();
      tr.addClass('shown');
    }
  });


    // Abrir modal para ingresar muestra
    document.getElementById('openMuestraModal').addEventListener('click', function () {
      Swal.fire({
        title: 'Cargando...',
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading()
      });

      fetch("/ingresar_muestras/")
        .then(response => response.json())
        .then(data => {
          Swal.close();
          const modalContent = document.getElementById("modalMuestraContent");
          modalContent.innerHTML = data.html_form;

          inicializarTomSelect('#id_etapa');
          new bootstrap.Modal(document.getElementById("modalMuestra")).show();
          activarSubmitAjax();
        })
        .catch(error => {
          Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo cargar el formulario.' });
          console.error('Error al cargar el formulario:', error);
        });
    });

  });
