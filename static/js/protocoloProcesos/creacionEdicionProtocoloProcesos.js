  document.addEventListener('DOMContentLoaded', function () {
    const spinner = document.getElementById('spinner');
    if (spinner) spinner.style.display = 'none';

    const form = document.getElementById('formProtocoloProceso');
    if (!form) {
      console.error("⚠️ No se encontró el formulario con id 'formProtocoloProceso'");
      return;
    }


  // Inicializar TomSelect
function limitItemsDisplay(ts) {
  const updateDisplay = () => {
    const items = ts.control.querySelectorAll('.item');
    items.forEach((item, index) => {
      if (index < 3) {
        item.style.display = '';
      } else {
        item.style.display = 'none';
      }
    });

    // Quitar indicador anterior si existe
    const oldIndicator = ts.control.querySelector('.more-indicator');
    if (oldIndicator) oldIndicator.remove();

    const extra = items.length - 3;
    if (extra > 0) {
      const indicator = document.createElement('div');
      indicator.className = 'item more-indicator disabled';
      indicator.textContent = `+${extra} más`;
      ts.control.insertBefore(indicator, ts.control.querySelector('.ts-control-input'));
    }
  };

  ts.on('change', updateDisplay);
  ts.on('item_remove', updateDisplay);
  ts.on('item_add', updateDisplay);
  ts.on('initialize', updateDisplay);
  updateDisplay();
}

  tsParametro = new TomSelect("#id_ensayos", {
    plugins: ['remove_button'],
    placeholder: "Seleccione parámetros",
    maxOptions: null,
    closeAfterSelect: false,
    onInitialize: function () {
      limitItemsDisplay(this);
    },
    onItemAdd: function () {
      this.open();
      this.focus();
    }
  });
  

  tsMuestras = new TomSelect("#id_muestras", {
    plugins: ['remove_button'],
    placeholder: "Seleccione muestras o placebos",
    maxOptions: null,
    closeAfterSelect: false,
    onInitialize: function () {
      limitItemsDisplay(this);
    },
    onItemAdd: function () {
      this.open();
      this.focus();
    }
  });

  // FORM SUBMIT
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
    if (spinner) spinner.style.display = 'block';

    fetch(form.action, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: formData
    })
    .then(response => {
      if (!response.ok) return response.json().then(err => Promise.reject(err));
      return response.json();
    })
    .then(data => {
      if (spinner) spinner.style.display = 'none';

     // Guardar el mensaje en sessionStorage
sessionStorage.setItem('protocoloSuccess', data.message);

// Redirigir
window.location.href = '/protocolo_proceso/?skipSpinner=1';


    })
    .catch(error => {
      if (spinner) spinner.style.display = 'none';

      let mensajes = '';
      if (error.errors) {
        const errores = JSON.parse(error.errors);
        for (let campo in errores) {
          errores[campo].forEach(e => {
            mensajes += `${campo}: ${e.message}\n`;
          });
        }
      }

      Swal.fire({
        icon: 'error',
        title: 'Error al guardar',
        text: mensajes || 'Ocurrió un error al guardar el protocolo.'
      });

      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  });
});


//Mostrar Spiner Al cargar inicialmente la plantilla

  document.addEventListener("DOMContentLoaded", () => {
    const spinner = document.getElementById("spinner-carga");
    const contenido = document.getElementById("contenido-cargado");

    if (spinner) {
      spinner.classList.remove("d-none");
    }

    // Esperar al menos 500ms antes de mostrar contenido
    window.addEventListener("load", () => {
      setTimeout(() => {
        if (spinner) spinner.classList.add("d-none");
        if (contenido) contenido.classList.remove("d-none");
      }, 500); // Ajusta el tiempo si deseas mostrar más tiempo el spinner
    });
  });

