let registrForm = document.querySelector('.registr'),
    errorMsg = document.getElementById('msg'),
    errorMsgPassword = document.getElementById('msg_password'),
    inputName = document.querySelector('.js-input-name'),
    inputPassword1 = document.querySelector('.js-input-password1'),
    inputPassword2 = document.querySelector('.js-input-password2'),
    errorMsgName = document.getElementById('msg_name')


registrForm.onsubmit = function () {
    let password1Value = inputPassword1.value,
        password2Value = inputPassword2.value,
        inputNameValue = inputName.value


    if (inputNameValue.length < 7) {
        inputName.classList.add('error');
        errorMsgName.classList.add('error_msg')
        return false
    } else if (password1Value !== password2Value || password1Value.length < 8) {
        inputName.classList.remove('error');
        errorMsgName.classList.remove('error_msg')
        inputPassword1.classList.add('error');
        inputPassword2.classList.add('error');
        errorMsg.classList.add('error_msg');
        return false
    } else if (password1Value === password2Value && (/(?=.*[0-9])(?=.*[a-z])[0-9a-zA-Z!@#$%^&*]{8,}/g.test(password1Value) === false)) {
        inputName.classList.remove('error');
        errorMsgName.classList.remove('error_msg')
        inputPassword1.classList.remove('error');
        inputPassword2.classList.remove('error');
        errorMsg.classList.remove('error_msg');
        errorMsgPassword.classList.add('error_msg');
        inputPassword1.classList.add('error');
        return false
    }


}