function validateFormCreacion() {
  let x = document.forms["myFormCreacion"]["nombre"].value;
  if (x == "") {
    alert("Todos los campos son requeridos");
    return false;
  }
}


