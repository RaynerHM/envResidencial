$(document).ready(function() {


    $('.opcion').click(function() {
        $('.opcion1').toggle('slow')
    });

    $('select').formSelect();

    $('.tooltip').tooltip({ delay: 50 });


    /*  ------------------------------------------ Menu SideNav ------------------------------------------*/

    $('.materialboxed').materialbox();


    $('.sidenav').sidenav({
        menuWidth: 350,
        closeOnClick: true,
        draggable: true,
        onOpen: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is opened
        onClose: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is closed
    });



    /*  ----------------------------------------- Inicial Modal -----------------------------------------*/

    $('.modal').modal({
        dismissible: false,
        onCloseEnd: function() {
            $('input[type=text]').val('');
            $('input[type=email]').val('');
        }
    });

    $('p.correo').animate(function() {

    });



    // $('p.correo').hover(function() {
    //     $(this).animate({ "right": '155px' }, 4000);
    // }, function() {
    //     $(this).animate({ "right": 0 }, 4000);
    // });

});