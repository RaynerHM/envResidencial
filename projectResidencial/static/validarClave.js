window.onload = function() {

    const myInput = document.getElementById('clave');
    const lengthC = document.getElementById('lengthCounter');
    const PSWlength = document.getElementById('PSWlength');
    const upper = document.getElementById('upper');
    const lower = document.getElementById('lower');
    const number = document.getElementById('number');
    const symbol = document.getElementById('symbol');

    const lengthCounter = (pass) => {
        const len = pass.length;
        lengthC.innerHTML = (`<b>Numero de Caracteres: ${len} </b>`);

    };

    const lengthValidator = (pass) => {
        if (pass.length >= 8) {
            PSWlength.classList.remove('invalid');
            PSWlength.classList.add('valid');
        } else {
            PSWlength.classList.remove('valid');
            PSWlength.classList.add('invalid');
        }
    };

    const capitalValidator = (pass) => {
        const upperCaseLetters = /[A-Z]/g;
        if (pass.match(upperCaseLetters)) {
            upper.classList.remove('invalid');
            upper.classList.add('valid');
        } else {
            upper.classList.remove('valid');
            upper.classList.add('invalid');
        }
    };

    const lowercaseValidator = (pass) => {
        const lowerCaseLetters = /[a-z]/g;
        if (pass.match(lowerCaseLetters)) {
            lower.classList.remove('invalid');
            lower.classList.add('valid');
        } else {
            lower.classList.remove('valid');
            lower.classList.add('invalid');
        }
    };

    const numberValidator = (pass) => {
        const numbers = /[0-9]/g;
        if (pass.match(numbers)) {
            number.classList.remove('invalid');
            number.classList.add('valid');
        } else {
            number.classList.remove('valid');
            number.classList.add('invalid');
        }
    };

    const symbolValidator = (pass) => {
        const symbols = /[$-/:-?{-~!"^@_`\[\]]/;
        if (pass.match(symbols)) {
            symbol.classList.remove('invalid');
            symbol.classList.add('valid');
        } else {
            symbol.classList.remove('valid');
            symbol.classList.add('invalid');
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