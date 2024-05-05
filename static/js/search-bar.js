"use strict";
let searchInput = $("#search-input");
let searchButton = $("#search-button");


searchButton.on("click", function() {
    let searchTerm = searchInput.val();
    window.location.href = `/search/${searchTerm}`;
});