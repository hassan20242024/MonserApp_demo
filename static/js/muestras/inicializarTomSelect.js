
function inicializarTomSelect(selector) {
  const elemento = document.querySelector(selector);
  if (!elemento) return;

  if (elemento.tomselect) {
    elemento.tomselect.destroy();
  }

  const esMultiple = elemento.hasAttribute("multiple");
  const valorInicial = elemento.dataset.etapaSeleccionada;

  fetch('/lista_etapas/')
    .then(response => response.json())
    .then(data => {
      const ts = new TomSelect(selector, {
        theme: 'bootstrap5',
        placeholder: esMultiple ? 'Seleccione una o más etapas' : 'Seleccione una etapa',
        plugins: esMultiple ? ['remove_button'] : [],
        maxItems: esMultiple ? null : 1,
        valueField: 'id',
        labelField: 'etapa',
        searchField: 'etapa',
        options: data,
        onChange: function() {
          actualizarMasTexto(ts, elemento);
        },
      });

      // Si estamos editando, preseleccionamos el valor actual
      if (!esMultiple && valorInicial) {
        ts.setValue(valorInicial);
      }

      // Añadimos clase multiples para CSS
      if (esMultiple) {
        ts.control.classList.add('multiples');
      }

      // Inicializamos estado del + más...
      actualizarMasTexto(ts, elemento);
    })
    .catch(error => {
      console.error('Error cargando etapas:', error);
    });
}
