$(document).ready(function() {
    $('.boton').on('click', function() {
        console.log($(this).val());
    });


    $('i.editar').click(function() {
        var id = $(this).attr('value');
        usuario1 = $('#datos-usuario1' + id);
        usuario2 = $('#datos-usuario2' + id);

        var nombre = $(usuario1).children().children().eq(0).text();
        var apellido = $(usuario1).children().children().eq(1).text();
        var apartamento = $(usuario2).children().eq(1).children().text();
        var edificio = $(usuario2).children().eq(2).children().text();
        var cedula = $(usuario2).children().eq(3).children().text();
        var telefono = $(usuario2).children().eq(4).children().text();
        var email = $(usuario2).children().eq(5).children().text();

        $('label').attr('for', 'apartamento').addClass('active')
        $('label').attr('for', 'edificio').addClass('active')
        $('label').attr('for', 'cedula').addClass('active')
        $('label').attr('for', 'telefono').addClass('active')
        $('label').attr('for', 'email').addClass('active')
        $('label').attr('for', 'nombre').addClass('active')

        $('input#apartamento').val(apartamento);
        $('input#edificio').val(edificio);
        $('input#cedula').val(cedula);
        $('input#telefono').val(telefono);
        $('input#correo').val(email);
        $('input#nombre').val(nombre.split('-')[0]);
        $('input#apellido').val(apellido);
    });
});