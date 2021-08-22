
document.addEventListener("DOMContentLoaded", function () {
    let scrollY = window.scrollY;
    let windowHeight = window.innerHeight;
    let docHeight = document.body.offsetHeight;

    if (scrollY + windowHeight == docHeight) {
        console.log("true");
    }
})

// Function to infinite scroll
function infiniteScroll() {
    /*
    window.onscroll = () => {
        if (window.innerHeight + window.scrollY == document.body.offsetHeight) {
            // get pagenum value and increment by 1
            var pagenum = parseInt(document.getElementById("pagenum").innerHTML);
            pagenum++;
            scroll(pagenum);
            // then pass to views.py via AJAX, for the view to render the next 8 elements (GET request)
            function scroll(pagenum) {
                $.ajax({
                    type: "GET",
                    url: "/all/",
                    dataType: "json",
                    data: pagenum,
                    success: function (data) {
                        console.log(data);
                        // append book elements to the end of .booklist
                    }
                });
                return false;
            }
        }
    }
    */
}


// Function to get cookie for csrf_token to pass form data securely
/*
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
*/


// Function to display filtered book results
function displayFilters() {
    var data = $("#filter-form").serializeArray();
    var booklist = document.querySelectorAll(".book_listing");
    var errorMessage = document.getElementById("error-message");
    var selectedSeries = document.getElementById("selected-series");
    var selectedWorld = document.getElementById("selected-world");
    var imageUrl = document.querySelectorAll("img")[0].src;
    imageUrl = imageUrl.slice(0, imageUrl.length - 55);
    var currentUrl = window.location.href;
    currentUrl = currentUrl.slice(0, currentUrl.length - 3);
    console.log("url:", currentUrl);
    console.log("imageUrl:", imageUrl);
    console.log("initial values:", data);
    filterFunction(data);

    function filterFunction(data) {
        $.ajax({
            type: "POST",
            url: "all",
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.error) {
                    errorMessage.innerHTML = data.error;
                    errorMessage.classList.remove("hidden");
                    selectedWorld.classList.add("hidden");
                    selectedSeries.classList.add("hidden");
                }
                else {
                    errorMessage.classList.add("hidden");
                    if (data.selected_world) {
                        selectedWorld.classList.remove("hidden");
                        document.getElementById("world-name").innerHTML = data.selected_world;
                    }
                    else {
                        selectedWorld.classList.add("hidden");
                    }
                    if (data.selected_series_name) {
                        selectedSeries.classList.remove("hidden");
                        document.getElementById("series-name").innerHTML = data.selected_series_name;
                        document.getElementById("series-description").innerHTML = data.selected_series_description;
                    }
                    else {
                        selectedSeries.classList.add("hidden");
                    }
                    booklist.forEach((listing) => {
                        listing.remove();
                    })
                    books = data.books;
                    booklistContainer = document.getElementById("booklist-container");
                    for (i = 0; i < books.length; i++) {
                        // build each book listing, append to booklistContainer
                        const bookListingDiv = document.createElement("div");
                        bookListingDiv.classList.add("book-listing", "hori");
                        const titleDiv = document.createElement("div");
                        titleDiv.classList.add("vert");
                        const image = document.createElement("img");
                        image.src = imageUrl + books[i].image + "_small.avif";
                        image.alt = books[i].title + " Cover";
                        image.width = "150px";
                        image.height = "200px";
                        const titleParagraph = document.createElement("p");
                        const titleLink = document.createElement("a");
                        titleLink.href = currentUrl + "book/" + books[i].id;
                        titleLink.innerHTML = books[i].title;
                        titleParagraph.appendChild(titleLink);
                        titleDiv.appendChild(titleParagraph, image);
                        bookListingDiv.appendChild(titleDiv);

                    }
                }
                // show button to clear filters
                document.getElementById("clear-filter").classList.remove("hidden");
            }
        });
        return false;
    }
}


// Function to show or hide password
function showPassword() {
    let password = document.getElementById("password");
    let confirmation = "";
    try {
        confirmation = document.getElementById("confirmation");
    }
    catch {
        confirmation = null;
    }
    let eye = document.getElementById("eye").src;
    if (password.type == "password") {
        password.setAttribute("type", "text");
        if (confirmation != null) {
            confirmation.setAttribute("type", "text");
        }
        document.getElementById("eye").src = eye.slice(0, eye.length - 18) + "hide_password.avif";
        document.getElementById("eye-label").innerHTML = "Hide Password";
    }
    else {
        password.setAttribute("type", "password");
        if (confirmation != null) {
            confirmation.setAttribute("type", "password");
        }
        document.getElementById("eye").src = eye.slice(0, eye.length - 18) + "show_password.avif";
        document.getElementById("eye-label").innerHTML = "Show Password";
    }
}


// Function to verify registration requirements for account creation
function verifyRequirements() {
    let password = document.getElementById("password").value;
    let confirmation = document.getElementById("confirmation").value;
    let username = document.getElementById("username").value;
    let email = document.getElementById("email").value;

    const errorMessage = document.getElementById("error-message");

    if (username.length < 6) {
        errorMessage.innerHTML = "Invalid username";
    }
    else if (email.length < 1) {
        errorMessage.innerHTML = "Missing email address"
    }
    else if (password.length < 8) {
        errorMessage.innerHTML = "Invalid password";
    }
    else if (username == password) {
        errorMessage.innerHTML = "Invalid password";
    }
    else if (password != confirmation) {
        errorMessage.innerHTML = "Password does not match confirmation";
    }
    else {
        // Pass to AJAX
    }
}


// Function to verify registration requirements for email reset
function verifyRequirementsReset() {
    let password = document.getElementById("password").value;
    let confirmation = document.getElementById("confirmation").value;

    const errorMessage = document.getElementById("error-message");

    if (password.length < 8) {
        errorMessage.innerHTML = "Invalid password";
    }
    else if (password != confirmation) {
        errorMessage.innerHTML = "Password does not match confirmation";
    }
    else {
        // Pass to AJAX
    }
}


// Function to show login error messages
// use AJAX
function loginErrors() {

}


// Function to show ability to edit user preferences
function editPreferences() {
    let form = document.getElementById("edit-preference-form");
    let button = document.getElementById("show-preference-form");

    if (button.innerHTML == "Change Email Preferences") {
        form.classList.remove("hidden");
        button.innerHTML = "Cancel";
    }
    else {
        form.classList.add("hidden");
        button.innerHTML = "Change Email Preferences";
    }
}


// Function to uncheck all email preferences
function uncheckAll() {
    let checkboxes = document.querySelectorAll(".checkbox");
    for (i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            checkboxes[i].checked = false;
        }
    }
}


// Function to show delete account option
function deleteAccount() {
    let form = document.getElementById("delete-account-div");
    let button = document.getElementById("delete-account-btn");

    if (button.innerHTML == "Delete Account") {
        form.classList.remove("hidden");
        button.innerHTML = "Cancel";
    }
    else {
        form.classList.add("hidden");
        button.innerHTML = "Delete Account";
    }
}


// Function to make search button clickable
function makeClickable() {
    let userInput = document.getElementById("searchbox").value;
    let searchButton = document.getElementById("search-btn");

    if (userInput.length > 0) {
        searchButton.type = "submit";
    }
    else {
        searchButton.type = "button";
    }
}

