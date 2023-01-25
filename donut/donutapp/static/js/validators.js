let resetForm = document.querySelector('.confirmForm'),
    resetInputPassword1 = document.querySelector('#id_new_password1'),
    resetIPassword2 = document.querySelector('#id_new_password2'),
    errorMsg = document.getElementById('msg'),
    errorMsgPassword = document.getElementById('msg_password'),
    registrForm = document.querySelector('.registr'),
    inputName = document.querySelector('.js-input-name'),
    inputPassword1 = document.querySelector('.js-input-password1'),
    inputPassword2 = document.querySelector('.js-input-password2'),
    errorMsgName = document.getElementById('msg_name')


resetForm.onsubmit = function () {
    let password12Value = resetInputPassword1.value,
        password22Value = resetIPassword2.value

    if (password12Value !== password22Value || password12Value.length < 8) {
        resetInputPassword1.classList.add('error');
        resetIPassword2.classList.add('error');
        errorMsg.classList.add('error_msg');
        return false
    } else if (password12Value === password22Value && (/(?=.*[0-9])(?=.*[a-z])[0-9a-zA-Z!@#$%^&*]{8,}/g.test(password12Value) === false)) {
        resetInputPassword1.classList.remove('error');
        resetInputPassword1.classList.remove('error');
        errorMsg.classList.remove('error_msg');
        errorMsgPassword.classList.add('error_msg');
        resetInputPassword1.classList.add('error');
        return false
    }

}
