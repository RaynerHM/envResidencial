window.onload = function() {

    const myInput = document.getElementById('clave');
    const lengthC = document.getElementById('lengthCounter');
    const PSWlength = document.getElementById('PSWlength');
    const upper = document.getElementById('upper');
    const lower = document.getElementById('lower');
    const number = document.getElementById('number');
    const symbol = document.getElementById('symbol');
    const bClave = document.getElementById('bClave');
    clave2 = document.getElementById('pass-new1');

    const lengthCounter = (pass) => {
        const len = pass.length;
        lengthC.innerHTML = (`<b>Numero de Caracteres: ${len} </b>`);

    };

    const lengthValidator = (pass) => {
        if (pass.length >= 8) {
            PSWlength.classList.remove('invalid');
            PSWlength.classList.add('valid');
            bClave.classList.remove('disabled');
        } else {
            PSWlength.classList.remove('valid');
            PSWlength.classList.add('invalid');
            bClave.classList.add('disabled');
        }
    };

    const capitalValidator = (pass) => {
        const upperCaseLetters = /[A-Z]/g;
        if (pass.match(upperCaseLetters)) {
            upper.classList.remove('invalid');
            upper.classList.add('valid');
            bClave.classList.remove('disabled');
        } else {
            upper.classList.remove('valid');
            upper.classList.add('invalid');
            bClave.classList.add('disabled');
        }
    };

    const lowercaseValidator = (pass) => {
        const lowerCaseLetters = /[a-z]/g;
        if (pass.match(lowerCaseLetters)) {
            lower.classList.remove('invalid');
            lower.classList.add('valid');
            bClave.classList.remove('disabled');
        } else {
            lower.classList.remove('valid');
            lower.classList.add('invalid');
            bClave.classList.add('disabled');
        }
    };

    const numberValidator = (pass) => {
        const numbers = /[0-9]/g;
        if (pass.match(numbers)) {
            number.classList.remove('invalid');
            number.classList.add('valid');
            bClave.classList.remove('disabled');
        } else {
            number.classList.remove('valid');
            number.classList.add('invalid');
            bClave.classList.add('disabled');
        }
    };

    const symbolValidator = (pass) => {
        const symbols = /[$-/:-?{-~!"^@_`\[\]]/;
        if (pass.match(symbols)) {
            symbol.classList.remove('invalid');
            symbol.classList.add('valid');
            bClave.classList.remove('disabled');

        } else {
            symbol.classList.remove('valid');
            symbol.classList.add('invalid');
            bClave.classList.add('disabled');
        }
    };

    myInput.addEventListener('keyup', (event) => {

        const password = myInput.value;
        lengthCounter(password);
        lengthValidator(password);
        capitalValidator(password);
        lowercaseValidator(password);
        numberValidator(password);
        symbolValidator(password);

    }, false);

};

$(document).ready(function() {
    //variables
    var pass1 = $('[name=pass-new]');
    var pass2 = $('[name=rep-pass]');
    var negacion = "Las contraseñas no son iguales";
    var span = $('<div></div>').insertAfter(pass2);
    span.hide();

    function coincidePassword() {
        var valor1 = pass1.val();
        var valor2 = pass2.val();

        span.show().removeClass();
        if (valor1 != valor2) {
            span.text(negacion).addClass('mensaje-clave negacion');
        }
        if (valor1.length != 0 && valor1 == valor2) {
            span.addClass('hide');
        }
    }
    pass2.keyup(function() {
        coincidePassword();
    });
    pass1.focus();

    $('#bClave').click(function() {

        var token = $('input[name="csrfmiddlewaretoken"]').val()
        $.ajax({
            type: "POST",
            url: "/cambiarclaveAjax/",
            data: {
                'pass-new': $('#clave').val(),
                'csrfmiddlewaretoken': token,
            },

            success: function(data) {
                if (data.estado == 0) {
                    var contenido = {
                        'html': data.mensaje,
                        'classes': 'rounded red text-white',
                        'displayLength': 10000,
                        'outDuration': 5000,
                        'inDuration': 2000,
                    }
                    M.toast(contenido);
                } else if (data.estado == 1) {
                    var contenido = {
                        'html': data.mensaje,
                        'classes': 'rounded green accent-4 text-white',
                        'displayLength': 10000,
                        'outDuration': 5000,
                        'inDuration': 2000,
                    }
                    M.toast(contenido);
                }

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
});