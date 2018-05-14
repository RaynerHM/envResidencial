window.onload = function() {

    const myInput = document.getElementById('clave');
    const lengthC = document.getElementById('lengthCounter');
    const PSWlength = document.getElementById('PSWlength');
    const upper = document.getElementById('upper');
    const lower = document.getElementById('lower');
    const number = document.getElementById('number');
    const symbol = document.getElementById('symbol');
    const bClave = document.getElementById('bClave');

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