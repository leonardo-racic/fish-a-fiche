import { updateForm } from "./cheat-sheet-input.js";


let titleInput = $("#title-input");
let contentInput = $("#content-input");
let contextInput = $("#context-input");
let createButton = $("#create-button");


updateForm(titleInput, contextInput, contentInput, createButton);