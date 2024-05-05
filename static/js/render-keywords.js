"use strict";
function getKeywords(context) {
    return context.split(" ");
}


function addKeyword(element, keyword) {
    $("<a/>", {
        text: keyword,
        class: "btn btn-outline-info me-2",
        href: `/search/${keyword}&context`,
    }).appendTo(element);
}


let contextElement = $("#context");
let context = contextElement.html();
let keywords = getKeywords(context);
contextElement.html("");
for (let k of keywords) {
    addKeyword(contextElement, k);
}