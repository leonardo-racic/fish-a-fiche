import { updateForm } from "./cheat-sheet-input.js"


let titleInput = $("#title-input");
let contentInput = $("#content-input");
let contextInput = $("#context-input");
let saveButton = $("#save-button");


updateForm(titleInput, contextInput, contentInput, saveButton);