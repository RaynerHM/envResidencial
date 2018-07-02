$(document).ready(function() {
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

        if (asd.length == 3) {
            asd = asd + "-";
            $('#cedula').val(asd);
        } else if (asd.length == 11) {
            asd = asd + "-";
            $('#cedula').val(asd);
        }
    });

});