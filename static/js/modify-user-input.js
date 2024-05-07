"use strict";
const FORBIDDEN_CHARS = ";";
const MIN_LENGTH = 0;


let saveChangesButton = $("#save-changes");
let usernameInput = $("#username-input");


function isUsernameValid(username) {
    for (let i = 0; i < username.length; i++) {
        if (FORBIDDEN_CHARS.includes(username[i])) {
            return false;
        }
    }
    return username.length > MIN_LENGTH;
}


function updateSaveChangesButton() {
    if (isUsernameValid(usernameInput.val())) {
        saveChangesButton.removeAttr("disabled");
    } else {
        saveChangesButton.attr("disabled", "disabled");
    }
}


usernameInput.on("input", updateSaveChangesButton);
console.log(usernameInput);
console.log(saveChangesButton);
