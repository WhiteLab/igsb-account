/**
 * Created by dfitzgerald on 5/30/16.
 */
function setColor(pass, confirm, color) {
    pass.style.color = color;
    confirm.style.color = color;
}

window.onload = function() {
    var username = document.getElementById('account-username');
    username.focus();

    var passwordsMatch = false;
    var pass = document.getElementById('account-password');
    var passConfirm = document.getElementById('account-password-confirm');

    pass.onkeyup = function() {
        if (passConfirm.value.trim() == '') {
            pass.style.color = 'black';
            passwordsMatch = false;
            return;
        }
        if (pass.value == passConfirm.value) {
            setColor(pass, passConfirm, 'green');
            passwordsMatch = true;
        } else {
            setColor(pass, passConfirm, 'red');
            passwordsMatch = false;
        }
    };

    passConfirm.onkeyup = function() {
        if (pass.value == passConfirm.value) {
            setColor(pass, passConfirm, 'green');
            passwordsMatch = true;
        } else {
            setColor(pass, passConfirm, 'red');
            passwordsMatch = false;
        }
    };

    var accountForm = document.getElementById('account-form');
    accountForm.onsubmit = function() {
        if (!passwordsMatch || username.value.trim() == '') {
            alert('do not match');
            return false;
        } else {
            accountForm.submit();
        }
    };
};
