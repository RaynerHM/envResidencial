$(document).ready(function() {
    /*
                $("input:checkbox:checked").each(
                    function() {
                        alert("El checkbox con valor " + $(this).val() + " está seleccionado");
                    }
                );
    */
    $('select#no_apartamento').on('change', function() {
        var valores = $(this).val();
        $('#concepto').val('Prueba');
        var bloq = valores.split('-')[0];
        var apto = valores.split('-')[1];
        console.log(bloq);
        console.log(apto);

        $.ajax({
            type: "GET",
            url: "/ajax",
            data: {
                'bloq': bloq,
                'apto': apto
            },

            success: function(data) {
                //$('#concepto').val(data.residente[0].nombre);
                //console.log(data.deuda[0].deuda_pendiente);
                $('#tabla').addClass('hide');
                if (data.deuda.length > 0) {
                    $('#ta').remove('#ta');
                    $('#tabla').removeClass('hide');
                    $('.no-datos').addClass('hide');
                    $('#tabla').html("<div id='nombre'><p id='p'>" + data.residente[0].nombre + "</p></div>").after();

                    var asd = "<form action='' method='GET'><table id='ta' class='centered striped highlight'><thead><tr><th>Seleccione</th><th>Deuda Pendiente</th><th>Recargo</th><th>Fecha Limite</th><th>Concepto Deuda</th><th>Total</th></tr></thead><tbody id='tbody'>";
                    $('#nombre').after(asd);
                    for (var i = 0; i < data.deuda.length; i++) {
                        console.log(data.deuda.length);

                        $('#tbody').append(
                            "<tr id='tr'><td><p><label><input type='checkbox' class='micheckbox' id='" + data.deuda[i].id + "' value='" + data.deuda[i].id + "'/> <span id='s" + data.deuda[i].id + "'>Seleccionar</span><label></p></td><td>RD$" + data.deuda[i].deuda_pendiente + "</td><td>RD$" + data.deuda[i].recargo + "</td>" +
                            "</td><td>" + data.ajuste[0].fecha_Limite_Pago + "</td>" +
                            "</td><td>" + data.deuda[i].concepto_deuda + "</td>" +
                            "</td><td>RD$" + (parseInt(data.deuda[i].deuda_pendiente) + parseInt(data.deuda[i].recargo)) + "</td></tr>"
                        );
                    }
                    $('#ta').after("<div class='input-field center'><input class='btn' value='Guardar' type='submit' required></div></form>");

                    $(".micheckbox").change(function() {
                        var chec = $(this).val();
                        console.log('--------- ' + chec)
                        if (this.checked) {
                            $('#s' + chec).text('Seleccionado');
                        } else {
                            $('#s' + chec).text('Seleccionar');
                        }
                    });

                } else {
                    $('.no-datos').removeClass('hide').text(data.residente[0].nombre + ' no tiene deudas pendiente.');
                }


            },
            error: function(data) {
                $('#tabla').html('<p style="text-align:center;color:blue;">No se pueden obtener los datos solicitados.</p>').after();
                console.log('No se pueden obtener los datos solicitados.');
            }
        });
    });
});


$('#Guardar').click(function() {
    $.ajax({
        type: "GET",
        url: "/ajaxguardar",
        data: {
            'bloq': bloq,
            'apto': apto
        },

        success: function(data) {
            console.log('Bien.');

        },
        error: function(data) {
            console.log('No se pueden obtener los datos solicitados.');
        }
    });
});