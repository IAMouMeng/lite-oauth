function vaildCheck() {
    let username = $('#username').val();
    let password = $('#password').val();
    let isValid = true;

    if (username === '' || !isValidEmail(username)) {
        $('#username').addClass('error-border');
        layer.msg(username === '' ? '请输入邮箱地址' : '请输入合法的邮箱地址');
        isValid = false;
    } else {
        $('#username').removeClass('error-border');
    }

    if (password === '') {
        $('#password').addClass('error-border');
        isValid = false;
    } else {
        $('#password').removeClass('error-border');
    }

    return isValid;
}

function isValidEmail(email) {
    return /\S+@\S+\.\S+/.test(email);
}

