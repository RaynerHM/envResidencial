// $(document).ready(function() {
//     $('select#no_apartamento')
// })



// $('select#select').on('change', function () {
//     var valor = $(this).val();
//     var v_27f = "Av. 27 de Febrero #452, Mirador Norte, Sto. Domingo, República Dominicana."
//     var v_meg = "Megacentro, Pasillo La Fauna, 1er nivel, local 46A, Sto. Domingo, República Dominicana."
//     var v_rom = "Av. Rómulo Betancourt No. 2154, Renacimiento, Sto. Domingo, República Dominicana."

//     if (valor == "27 de Febrero") {
//         $('#fdireccion').removeClass('hide');
//         $("#sdireccion").html(v_27f);
//     }
//     else if (valor == "Rómulo Betancourt") {
//         $('#fdireccion').removeClass('hide');
//         $("#sdireccion").html(v_rom);
//     }
//     else if (valor == "Megacentro") {
//         $('#fdireccion').removeClass('hide');
//         $("#sdireccion").html(v_meg);
//     }
//     else {
//         $('#fdireccion').addClass('hide');
//     }
// });

// $('select#no_apartamento').on('change', function() {
//     var valor = $(this).val();

//     $.ajax({
//         url: $(this).attr('action'),
//         type: $(this).attr('method'),
//         data: $(this).Ajax(),

//         success: function(json) {
//             console.log(json)
//         }

//     });

// });





// $('.likebutton').click(function(){
//     var catid;
//     catid = $(this).attr("data-catid");
//     $.ajax({
        
//         type: "GET",
//         url: "/likepost",
//         data:{
//                 post_id: catid
//             },

//     success: function( data )
//     {
//         $('#like' + catid).remove();
//         $( '#message' ).text(data);
//     }
//     })
// });
