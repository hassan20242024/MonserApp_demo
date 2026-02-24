
async function getDataAndRender() {
  try {
    const response = await fetch("./listado_secuencias_validadas");
    const data = await response.json();
    allData = data;
    filteredData = allData;
    renderTable(filteredData);
  } catch (error) {
    document.getElementById('tbody').innerHTML = `<tr><td colspan="8">Error cargando datos</td></tr>`;
    console.error(error);
  } finally {
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  }
}
