
// Functions for MAINAPP

// Function to go back
function goBack() {
    try {
        window.history.back();
    }
    catch {
        window.location.href = "http://127.0.0.1:8000";
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

// Function for slideshow
function slideshow() {
    var slideIndex = 0;
    showSlides();

    function showSlides() {
        var slides = document.querySelectorAll(".slide-image");
        var i;
        for (i = 0; i < slides.length; i++) {
            slides[i].classList.add("hidden")
        }
        slideIndex++;
        if (slideIndex > slides.length) {
            slideIndex = 1;
        }
        slides[slideIndex - 1].classList.remove("hidden");
        setTimeout(showSlides, 3000);
    }
}

// Function to infinite scroll
function infiniteScroll() {
    if (document.getElementById("stop-scrolling").innerHTML === "False") {
        if (window.innerHeight + window.scrollY === document.body.offsetHeight) {
            var data = $("#filter-form").serializeArray();
            data[1].value++;
            var currentUrl = window.location.href;
            currentUrl = currentUrl.slice(0, currentUrl.length - 3);
            if (data[2].value === "" && data[3].value === "") {
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
                        if (data.stop_scrolling === true) {
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
                    if (data.stop_scrolling === true) {
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

// Function to build book results from filters
function buildListing(books, data, currentUrl) {
    const booklistContainer = document.getElementById("booklist-container");
    for (i = 0; i < books.length; i++) {
        // build each book listing, append to booklistContainer
        const bookListingDiv = document.createElement("div");
        bookListingDiv.classList.add("book-listing", "hori", "fade-in");
        // create image elements
        const imageDiv = document.createElement("div");
        imageDiv.classList.add("vert", "image-div");
        const picture = document.createElement("picture");
        const sourceAvif = document.createElement("source");
        sourceAvif.srcset = currentUrl + "static/" + books[i].image + "_small.avif";
        sourceAvif.type = "image/avif";
        const imgLink = document.createElement("a");
        imgLink.href = currentUrl + "book/" + books[i].id;
        const image = document.createElement("img");
        image.src = currentUrl + "static/" + books[i].image + "_small.jpg";
        image.alt = books[i].title + " Cover";
        image.classList.add("small-img");
        imgLink.appendChild(image);
        picture.appendChild(sourceAvif);
        picture.appendChild(imgLink);
        imageDiv.appendChild(picture);
        bookListingDiv.appendChild(imageDiv);
        // create main content elements
        const contentDiv = document.createElement("div");
        contentDiv.classList.add("vert");
        const releaseDate = document.createElement("p");
        releaseDate.innerHTML = `Published ${books[i].date_released}`;
        // create title
        const titleDiv = document.createElement("div");
        titleDiv.classList.add("hori", "listing-title");
        const titleParagraph = document.createElement("p");
        const titleLink = document.createElement("a");
        titleLink.href = currentUrl + "book/" + books[i].id;
        titleLink.innerHTML = books[i].title;
        titleParagraph.appendChild(titleLink);
        titleDiv.appendChild(titleParagraph);
        if (books[i].audio_book == true) {
            const audioBook = document.createElement("h5");
            const icon = document.createElement("i");
            icon.classList.add("fas", "fa-headphones");
            audioBook.appendChild(icon);
            const span = document.createElement("span");
            span.classList.add("tooltip-text");
            span.innerHTML = "Available as an Audio Book";
            audioBook.appendChild(span);
            titleDiv.appendChild(audioBook);
        }
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
        const synopsisP = document.createElement("p");
        synopsisP.id = `book-synopsis-${books[i].id}`;
        synopsisP.classList.add("synopsis")
        synopsisP.innerHTML = books[i].synopsis;
        const synopsisLabel = document.createElement("label");
        synopsisLabel.for = synopsisP.id;
        synopsisLabel.innerHTML = "Synopsis:";
        const seeMoreDiv = document.createElement("div");
        seeMoreDiv.style = "text-align: center";
        const seeMore = document.createElement("button");
        seeMore.type = "button";
        seeMore.classList.add("btn", "btn-primary", "btn-sm", "more-btn");
        seeMore.innerHTML = "See more";
        seeMore.addEventListener("click", showMore);
        seeMoreDiv.appendChild(seeMore);
        synopsisDiv.appendChild(synopsisLabel);
        synopsisDiv.appendChild(synopsisP);
        synopsisDiv.appendChild(seeMoreDiv);
        // if on sale
        if (books[i].on_sale === true) {
            const onSale = document.createElement("h5");
            onSale.innerHTML = "On Sale Now!";
            contentDiv.appendChild(onSale);
        }
        // append together
        contentDiv.appendChild(titleDiv);
        contentDiv.appendChild(releaseDate);
        contentDiv.appendChild(seriesDiv);
        contentDiv.appendChild(worldDiv);
        contentDiv.appendChild(synopsisDiv);
        bookListingDiv.appendChild(contentDiv);
        booklistContainer.appendChild(bookListingDiv);
    }
}

// Function to clear filter results
function clearFilters() {
    var url = this.form.action;
    var currentUrl = window.location.href;
    currentUrl = currentUrl.slice(0, currentUrl.length - 3);
    try {
        var bookList = document.querySelectorAll(".book-listing");
    }
    catch { }
    try {
        var loreList = document.querySelectorAll(".lore-listing");
    }
    catch { }
    data = $("#clear-filter-form").serializeArray();
    clearFiltersFunc(data);

    function clearFiltersFunc(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                if (url.slice(url.length - 3) === "all") {
                    // clear book filters
                    document.getElementById("series-name").innerHTML = "";
                    document.getElementById("series-description").innerHTML = "";
                    document.getElementById("selected-series").classList.add("hidden");
                    document.getElementById("world-name").innerHTML = "";
                    document.getElementById("selected-world").classList.add("hidden");
                    document.getElementById("error-message").innerHTML = "";
                    document.getElementById("error-message").classList.add("hidden");
                    document.getElementById("clear-filter").classList.add("hidden");
                    bookList.forEach((listing) => {
                        listing.remove();
                    })
                    document.getElementById("pagenum").value = 1;
                    resetFilter("series-filter", "world-filter", "");
                    // build new book listings
                    buildListing(data.books, data, currentUrl);
                    document.getElementById("stop-scrolling").innerHTML = "False";
                }
                else {
                    // clear lore filters
                }
            }
        });
        return false;
    }
}
// Function to reset search filter
function resetFilter(seriesId, worldId, valueToSelect) {
    let seriesElement = document.getElementById(seriesId);
    let worldElement = document.getElementById(worldId)
    seriesElement.value = valueToSelect;
    worldElement.value = valueToSelect;
}

// Function to display filtered lore results

// Function to build lore results from filters

// Function to display more of the synopsis
function showMore() {
    var synopsis = this.parentElement.previousElementSibling;
    if (this.innerHTML === "See more") {
        synopsis.style.maxHeight = "700px";
        synopsis.style.background = "none";
        this.style.marginTop = "0";
        this.parentElement.style.height = "2rem";
        console.log(this.parentElement);
        this.innerHTML = "See less";
    }
    else {
        synopsis.style.maxHeight = "5rem";
        synopsis.style.background = "linear-gradient(to top, rgba(0,0,0,0.7), 1%, rgba(0,0,0,0.0))";
        this.style.marginTop = "-2rem";
        this.parentElement.style.height = "0";
        this.innerHTML = "See more";
    }
}

// Function to show the scroll button
function topButtonScroll() {
    var scrollBtn = document.getElementById("return-to-top");
    var screen = window.screen.height;
    if (document.body.scrollTop > screen / 2 || document.documentElement.scrollTop > screen / 2) {
        scrollBtn.classList.remove("hidden");
    }
    else {
        scrollBtn.classList.add("hidden");
    }
}

// Function to scroll to the top of the page
function returnToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

// Function to darken the page and display larger image
function largeImage() {
    var modal = document.getElementById("my-modal");
    var close = document.querySelector(".close");
    modal.classList.remove("hidden");
    modal.style.display = "block";

    close.onclick = function () {
        modal.classList.add("hidden");
        modal.style.display = "none";
    }
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
}


// Functions for USERAPP & EMAILAPP

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
    if (password.type === "password") {
        password.setAttribute("type", "text");
        if (confirmation != null) {
            confirmation.setAttribute("type", "text");
        }
        document.getElementById("eye").src = eye.slice(0, eye.length - 17) + "hide_password.jpg";
        document.getElementById("eye-label").innerHTML = "Hide Password";
        document.getElementById("eye").parentElement.children[0].srcset = eye.slice(0, eye.length - 17) + "hide_password.avif";
    }
    else {
        password.setAttribute("type", "password");
        if (confirmation != null) {
            confirmation.setAttribute("type", "password");
        }
        document.getElementById("eye").src = eye.slice(0, eye.length - 17) + "show_password.jpg";
        document.getElementById("eye-label").innerHTML = "Show Password";
        document.getElementById("eye").parentElement.children[0].srcset = eye.slice(0, eye.length - 17) + "show_password.avif";
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
    else if (username === password) {
        errorMessage.innerHTML = "Invalid password";
    }
    else if (password != confirmation) {
        errorMessage.innerHTML = "Password does not match confirmation";
    }
    else {
        document.querySelector(".registration-content").style.opacity = "50%";
        var spinner = document.querySelector(".spinner-border");
        spinner.parentElement.classList.remove("hidden");
        var data = $("#registration-form").serializeArray();
        registerUser(data);

        function registerUser(data) {
            $.ajax({
                type: "POST",
                url: "register",
                dataType: "json",
                data: data,
                success: function (data) {
                    if (data.success === true) {
                        window.location.href = data.url;
                    }
                    else {
                        errorMessage.innerHTML = data.error_message;
                    }
                    document.querySelector(".registration-content").style.opacity = "100%";
                    spinner.parentElement.classList.add("hidden");
                }
            });
            return false;
        }
    }
}

// Function to verify email for registration
function verifyEmailRegister() {
    document.querySelector(".verify-email").style.opacity = "50%";
    var spinner = document.querySelector(".spinner-border");
    spinner.parentElement.classList.remove("hidden");
    var data = $("#verify-email-form").serializeArray();
    verifyRegistration(data);

    function verifyRegistration(data) {
        $.ajax({
            type: "POST",
            url: "verify_registration",
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.success === true) {
                    window.location.href = data.url;
                }
                else {
                    document.querySelector(".verify-email").style.opacity = "100%";
                    spinner.parentElement.classList.add("hidden");
                    document.getElementById("error-message").innerHTML = data.error_message;
                    // pause, then redirect;
                    var url = data.url
                    setTimeout(function () {
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
    document.querySelector(".login-form").style.opacity = "50%";
    var spinner = document.querySelector(".spinner-border");
    spinner.parentElement.classList.remove("hidden");
    var data = $("#reset-form").serializeArray();
    verifyEmail(data);

    function verifyEmail(data) {
        $.ajax({
            type: "POST",
            url: "reset",
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.success === false) {
                    document.getElementById("error-message").innerHTML = data.error_message;
                }
                else {
                    window.location.href = data.url;
                }
                document.querySelector(".login-form").style.opacity = "100%";
                spinner.parentElement.classList.add("hidden");
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

    if (passcode.length === 0) {
        errorMessage.innerHTML = "Missing passcode";
    }
    else if (password.length < 8) {
        errorMessage.innerHTML = "Invalid password";
    }
    else if (password != confirmation) {
        errorMessage.innerHTML = "Password does not match confirmation";
    }
    else {
        document.querySelector(".registration-content").style.opacity = "50%";
        var spinner = document.querySelector(".spinner-border");
        spinner.parentElement.classList.remove("hidden");
        var data = $("#verify-reset-form").serializeArray();
        verifyReset(data);

        function verifyReset(data) {
            $.ajax({
                type: "POST",
                url: "verify_reset",
                dataType: "json",
                data: data,
                success: function (data) {
                    document.querySelector(".registration-content").style.opacity = "100%";
                    spinner.parentElement.classList.add("hidden");
                    if (data.success === true) {
                        errorMessage.innerHTML = "Success! You will be redirected soon";
                        var url = data.url
                        setTimeout(function () {
                            window.location.href = url;
                        }, 3000);
                    }
                    else {
                        errorMessage.innerHTML = data.error_message;
                        if (data.url) {
                            var url = data.url
                            setTimeout(function () {
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
    document.querySelector(".login-form").style.opacity = "50%";
    var spinner = document.querySelector(".spinner-border");
    spinner.parentElement.classList.remove("hidden");
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
                document.querySelector(".login-form").style.opacity = "100%";
                spinner.parentElement.classList.add("hidden");
            }
        });
        return false;
    }
}

// Function to show user preference and delete account forms 
function showContent() {
    let content = this.previousElementSibling;
    if (content.style.maxHeight) {
        content.style.maxHeight = null;
        if (content.id === "edit-preference-form") {
            this.innerHTML = "Change Email Preferences";
        }
        else {
            this.innerHTML = "Delete Account";
            document.getElementById("delete-error-message").innerHTML = "";
        }
    }
    else {
        content.style.maxHeight = "1000px";
        content.classList.remove("hidden");
        this.innerHTML = "Cancel"
    }
}

// Function to change user email preferences
function editPreferences() {
    var data = $("#edit-preference-form").serializeArray();
    var url = this.form.action;
    editPreferenceFunc(data);

    function editPreferenceFunc(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                var saveMessage = document.getElementById("save-message");
                saveMessage.innerHTML = "Your preferences have been saved";
                saveMessage.style.display = "flex";
                setTimeout(function () {
                    $("#save-message").fadeOut(1000);
                }, 3000);
            }
        });
        return false;
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

// Function to show delete account error messages
function deleteAccount() {
    var data = $("#delete-account-form").serializeArray();
    var url = this.form.action;
    deleteAccountFinal(data);

    function deleteAccountFinal(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.success === false) {
                    document.getElementById("delete-error-message").innerHTML = data.message;
                }
                else {
                    window.location.href = data.url;
                }
            }
        });
        return false;
    }
}

// Function to add or remove books from wishlist
function wishlistFunc() {
    var bookId = this.form.classList[0];
    var formId = this.form.id;
    var url = this.form.action;
    data = $(`#${formId}`).serializeArray();
    var page = data[1].value;
    if (page === "profile") {
        this.form.parentElement.style.opacity = "50%";
    }
    updateWish(data);

    function updateWish(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                if (page === "profile") {
                    if (data.action === "remove") {
                        document.getElementById(`wish-element-${bookId}`).children[0].classList.add("hidden");
                        document.getElementById(`wish-btn-${bookId}`).innerHTML = "Undo";
                    }
                    else {
                        document.getElementById(`wish-element-${bookId}`).children[0].classList.remove("hidden");
                        document.getElementById(`wish-btn-${bookId}`).innerHTML = "Remove";
                    }
                    document.getElementById(`wish-element-${bookId}`).style.opacity = "100%";
                }
                else {
                    if (data.action === "remove") {
                        document.getElementById("wish-btn").innerHTML = "Add to wishlist";
                    }
                    else {
                        document.getElementById("wish-btn").innerHTML = "Remove from wishlist";
                    }
                }
            }
        });
        return false;
    }
}

// Function to follow and unfollow series
function followFunc() {
    var seriesId = this.form.classList[0];
    var formId = this.form.id;
    var url = this.form.action;
    data = $(`#${formId}`).serializeArray();
    var page = data[1].value;
    if (page === "profile") {
        this.form.parentElement.style.opacity = "50%";
    }
    updateFollow(data);

    function updateFollow(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                if (page === "profile") {
                    if (data.action === "remove") {
                        document.getElementById(`follow-element-${seriesId}`).children[0].classList.add("hidden");
                        document.getElementById(`follow-btn-${seriesId}`).innerHTML = "Undo";
                    }
                    else {
                        document.getElementById(`follow-element-${seriesId}`).children[0].classList.remove("hidden");
                        document.getElementById(`follow-btn-${seriesId}`).innerHTML = "Unfollow";
                    }
                    document.getElementById(`follow-element-${seriesId}`).style.opacity = "100%";
                }
                else {
                    if (data.action === "remove") {
                        document.getElementById("follow-btn").innerHTML = "Follow Series";
                    }
                    else {
                        document.getElementById("follow-btn").innerHTML = "Unfollow Series";
                    }
                }
            }
        });
        return false;
    }
}
