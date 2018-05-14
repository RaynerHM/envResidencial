/*  ------------------------------------------ Menu SideNav ------------------------------------------*/
$('.deslizar').sideNav({
    menuWidth: 300,
    closeOnClick: true,
    draggable: true,
    onOpen: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is opened
    onClose: function(el) { /* Do Stuff */ }, // A function to be called when sideNav is closed
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
$(".dropdown-trigger").dropdown();



$(document).ready(function() {
    var pass1 = $('[name=pass-new]');
    var pass2 = $('[name=rep-pass]');

    if (pass1 != pass2) {
        $("#mensaje").removeClass("red");
        $("#mensaje").addClass("green accent-4");
    } else {
        $("#mensaje").removeClass("green accent-4");
        $("#mensaje").addClass("red");
    }
});