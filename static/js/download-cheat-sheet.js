"use strict";
function onDowloadClick() {
    let contentDiv = $("#content-div");
    let htmlContent = contentDiv.html();
    downloadForm.on("submit", function() {
        contentInput.val(htmlContent);
        return true;
    });
}