

  window.addEventListener('pageshow', function (event) {
    const isBackOrForward = event.persisted || (performance.getEntriesByType('navigation')[0]?.type === 'back_forward');
    if (isBackOrForward && Swal.isVisible()) {
      Swal.close();
    }
  });

  // Mostrar Swal antes de redirigir
  function mostrarSwalYRedirigir(href) {
    Swal.fire({
      title: 'Cargando...',
      text: 'Espere un momento por favor',
      allowOutsideClick: false,
      allowEscapeKey: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });

    setTimeout(() => {
      window.location.href = href;
    }, 300);
  }

  document.addEventListener('DOMContentLoaded', function () {
    // ✅ Botón de nuevo protocolo (ya en el DOM)
    const btnNuevo = document.getElementById('btn-nuevo-protocolo-proceso');
    if (btnNuevo) {
      btnNuevo.addEventListener('click', function (e) {
        e.preventDefault();
        mostrarSwalYRedirigir(this.href);
      });
    }

    // ✅ Delegar eventos en tabla para botones que se generan dinámicamente
    document.addEventListener('click', function (e) {
      const btnEditar = e.target.closest('.btn-editar-protocolo-proceso');
      if (btnEditar) {
        e.preventDefault();
        mostrarSwalYRedirigir(btnEditar.href);
      }
    });

            document.addEventListener('click', function (e) {
      const btnEditar = e.target.closest('.btn-crear-protocolo-proceso-sidebar');
      if (btnEditar) {
        e.preventDefault();
        mostrarSwalYRedirigir(btnEditar.href);
      }
    });

  });
