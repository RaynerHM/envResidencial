$(document).ready(function() {
    // $('select#no_apartamento').on('change', function() {
    var deudas = []
    $('#buscar_deuda').on('click', function() {
        var valor = $('#no_apartamento').val();
        if (valor == null || valor.length == 0 || /^\s+$/.test(valor)) {
            return false;
        }

        var bloq = valor.split('-')[0];
        var apto = valor.split('-')[1];
        var token = $('input[name="csrfmiddlewaretoken"]').val()

        $.ajax({
            type: "POST",
            url: "/ajaxbuscardeuda/",
            data: {
                'bloq': bloq,
                'apto': apto,
                'csrfmiddlewaretoken': token,
            },

            success: function(data) {
                $('#tabla').addClass('hide');
                if (data.deuda.length > 0) {
                    $('#ta').remove('#ta');
                    $('#tabla').removeClass('hide');
                    $('.no-datos').addClass('hide');
                    $('#nombre').html("<h4>" + data.residente[0].nombre + "</h4>");
                    $('#tabla').html("<div id='qw'><p id='p'>" + data.residente[0].nombre + "</p></div>").after();

                    var asd = ("<table id='ta' class='centered striped highlight'><thead><tr><th style='width:190px;'>Seleccione</th><th style='width:150px;'>Deuda Pendiente</th><th style='width:130px;'>Recargo</th><th style='width:150px;'>Fecha Limite</th><th style='width:300px;'>Concepto Deuda</th><th style='width:130px;'>Total</th></tr></thead><tbody id='tbody'>");
                    $('#qw').after(asd);
                    for (var i = 0; i < data.deuda.length; i++) {
                        $('#tbody').append(
                            ("<tr id='tr" + data.deuda[i].id + "'><td><p><label><input type='checkbox' class='micheckbox' id='" + data.deuda[i].id + "' value='" + data.deuda[i].id + "'/> <span id='s" + data.deuda[i].id + "'>Seleccionar</span><label></p></td><td>RD$" + data.deuda[i].deuda_pendiente + "</td><td>RD$" + data.deuda[i].recargo + "</td>" +
                                "</td><td>" + data.ajuste[0].fecha_Limite_Pago + "</td>" +
                                "</td><td>" + data.deuda[i].concepto_deuda + "</td>" +
                                "</td><td>RD$" + (parseInt(data.deuda[i].deuda_pendiente) + parseInt(data.deuda[i].recargo)) + "</td></tr>")
                        );
                    }
                    $('#ta').after("<div class='input-field center'><input id='guardarDeuda' class='btn' value='Guardar' type='submit' required></div>");

                    deudas.splice(0);
                    $(".micheckbox").change(function() {
                        var chec = $(this).val();
                        if (this.checked) {
                            $('#s' + chec).text('Seleccionado');
                            $('#tr' + chec).addClass('seleccionado');

                            if (!deudas.includes(chec)) {
                                deudas.push(chec);
                            }
                        } else {
                            $('#s' + chec).text('Seleccionar');
                            $('#tr' + chec).removeClass('seleccionado');
                        }
                    });


                    $('#guardarDeuda').click(function() {

                        $.ajax({
                            type: "POST",
                            url: "/ajaxguardar/",
                            data: {
                                'deudas': deudas.toString(),
                                'csrfmiddlewaretoken': token,
                            },

                            success: function(data) {
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
                                    'html': '<span>No se pueden guardar los datos.</span>',
                                    'classes': 'rounded red text-white',
                                    'displayLength': 10000,
                                    'outDuration': 5000,
                                    'inDuration': 2000,
                                }
                                M.toast(contenido);
                            }
                        });
                    });


                } else {
                    $('#nombre').html("<h4>" + data.residente[0].nombre + "</h4>");
                    $('.no-datos').removeClass('hide').text(data.residente[0].nombre + ' no tiene deudas pendiente.');
                }
            },

            error: function(data) {
                $('#tabla').html('<p style="text-align:center;color:blue;">No se pueden obtener los datos solicitados.</p>').after();
                var contenido = {
                    'html': '<span>No se pueden obtener los datos solicitados.</span>',
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