//const eliminar = document.querySelectorAll('.id_eliminar') 




document.querySelectorAll('.id_eliminar').forEach((btn) =>{
    btn.addEventListener("click", function (e) {
        e.preventDefault();
        Swal.fire({
            title:"¿Está seguro de invalidar esta secuencia?",
            showCancelButton:true,
            confirmButtonText:"Invalidar",
            confirmButtonColor:"#d33",
            backDrop:true,
            showLoaderOnConfirm:true,
            preConfirm: () => {
                location.href=e.target.href
            },
            allowOutsideClick:() => false,
            allowEscapeKey: () => false, 


        })
    })
})
   
