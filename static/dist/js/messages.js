const btnsEliminacion = document.querySelectorAll(" .errorAlert");

(function () {
    btnsEliminacion.forEach(btn => {
        btn.addEvntListener("click", function(e){
            let confirmacion = confirm("Confirmar el guardado?");
            if (!confirmacion) {
                e.preventDefault();
                Swal.fire({
                    title: "Excelente!",
                    text: "Guardado exitoso",
                    icon: "success",
                    
                  });
            }
        })
    })
}
    )