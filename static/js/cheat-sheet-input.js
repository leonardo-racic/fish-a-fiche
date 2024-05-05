"use strict";
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


function getCondition(titleInput, contextInput, contentInput, particularity) {
    let condition = [];
    try {
        let titleValid = isTitleValid(titleInput.val());
        let contentValid = isInputValid(contentInput.val());
        let contextValid = isContextValid(contextInput.val());
        condition.push(titleValid, contentValid, contextValid);
    } catch (error) {
        if (particularity === "no-content") {
            let titleValid = isTitleValid(titleInput.val());
            let contextValid = isContextValid(contextInput.val());
            condition = [titleValid, contextValid];
        }
    }
    return condition;
}


function isFormInputValid(titleInput, contextInput, contentInput, particularity) {
    let condition = getCondition(titleInput, contextInput, contentInput, particularity);
    for (let isValid of condition) {
        if (!isValid) {
            return false;
        }
    }
    return true;
}


function updateButton(titleInput, contextInput, contentInput, button, particularity) {
    if (isFormInputValid(titleInput, contextInput, contentInput, particularity)) {
        button.removeAttr("disabled");
    } else {
        button.attr("disabled", "disabled");
    }
}


function updateElement(element, titleInput, contextInput, contentInput, button, particularity) {
    element.on("input", () => {
        updateButton(titleInput, contextInput, contentInput, button, particularity);
    });
} 


export function updateForm(titleInput, contextInput, contentInput, button, particularity = "") {
    let inputFields = [titleInput, contextInput, contentInput];
    for (let element of inputFields) {
        if (element !== null) {
            updateElement(element, titleInput, contextInput, contentInput, button, particularity);
        }
    }
}