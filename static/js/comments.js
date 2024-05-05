"use strict";
const MIN_LENGTH = 0;


let commentButton = $("#comment-button");
let commentInput = $("#comment-input");


function isInputValid(inputVal) {
    return inputVal.length > MIN_LENGTH;
}


function isCommentInputValid() {
    let isCommentValid = isInputValid(commentInput.val());
    return isCommentValid;
}


function updateButton() {
    if (isCommentInputValid()) {
        commentButton.removeAttr("disabled");
    } else {
        commentButton.attr("disabled", "disabled");
    }
}


commentInput.on("input", updateButton);