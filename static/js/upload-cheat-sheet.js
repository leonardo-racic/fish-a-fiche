"use strict";
import { updateForm } from "./cheat-sheet-input.js";


let titleInput = $("#title-input");
let contextInput = $("#context-input");
let uploadButton = $("#upload-button");


updateForm(titleInput, contextInput, null, uploadButton, "no-content");