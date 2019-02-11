$(document).ready(function() {

    $('#idEnviar').on('click', function() {

        var user_id = $('#user_id').val()
        var titulo = $('#titulo').val()
        var sugerencia = $('#textarea1').val()
        var token = $('input[name="csrfmiddlewaretoken"]').val()

        console.log('Token', token)
        console.log('ID Usuario', user_id)
        console.log('Titulo', titulo)
        console.log('Sugerencia', sugerencia)

        $.ajax({
            type: "POST",
            url: "/sugerencias_ajax/",
            data: {
                'user_id': user_id,
                'titulo': titulo,
                'sugerencia': sugerencia,
                'csrfmiddlewaretoken': token,
            },

            success: function(data) {
                $("#cerrar").trigger("click");
                $('.sidenav').sidenav('close');

                var contenido = {
                    'html': data.mensaje,
                    'classes': 'rounded green accent-4 text-white',
                    'displayLength': 10000,
                    'outDuration': 5000,
                    'inDuration': 2000,
                }
                M.toast(contenido);
            },

            error: function(data) {
                var contenido = {
                    'html': '<span>' + data.mensaje + '</span>',
                    'classes': 'rounded red text-white',
                    'displayLength': 10000,
                    'outDuration': 5000,
                    'inDuration': 2000,
                }
                M.toast(contenido);
            }
        });
    });
});