const MIN_LENGTH = 0;
const MAX_TITLE_LENGTH = 32;
const MAX_KEYWORDS = 10;
const MAX_KEYWORD_LENGTH = 20;


function isInputValid(input) {
    return (input.length > MIN_LENGTH);
}


function isTitleValid(input) {
    return isInputValid(input) && input.length <= MAX_TITLE_LENGTH;
}


function areCharactersValid(input) {
    for (let c of input) {
        if (c.match(/[a-z]/i) || c === "-" || c === " ") {
            continue;
        } else {
            return false
        }
    }
    return true;
}


function isKeywordNumberValid(input) {
    let numberOfKeywords = input.split(" ").length;
    return numberOfKeywords <= MAX_KEYWORDS;
}


function noRepeatingKeyword(input) {
    let cache = [];
    let keywords = input.split(" ");
    for (let k of keywords) {
        if (!cache.includes(k) && k.length < MAX_KEYWORD_LENGTH) {
            cache.push(k);
        } else {
            return false;
        }
    }
    return true;
}


function isContextValid(input) {
    if (!isInputValid(input)) {
        return false;
    }
    if (!areCharactersValid(input)) {
        return false;
    }
    if (!isKeywordNumberValid(input)) {
        return false;
    }
    if (!noRepeatingKeyword(input)) {
        return false;
    }
    return true;
}


function isFormInputValid(titleInput, contextInput, contentInput) {
    let titleValid = isTitleValid(titleInput.val());
    let contentValid = isInputValid(contentInput.val());
    let contextValid = isContextValid(contextInput.val());
    let condition = titleValid && contentValid && contextValid
    return condition;
}


function updateButton(titleInput, contextInput, contentInput, button) {
    if (isFormInputValid(titleInput, contextInput, contentInput)) {
        button.removeAttr("disabled");
    } else {
        button.attr("disabled", "disabled");
    }
}


function updateElement(element, titleInput, contextInput, contentInput, button) {
    element.on("input", () => {
        updateButton(titleInput, contextInput, contentInput, button);
    });
} 


export function updateForm(titleInput, contextInput, contentInput, button) {
    let inputFields = [titleInput, contextInput, contentInput];
    for (let element of inputFields) {
        updateElement(element, titleInput, contextInput, contentInput, button);
    }
}