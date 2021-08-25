
// Function to infinite scroll
function infiniteScroll() {
    window.onscroll = () => {
        if (document.getElementById("stop-scrolling").innerHTML == "False") {
            if (window.innerHeight + window.scrollY == document.body.offsetHeight) {
                var data = $("#filter-form").serializeArray();
                data[1].value++;
                var currentUrl = window.location.href;
                currentUrl = currentUrl.slice(0, currentUrl.length - 3);
                if (data[2].value == "" && data[3].value == "") {
                    var url = "all";
                }
                else {
                    var url = "filter_books";
                }
                scroll(data);

                function scroll(data) {
                    $.ajax({
                        type: "POST",
                        url: url,
                        dataType: "json",
                        data: data,
                        success: function (data) {
                            document.getElementById("pagenum").value = data.pagenum;
                            // append book elements to the end of .booklist
                            if (data.error) {
                                let errorMessage = document.getElementById("error-message");
                                let selectedSeries = document.getElementById("selected-series");
                                let selectedWorld = document.getElementById("selected-world");
                                errorMessage.innerHTML = data.error;
                                errorMessage.classList.remove("hidden");
                                selectedWorld.classList.add("hidden");
                                selectedSeries.classList.add("hidden");
                            }
                            else {
                                buildListing(data.books, data, currentUrl);
                            }
                            if (data.stop_scrolling == true) {
                                document.getElementById("stop-scrolling").innerHTML = "True";
                            }
                            else {
                                document.getElementById("stop-scrolling").innerHTML = "False";
                            }
                        }
                    });
                    return false;
                }
            }
        }
    }
}

// Function to display filtered book results
function displayFilters() {
    document.getElementById("pagenum").value = 1;
    var data = $("#filter-form").serializeArray();
    var booklist = document.querySelectorAll(".book-listing");
    var errorMessage = document.getElementById("error-message");
    var selectedSeries = document.getElementById("selected-series");
    var selectedWorld = document.getElementById("selected-world");
    var currentUrl = window.location.href;
    currentUrl = currentUrl.slice(0, currentUrl.length - 3);
    filterBooks(data);

    function filterBooks(data) {
        $.ajax({
            type: "POST",
            url: "filter_books",
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
                    // clear existing listings
                    booklist.forEach((listing) => {
                        listing.remove();
                    })
                    // build new listings
                    buildListing(data.books, data, currentUrl);
                    
                    // show button to clear filters
                    document.getElementById("clear-filter").classList.remove("hidden");

                    // signal page to stop scrolling
                    if (data.stop_scrolling == true) {
                        document.getElementById("stop-scrolling").innerHTML = "True";
                    }
                    else {
                        document.getElementById("stop-scrolling").innerHTML = "False";
                    }
                }   
            }
        });
        return false;
    }
}

