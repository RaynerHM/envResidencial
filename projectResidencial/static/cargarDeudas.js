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

                    var asd = "<table id='ta' class='centered striped highlight'><thead><tr><th>Seleccione</th><th>Deuda Pendiente</th><th>Recargo</th><th>Fecha Limite</th><th>Concepto Deuda</th><th>Total</th></tr></thead><tbody id='tbody'>";
                    $('#nombre').after(asd);
                    for (var i = 0; i < data.deuda.length; i++) {
                        console.log(data.deuda.length);

                        $('#tbody').append(
                            "<tr id='tr'><td><p><input type='checkbox' class='micheckbox' id='" + data.deuda[i].id + "' value='" + data.deuda[i].id + "'/><label id='" + data.deuda[i].id + "' for=" + data.deuda[i].id + ">Seleccionar</label></p></td><td>RD$" + data.deuda[i].deuda_pendiente +
                            "</td><td>RD$" + data.deuda[i].recargo + "</td>" +
                            "</td><td>" + data.ajuste[0].fecha_Limite_Pago + "</td>" +
                            "</td><td>" + data.deuda[i].concepto_deuda + "</td>" +
                            "</td><td>RD$" + (parseInt(data.deuda[i].deuda_pendiente) + parseInt(data.deuda[i].recargo)) + "</td></tr>"
                        ).after("<div class='input-field center'><input class='btn' value='Guardar' type='submit' required></div>");
                    }

                    $(".micheckbox").change(function() {
                        //[type="checkbox"]+label
                        //var lab = $(input[type = 'checkbox']).value = $(this).val();
                        // console.log(lab);
                        var chec = $(this).val();
                        if (this.checked) {
                            // Desencadena aquí tu evento
                            // if (lab == chec) {
                            // }
                            this.after('Seleccionado');
                            alert("El checkbox con valor " + $(this).val() + " ha sido deseleccionado");

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

// $('.micheckbox').change()

// $(".micheckbox").on('change', function() {
//     if ($(this).is(':checked')) {
//         // Hacer algo si el checkbox ha sido seleccionado
//         alert("El checkbox con valor " + $(this).val() + " ha sido seleccionado");
//     } else {
//         // Hacer algo si el checkbox ha sido deseleccionado
//         alert("El checkbox con valor " + $(this).val() + " ha sido deseleccionado");
//     }
// });