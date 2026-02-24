
function getBadgeClass(status) {
  switch (status) {
    case 'Revisada': return 'bg-danger text-white';
    case 'Impresa': return 'bg-warning text-dark';
    case 'Reportada': return 'bg-success text-white';
    case 'Auditada': return 'bg-primary text-white';
    case 'Ensayo': return 'bg-info text-dark';
    default: return 'bg-secondary text-white';
  }
}

function buildEstadoSpan(item) {
  const locked = item.status === 'Auditada';
  const lockIcon = locked ? ' 🔒' : '';
  return `
    <span class="estado-dinamico badge rounded-pill ${getBadgeClass(item.status)}"
          data-id="${item.id}" data-status="${item.status}">
      ${item.status}${lockIcon}
    </span>`;
}