function buildListing(books, data, currentUrl) {
    const booklistContainer = document.getElementById("booklist-container");
    for (i = 0; i < books.length; i++) {
        // build each book listing, append to booklistContainer
        const bookListingDiv = document.createElement("div");
        bookListingDiv.classList.add("book-listing", "hori");
        // create title + image elements
        const titleDiv = document.createElement("div");
        titleDiv.classList.add("vert");
        titleDiv.classList.add("title-div");
        const image = document.createElement("img");
        image.src = currentUrl + "static/" + books[i].image + "_small.avif";
        image.alt = books[i].title + " Cover";
        image.width = "150";
        image.height = "200";
        const titleParagraph = document.createElement("p");
        const titleLink = document.createElement("a");
        titleLink.href = currentUrl + "book/" + books[i].id;
        titleLink.innerHTML = books[i].title;
        titleParagraph.appendChild(titleLink);
        titleDiv.appendChild(image);
        titleDiv.appendChild(titleParagraph);
        bookListingDiv.appendChild(titleDiv);
        // create main content elements
        const contentDiv = document.createElement("div");
        contentDiv.classList.add("vert");
        const releaseDate = document.createElement("p");
        releaseDate.innerHTML = `Published ${books[i].date_released}`;
        // series div
        const seriesDiv = document.createElement("div");
        seriesDiv.classList.add("hori");
        const seriesP = document.createElement("p");
        seriesP.id = `book-series-${books[i].title}`;
        seriesP.innerHTML = data.series_list[parseInt(books[i].series_id) - 1].name;
        const seriesLabel = document.createElement("label");
        seriesLabel.for = seriesP.id;
        seriesLabel.innerHTML = "Series:";
        seriesDiv.appendChild(seriesLabel);
        seriesDiv.appendChild(seriesP);
        // world div
        const worldDiv = document.createElement("div");
        worldDiv.classList.add("hori");
        const worldP = document.createElement("p");
        worldP.id = `book-world-${books[i].title}`;
        worldP.innerHTML = books[i].world;
        const worldLabel = document.createElement("label");
        worldLabel.for = worldP.id;
        worldLabel.innerHTML = "World:";
        worldDiv.appendChild(worldLabel);
        worldDiv.appendChild(worldP);
        // synopsis div
        const synopsisDiv = document.createElement("div");
        synopsisDiv.classList.add("hori");
        const synopsisP = document.createElement("p");
        synopsisP.id = `book-synopsis-${books[i].id}`;
        synopsisP.innerHTML = `${books[i].synopsis.slice(0, 300)} ...`;
        const synopsisLabel = document.createElement("label");
        synopsisLabel.for = synopsisP.id;
        synopsisLabel.innerHTML = "Synopsis:";
        const seeMoreLink = document.createElement("a");
        seeMoreLink.href = currentUrl + "book/" + books[i].id;
        seeMoreLink.innerHTML = "See more";
        synopsisP.appendChild(seeMoreLink);
        synopsisDiv.appendChild(synopsisLabel);
        synopsisDiv.appendChild(synopsisP);
        // if on sale
        if (books[i].on_sale == true) {
            const onSale = document.createElement("h5");
            onSale.innerHTML = "On Sale Now!";
            contentDiv.appendChild(onSale);
        }
        // append together
        contentDiv.appendChild(releaseDate);
        contentDiv.appendChild(seriesDiv);
        contentDiv.appendChild(worldDiv);
        contentDiv.appendChild(synopsisDiv);
        bookListingDiv.appendChild(contentDiv);
        booklistContainer.appendChild(bookListingDiv);
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

// Functions for USERAPP

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
        var data = $("#registration-form").serializeArray();
        registerUser(data);

        function registerUser(data) {
            $.ajax({
                type: "POST",
                url: "register",
                dataType: "json",
                data: data,
                success: function (data) {
                    if (data.success == true) {
                        window.location.href = data.url;
                    }
                    else {
                        errorMessage.innerHTML = data.error_message;
                    }
                }
            });
            return false;
        }
    }
}

// Function to verify email for registration
function verifyEmailRegister() {
    var data = $("#verify-email-form").serializeArray();
    verifyRegistration(data);

    function verifyRegistration(data) {
        $.ajax({
            type: "POST",
            url: "verify_registration",
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.success == true) {
                    window.location.href = data.url;
                }
                else {
                    document.getElementById("error-message").innerHTML = data.error_message;
                    // pause, then redirect;
                    var url = data.url
                    setTimeout(function() {
                        window.location.href = url;
                    }, 3000);
                }
            }
        });
        return false;
    }
}

// Function to reset password
function resetPassword() {
    var data = $("#reset-form").serializeArray();
    verifyEmail(data);

    function verifyEmail(data) {
        $.ajax({
            type: "POST",
            url: "reset",
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.success == false) {
                    document.getElementById("error-message").innerHTML = data.error_message;
                }
                else {
                    window.location.href = data.url;
                }
            }
        });
        return false;
    }
}

// Function to verify registration requirements for email reset
function verifyRequirementsReset() {
    let password = document.getElementById("password").value;
    let confirmation = document.getElementById("confirmation").value;
    let passcode = document.getElementById("passcode").value;

    var errorMessage = document.getElementById("error-message");

    if (passcode.length == 0) {
        errorMessage.innerHTML = "Missing passcode";
    }
    else if (password.length < 8) {
        errorMessage.innerHTML = "Invalid password";
    }
    else if (password != confirmation) {
        errorMessage.innerHTML = "Password does not match confirmation";
    }
    else {
        // Pass to AJAX
        var data = $("#verify-reset-form").serializeArray();
        verifyReset(data);
        
        function verifyReset(data) {
            $.ajax({
                type: "POST",
                url: "verify_reset",
                dataType: "json",
                data: data,
                success: function (data) {
                    if (data.success == true) {
                        window.location.href = data.url;
                    }
                    else {
                        errorMessage.innerHTML = data.error_message;
                        if (data.url) {
                            var url = data.url
                            setTimeout(function() {
                                window.location.href = url;
                            }, 3000);
                        }
                    }
                }
            });
            return false;
        }
    }
}

// Function to login and show login error messages
function submitLogin() {
    var data = $("#login-form").serializeArray();
    checkError(data);

    function checkError(data) {
        $.ajax({
            type: "POST",
            url: "login",
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.success) {
                    window.location.href = data.url;
                }
                else {
                    document.getElementById("error-div").classList.remove("hidden");
                    document.getElementById("error-message").innerHTML = data.message;
                }
            }
        });
        return false;
    }
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

// Function to remove books from wishlist
// AJAX

// Function to unfollow series
// AJAX

// Function to show delete account error messages
// AJAX