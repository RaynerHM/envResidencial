/*  ---------------- Formulario Registro de Nuevos Usuarios ----------------*/
$(document).ready(function() {

    $('#nombre').focus();

    $("#telefono").keydown(function() {
        var asd = $(this).val();

        if (asd.length == 3) {
            asd = asd + "-";
            $('#telefono').val(asd);
        } else if (asd.length == 7) {
            asd = asd + "-";
            $('#telefono').val(asd);
        }
    });

    $("#cedula").keydown(function() {
        var asd = $(this).val();

        if (asd.length <= 13) {

            if (asd.length == 3) {
                asd = asd + "-";
                $('#cedula').val(asd);
            } else if (asd.length == 11) {
                asd = asd + "-";
                $('#cedula').val(asd);
            }
        } else {
            this.value = this.value.slice(0, 12);
        }
    });
});