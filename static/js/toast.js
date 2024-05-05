"use strict";
const FADING_FREQUENCY = 25.0;
const FADING_DIFF = 0.25;
const MIN_OPACITY = 0.0;
const MAX_OPACITY = 1.0;


function fadeOut(element) {
    let effect = setInterval(function() {
        if (!element.style.opacity) {
            element.style.opacity = MAX_OPACITY.toString();
        }
        let opacity = Number(element.style.opacity);
        if (opacity > MIN_OPACITY) {
            opacity -= FADING_DIFF;
            element.style.opacity = opacity.toString();
        } else {
            clearInterval(effect);
            element.parentNode.removeChild(element);
        }
    }, FADING_FREQUENCY);
}


let toasts = $(".toast");
toasts.show();


for (let t of toasts) {
    let currentToast = $(t)
    let closeButton = currentToast.find(".btn-close");
    closeButton.on("click", function() {
        fadeOut(t);
    });
}