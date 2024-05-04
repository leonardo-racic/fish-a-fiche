$("textarea").each(function () {
    let newStyle = `height: ${this.scrollHeight}px; overflow: hidden;`
    this.setAttribute("style", newStyle);
}).on("input", function () {
    this.style.minHeight = "0";
    let newHeight  = this.scrollHeight + "px";
    this.style.minHeight = newHeight;
});