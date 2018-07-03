$('#username').focus();

$('select').material_select();

/*  ------------------------------------------ Menu SideNav ------------------------------------------*/
$(document).ready(function() {
    $('.deslizar').sideNav({
        menuWidth: 300,
        closeOnClick: true,
        draggable: true,
        onOpen: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is opened
        onClose: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is closed
    });
});


/* ------------------------------------------------------------------------------------------------ */
var myVar;

function myFunction() {
    myVar = setTimeout(showPage, 500);
}

function showPage() {
    document.getElementById("loader").style.display = "none";
    document.getElementById("myDiv").style.display = "block";
}


/*  ------------------------------------------ Menu SideNav ------------------------------------------*/
$('#nombre').focus();

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