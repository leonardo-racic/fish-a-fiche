const MIN_NAME_LENGTH = 0;
const MAX_NAME_LENGTH = 32;
const FORBIDDEN_CHARS = " ";


let createCollectionButton = $("#create-collection-button");
let collectionNameInput = $("#collection-name");


function containsForbiddenChars(chosenName) {
    for (let i = 0; i < FORBIDDEN_CHARS.length; i++) {
        if (chosenName.includes(FORBIDDEN_CHARS[i])) {
            return true;
        }
    }
    return false;
}


function isChosenNameValid(chosenName) {
    if (chosenName.length <= MIN_NAME_LENGTH) {
        return false;
    } else if (chosenName.length > MAX_NAME_LENGTH) {
        return false;
    } else if (containsForbiddenChars(chosenName)) {
        return false;
    }
    return true;
}


collectionNameInput.on("input", function(e) {
    let chosenName = collectionNameInput.val();
    if (isChosenNameValid(chosenName)) {
        createCollectionButton.removeAttr("disabled");
    } else {
        createCollectionButton.attr("disabled", "disabled");
    }
});