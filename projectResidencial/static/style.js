$('#username').focus();

$('#nombre').focus();


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




// document.addEventListener('DOMContentLoaded', function () {
//     var elems = document.querySelectorAll('select');
//     var instances = M.FormSelect.init(elems, options);
// });

// Or with jQuery