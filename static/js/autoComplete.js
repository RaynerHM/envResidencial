$(document).ready(function() {
    var token = $('input[name="csrfmiddlewaretoken"]').val()

    $.ajax({
        type: "POST",
        url: "/CargarNombresAjax/",
        data: {
            'csrfmiddlewaretoken': token,
        },

        success: function(data) {

            // $('#no_apartamento').on('focus', function() {
            //var remitente = $(this).val();

            // $('input.autocomplete').autocomplete({
            console.log(data);
            $('input#no_apartamento').autocomplete({
                data: data,
                // limit: 4,
                onAutocomplete: function(val) {

                    // if (val != "") {
                    //     $('#departamento').val(data.nombre[val]);
                    // } else {
                    //     alert('Error.');
                    // }
                },
            });
            // });
        },
        error: function(data) {
            console.log('No se pudo obtener los datos solicitados.');
        }
    });
});