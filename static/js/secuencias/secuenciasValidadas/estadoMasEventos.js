
function attachEstadoEvents() {
  // Obtener referencias a los checkboxes
  const chkImpresa = document.getElementById('chkImpresa');
  const chkReportada = document.getElementById('chkReportada');
  const chkAuditada = document.getElementById('chkAuditada');

  document.querySelectorAll('.estado-dinamico').forEach(el => {
    if (el.id === 'modalStatus') return;

    el.addEventListener('click', async function () {
      const id = this.dataset.id;
      const currentStatus = this.dataset.status;

      const userIsAdmin = USER_ROLE === 'Administrador';

      // Bloquear clic si el estado es Auditada y el usuario no es admin
      if (currentStatus === 'Auditada' && !userIsAdmin) {
        Swal.fire({
          icon: 'error',
          title: '🔒 Estado bloqueado',
          text: 'Este registro ya fue auditado y no puede ser modificado.',
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#dc3545',
        });
        return;
      }

      // --- NUEVO: validar checkboxes para rol Analista ---
      if (USER_ROLE === 'Analista') {
        // Solo permitir click si el checkbox correspondiente está activado para ese estado
        if (currentStatus === 'Revisada') {
          if (!chkImpresa.checked) {
            Swal.fire({
              icon: 'warning',
              title: '⚠️ Acción bloqueada',
              text: 'Para cambiar a Impresa debe activar el checkbox "Impresa".',
              confirmButtonText: 'OK',
              confirmButtonColor: '#ffc107', // amarillo
            });
            return;
          }
        } else if (currentStatus === 'Impresa') {
          if (!chkReportada.checked) {
            Swal.fire({
              icon: 'warning',
              title: '⚠️ Acción bloqueada',
              text: 'Para cambiar a Reportada debe activar el checkbox "Reportada".',
              confirmButtonText: 'OK',
              confirmButtonColor: '#fd7e14', // naranja
            });
            return;
          }
        } else if (currentStatus === 'Reportada') {
          if (!chkAuditada.checked) {
            Swal.fire({
              icon: 'warning',
              title: '⚠️ Acción bloqueada',
              text: 'Para cambiar a Auditada debe activar el checkbox "Auditada".',
              confirmButtonText: 'OK',
              confirmButtonColor: '#dc3545', // rojo
            });
            return;
          }
        }
        
      } else if (USER_ROLE === 'Auditor') {
    if (currentStatus === 'Reportada' && !chkAuditada.checked) {
    Swal.fire({
      icon: 'warning',
      title: '⚠️ Acción bloqueada',
      text: 'Para auditar, primero debe marcar el checkbox "Auditada".',
      confirmButtonText: 'OK',
      confirmButtonColor: '#0d6efd',
    });
    return;
  }
  }

      let newStatus = null;
      let endpoint = null;

      if (USER_ROLE === 'Analista') {
        if (currentStatus === 'Revisada') {
          newStatus = 'Impresa';
          endpoint = '/cambiar_estado_impresa/';
        } else if (currentStatus === 'Impresa') {
          newStatus = 'Reportada';
          endpoint = '/cambiar_estado_reportar/';
        }
      } else if (USER_ROLE === 'Auditor') {
        if (currentStatus === 'Reportada') {
          newStatus = 'Auditada';
          endpoint = '/cambiar_estado_auditada/';
        }
      } else if (USER_ROLE === 'Administrador') {
        if (currentStatus === 'Auditada') {
          newStatus = 'Reportada';
          endpoint = '/revertir_estado_a_reportada/';
        } else if (currentStatus === 'Reportada') {
          newStatus = 'Impresa';
          endpoint = '/revertir_estado_a_impresa/';
        } else if (currentStatus === 'Impresa') {
          newStatus = 'Revisada';
          endpoint = '/revertir_estado_a_revisada/';
        } else if (currentStatus === 'Revisada') {
          newStatus = 'Registrada';
          endpoint = '/revertir_estado_a_registrada/';
        }
      }

      if (!newStatus || !endpoint) {
        Swal.fire({
          toast: true,
          position: 'top-end',
          icon: 'error',
          title: '🔒 Acción no permitida',
          text: 'Tu rol no tiene permiso para cambiar este estado.',
          showConfirmButton: false,
          timer: 4000,
          timerProgressBar: true,
        });
        return;
      }

      this.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Actualizando...`;

      try {
        const res = await fetch(endpoint, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
          },
          body: JSON.stringify({ ids: [id], status: newStatus })
        });

        const data = await res.json();
        if (data.success) {
          if (newStatus === 'Registrada') {
            // Eliminar la fila si el estado cambia a Registrada
            this.closest('tr').remove();
          } else {
            this.className = `estado-dinamico badge rounded-pill ${getBadgeClass(newStatus)}`;
            this.dataset.status = newStatus;
            this.innerHTML = newStatus === 'Auditada' ? `${newStatus} 🔒` : newStatus;
          }
        } else {
          this.innerHTML = '❌ Error';
        }
      } catch (err) {
        console.error(err);
        this.innerHTML = '❌ Error';
      }
    });
  });
}
//Para permitir una sola marcación de checkbox a la vez
  document.querySelectorAll('.estado-checkboxes input[type="checkbox"]').forEach(checkbox => {
    checkbox.addEventListener('change', function () {
      if (this.checked) {
        // Desmarca todos los demás
        document.querySelectorAll('.estado-checkboxes input[type="checkbox"]').forEach(cb => {
          if (cb !== this) cb.checked = false;
        });
      }
    });
  });
