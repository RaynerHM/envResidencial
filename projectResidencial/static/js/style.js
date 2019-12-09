$(document).ready(function() {

    $('.opcion').click(function() {
        $('.opcion1').toggle('slow')
    });

    $('select').formSelect();

    $('#username').focus();
    $('.tooltipped').tooltip({ delay: 50 });

    /*  --------------------------------------- Menu SideNav ---------------------------------------*/
    $('.sidenav').sidenav({
        menuWidth: 350,
        closeOnClick: true,
        draggable: true,
        onOpen: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is opened
        onClose: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is closed
    });


    /*  -------------------------------------- Inicial Modal --------------------------------------*/
    $('.modal').modal({
        dismissible: false,
    });

    $('#nombre').focus();

    /*  ------------------------- Formulario Registro de Nuevos Usuarios -------------------------*/
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