"use strict";
const MIN_LENGTH = 0;
const FORBIDDEN_CHARS = ";";


let passwordInput = $("#password-input");
let usernameInput = $("#username-input");
let signUpButton = $("#sign-up-button");


function isUsernameValid(username) {
    for (let i = 0; i < username.length; i++) {
        if (FORBIDDEN_CHARS.includes(username[i])) {
            return false;
        }
    }
    return username.length > MIN_LENGTH;
}


function isPasswordValid(password) {
    return password.length > MIN_LENGTH;
}


function isInputValid() {
    let username = usernameInput.val();
    let password = passwordInput.val();
    let usernameValid = isUsernameValid(username);
    let passwordValid = isPasswordValid(password);
    return usernameValid && passwordValid
}


function updateButton() {
    if (isInputValid()) {
        signUpButton.removeAttr("disabled");
    } else {
        signUpButton.attr("disabled", "disabled");
    }
}


usernameInput.on("input", updateButton);
passwordInput.on("input", updateButton);