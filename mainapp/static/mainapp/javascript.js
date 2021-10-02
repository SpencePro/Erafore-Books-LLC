
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
    let userInput = this.value;
    let searchButton = this.nextElementSibling;

    if (userInput.length > 0) {
        searchButton.type = "submit";
    }
    else {
        searchButton.type = "button";
    }
}

// Function to toggle navbar on mobile
function displayMobileNav() {
    let navContent = document.getElementById("navbar-mobile");
    let topBar = document.querySelector(".top-bar");
    let middleBar = document.querySelector(".middle-bar");
    let bottomBar = document.querySelector(".bottom-bar");
    if (navContent.style.maxHeight === "0px") {
        navContent.style.maxHeight = "1000px";
        topBar.style.transform = "rotate(45deg)";
        middleBar.style.opacity = 0;
        bottomBar.style.transform = "rotate(-45deg)";
    }
    else {
        navContent.style.maxHeight = "0px";
        topBar.style.transform = "rotate(0)";
        middleBar.style.opacity = 1;
        bottomBar.style.transform = "rotate(0)";
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
            slides[i].classList.add("hidden");
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
    if (document.getElementById("stop-scrolling").innerHTML === "True") {
        document.getElementById("end-of-results").classList.remove("hidden");
    }
    else {
        if (window.innerHeight + window.scrollY === document.body.offsetHeight - 1) {
            var data = $("#filter-form").serializeArray();
            data[1].value++;
            var currentUrl = window.location.href;
            var page = "";
            var spinner = document.querySelector(".spinner-results");
            spinner.style.visibility = "visible";
            
            if (currentUrl.slice(currentUrl.length - 3) === "all") {
                page = "books";
                currentUrl = currentUrl.slice(0, -3);
                if (data[2].value === "" && data[3].value === "") {
                    var url = "all";
                }
                else {
                    var url = "filter_books";
                }
            }
            else {
                page = "lore";
                currentUrl = currentUrl.slice(0, -4);
                if (data[2].value === "" && data[3].value === "" && data[4].value === "") {
                    var url = "lore";
                }
                else {
                    var url = "filter_lore";
                }
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
                        // append elements to the end of .booklist
                        if (data.error) {
                            // hide elements in case of error
                            let errorMessage = document.getElementById("error-message");
                            let selectedSeries = document.getElementById("selected-series");
                            let selectedWorld = document.getElementById("selected-world");
                            let selectedType = document.getElementById("selected-type");
                            errorMessage.innerHTML = data.error;
                            errorMessage.classList.remove("hidden");
                            selectedWorld.classList.add("hidden");
                            selectedSeries.classList.add("hidden");
                            if (page === "lore") {
                                selectedType.classList.add("hidden");
                            }
                        }
                        else {
                            if (page === "books") {
                                buildListing(data.books, data, currentUrl);
                            }
                            else {
                                buildLoreListing(data.lore_data, data, currentUrl);
                            }
                        }
                        spinner.style.visibility = "hidden";

                        if (data.stop_scrolling === true) {
                            document.getElementById("stop-scrolling").innerHTML = "True";
                            document.getElementById("end-of-results").classList.remove("hidden");
                        }
                        else {
                            document.getElementById("stop-scrolling").innerHTML = "False";
                            document.getElementById("end-of-results").classList.add("hidden")
                        }
                    }
                });
                return false;
            }
        }
    }
}

// Function to display filtered results
function displayFilters() {
    document.getElementById("pagenum").value = 1;
    var data = $("#filter-form").serializeArray();
    var booklist = document.querySelectorAll(".book-listing");
    var errorMessage = document.getElementById("error-message");
    var selectedSeries = document.getElementById("selected-series");
    var selectedWorld = document.getElementById("selected-world");
    var selectedType = document.getElementById("selected-type");
    var currentUrl = window.location.href;
    var page = "";
    var url = "";
    document.querySelector(".fetch-results").classList.remove("hidden");
    if (currentUrl.slice(currentUrl.length - 3) === "all") {
        page = "books";
        currentUrl = currentUrl.slice(0, -3);
        url = "filter_books";
    }
    else {
        page = "lore";
        currentUrl = currentUrl.slice(0, -4); 
        url = "filter_lore";
    }
    filterObjects(data);

    function filterObjects(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                if (data.error) {
                    errorMessage.innerHTML = data.error;
                    errorMessage.classList.remove("hidden");
                    selectedWorld.classList.add("hidden");
                    selectedSeries.classList.add("hidden");
                    if (page === "lore") {
                        selectedType.classList.add("hidden");
                    }
                }
                else {
                    errorMessage.classList.add("hidden");
                    if (data.selected_world_name) {
                        selectedWorld.classList.remove("hidden");
                        document.getElementById("world-name").innerHTML = data.selected_world_name;
                        document.getElementById("world-description").innerHTML = data.selected_world_description;
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
                    if (page === "lore") {
                        if (data.selected_type) {
                            selectedType.classList.remove("hidden");
                            document.getElementById("type-name").innerHTML = data.selected_type;
                        }
                        else {
                            selectedType.classList.add("hidden");
                        }
                    }
                    // clear existing listings
                    booklist.forEach((listing) => {
                        listing.remove();
                    })
                    // build new listings
                    if (page === "books") {
                        buildListing(data.books, data, currentUrl);
                    }
                    else {
                        buildLoreListing(data.lore_data, data, currentUrl);
                    }
                    // show button to clear filters
                    document.getElementById("clear-filter").classList.remove("hidden");
                    // signal page to stop scrolling
                    if (data.stop_scrolling === true) {
                        document.getElementById("stop-scrolling").innerHTML = "True";
                        document.getElementById("end-of-results").classList.remove("hidden")
                    }
                    else {
                        document.getElementById("stop-scrolling").innerHTML = "False";
                        document.getElementById("end-of-results").classList.add("hidden")
                    }
                }
                document.querySelector(".fetch-results").classList.add("hidden");
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
        const seriesName = document.createElement("a");
        seriesName.id = `book-series-${books[i].title}`;
        seriesName.innerHTML = data.series_list[parseInt(books[i].series_id) - 1].name;
        seriesName.href = currentUrl + "all/series/" + books[i].series_id;
        const seriesLabel = document.createElement("label");
        seriesLabel.for = seriesName.id;
        seriesLabel.innerHTML = "Series:";
        seriesDiv.appendChild(seriesLabel);
        seriesDiv.appendChild(seriesName);
        // world div
        const worldDiv = document.createElement("div");
        worldDiv.classList.add("hori");
        const worldName = document.createElement("a");
        worldName.id = `book-world-${books[i].title}`;
        worldName.innerHTML = data.worlds[books[i].world_id - 1].name;
        worldName.href = currentUrl + "all/world/" + books[i].world_id;
        const worldLabel = document.createElement("label");
        worldLabel.for = worldName.id;
        worldLabel.innerHTML = "World:";
        worldDiv.appendChild(worldLabel);
        worldDiv.appendChild(worldName);
        // synopsis div
        const synopsisDiv = document.createElement("div");
        synopsisDiv.classList.add("synopsis")
        const synopsisP = document.createElement("p");
        synopsisP.id = `book-synopsis-${books[i].id}`;
        synopsisP.innerHTML = books[i].synopsis;
        const synopsisLabel = document.createElement("label");
        synopsisLabel.for = synopsisP.id;
        synopsisLabel.innerHTML = "Synopsis:";
        const seeMoreDiv = document.createElement("div");
        seeMoreDiv.style = "text-align: center";
        const seeMore = document.createElement("a");
        seeMore.classList.add("btn", "btn-primary", "btn-sm", "more-btn");
        seeMore.innerHTML = "See more";
        seeMore.href = currentUrl + "book/" + books[i].id;
        seeMoreDiv.appendChild(seeMore);
        synopsisDiv.appendChild(synopsisLabel);
        synopsisDiv.appendChild(synopsisP);
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
        contentDiv.appendChild(seeMoreDiv);
        bookListingDiv.appendChild(contentDiv);
        booklistContainer.appendChild(bookListingDiv);
    }
}

// Function to clear filter results
function clearFilters() {
    var url = this.form.action;
    var currentUrl = window.location.href;
    var bookList = document.querySelectorAll(".book-listing");
    data = $("#clear-filter-form").serializeArray();
    document.querySelector(".fetch-results").classList.remove("hidden");
    clearFiltersFunc(data);

    function clearFiltersFunc(data) {
        $.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            data: data,
            success: function (data) {
                // clear book filters
                document.getElementById("series-name").innerHTML = "";
                document.getElementById("series-description").innerHTML = "";
                document.getElementById("selected-series").classList.add("hidden");
                document.getElementById("world-name").innerHTML = "";
                document.getElementById("selected-world").classList.add("hidden");
                document.getElementById("error-message").innerHTML = "";
                document.getElementById("error-message").classList.add("hidden");
                document.getElementById("clear-filter").classList.add("hidden");
                document.getElementById("end-of-results").classList.add("hidden")
                bookList.forEach((listing) => {
                    listing.remove();
                })
                //document.getElementById("pagenum").value = 1;
                
                if (currentUrl.slice(-3) === "all") {
                    resetBookFilter("series-filter", "world-filter", "");
                    // build new book listings
                    buildListing(data.books, data, currentUrl.slice(0, -3));
                    document.getElementById("stop-scrolling").innerHTML = "False";
                }
                else {
                    // clear additional lore filters
                    document.getElementById("selected-type").classList.add("hidden");
                    resetLoreFilter("series-filter", "world-filter", "type-filter", "")
                    //build lore listing
                    buildLoreListing(data.lore_data, data, currentUrl.slice(0, -3));
                    document.getElementById("stop-scrolling").innerHTML = "False";
                }
                document.querySelector(".fetch-results").classList.add("hidden");
            }
        });
        return false;
    }
}

// Function to reset book filter
function resetBookFilter(seriesId, worldId, valueToSelect) {
    document.getElementById("pagenum").value = 1;
    let seriesElement = document.getElementById(seriesId);
    let worldElement = document.getElementById(worldId)
    seriesElement.value = valueToSelect;
    worldElement.value = valueToSelect;
}

// Function to reset lore filter
function resetLoreFilter(seriesId, worldId, typeId, valueToSelect) {
    document.getElementById("pagenum").value = 1;
    let seriesElement = document.getElementById(seriesId);
    let worldElement = document.getElementById(worldId)
    let typeElement = document.getElementById(typeId);
    seriesElement.value = valueToSelect;
    worldElement.value = valueToSelect;
    typeElement.value = valueToSelect;
}

// Function to build lore results from filters
function buildLoreListing(lore, data, currentUrl) {
    const booklistContainer = document.getElementById("booklist-container");
    for (i = 0; i < lore.length; i++) {
        // build each lore listing, append to booklistContainer
        const bookListingDiv = document.createElement("div");
        bookListingDiv.classList.add("book-listing", "hori", "fade-in");
        // create image elements
        const imageDiv = document.createElement("div");
        imageDiv.classList.add("vert", "image-div");
        const picture = document.createElement("picture");
        const sourceAvif = document.createElement("source");
        sourceAvif.srcset = "static/placeholder.avif";
        sourceAvif.type = "image/avif";
        const image = document.createElement("img");
        image.src = currentUrl + "static/placeholder.jpg";
        image.alt = lore[i].name;
        image.classList.add("small-img");
        picture.appendChild(sourceAvif);
        picture.appendChild(image);
        imageDiv.appendChild(picture);
        bookListingDiv.appendChild(imageDiv);
        // create main content elements
        const contentDiv = document.createElement("div");
        contentDiv.classList.add("vert");
        // create title
        const titleDiv = document.createElement("div");
        titleDiv.classList.add("hori", "listing-title");
        const titleParagraph = document.createElement("p");
        titleParagraph.innerHTML = lore[i].name;
        titleDiv.appendChild(titleParagraph);
        // series div
        const seriesDiv = document.createElement("div");
        seriesDiv.classList.add("hori");
        const seriesName = document.createElement("a");
        seriesName.id = `object-series-${lore[i].name}`;
        if (lore[i].series_id === null) {
            seriesName.innerHTML = "Various";
        }
        else {
            seriesName.innerHTML = data.series_list[parseInt(lore[i].series_id) - 1].name;
            seriesName.href = currentUrl + "all/series/" + lore[i].series_id;
        }
        const seriesLabel = document.createElement("label");
        seriesLabel.for = seriesName.id;
        seriesLabel.innerHTML = "Series:";
        seriesDiv.appendChild(seriesLabel);
        seriesDiv.appendChild(seriesName);
        // world div
        const worldDiv = document.createElement("div");
        worldDiv.classList.add("hori");
        const worldName = document.createElement("a");
        worldName.id = `object-world-${lore[i].title}`;
        worldName.innerHTML = data.worlds[parseInt(lore[i].world_id) - 1].name;
        worldName.href = currentUrl + "all/world/" + lore[i].world_id;
        const worldLabel = document.createElement("label");
        worldLabel.for = worldName.id;
        worldLabel.innerHTML = "World:";
        worldDiv.appendChild(worldLabel);
        worldDiv.appendChild(worldName);
        //type div
        const typeDiv = document.createElement("div");
        typeDiv.classList.add("hori");
        const typeP = document.createElement("p");
        typeP.id = `object-type-${lore[i].title}`;
        typeP.innerHTML = lore[i].type;
        const typeLabel = document.createElement("label");
        typeLabel.for = typeP.id;
        typeLabel.innerHTML = "Type:";
        typeDiv.appendChild(typeLabel);
        typeDiv.appendChild(typeP);
        // synopsis div
        const synopsisDiv = document.createElement("div");
        const synopsisP = document.createElement("p");
        synopsisP.id = `object-description-${lore[i].id}`;
        synopsisP.classList.add("synopsis")
        synopsisP.innerHTML = lore[i].description;
        const synopsisLabel = document.createElement("label");
        synopsisLabel.for = synopsisP.id;
        synopsisLabel.innerHTML = "Description:";
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
        // append together
        contentDiv.appendChild(titleDiv);
        contentDiv.appendChild(seriesDiv);
        contentDiv.appendChild(worldDiv);
        contentDiv.appendChild(typeDiv);
        contentDiv.appendChild(synopsisDiv);
        bookListingDiv.appendChild(contentDiv);
        booklistContainer.appendChild(bookListingDiv);
    }
}

// Function to display more of the synopsis
function showMore() {
    var synopsis = this.parentElement.previousElementSibling;
    if (this.innerHTML === "See more") {
        synopsis.classList.add("expanded");
        this.style.marginTop = "0";
        this.parentElement.style.height = "2rem";
        this.innerHTML = "See less";
    }
    else {
        synopsis.classList.remove("expanded");
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

// Function to copy email address to the clipboard
function copyText() {
    let email = document.getElementById("email-address");
    let emailText = email.innerHTML;
    navigator.clipboard.writeText(emailText);
    document.querySelector(".tooltip-text").innerHTML = "Email Copied!";
    setTimeout(function () {
        document.querySelector(".tooltip-text").innerHTML = "Copy Email to Clipboard";
    }, 3000);
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
    else {
        this.style.opacity = "50%";
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
                        document.getElementById(`wish-element-${bookId}`).children[1].classList.add("hidden");
                        document.getElementById(`wish-element-${bookId}`).children[0].classList.add("hidden");
                        document.getElementById(`wish-btn-${bookId}`).innerHTML = "Undo";
                    }
                    else {
                        document.getElementById(`wish-element-${bookId}`).children[1].classList.remove("hidden");
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
                    document.getElementById("wish-btn").style.opacity = "100%";
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
    else {
        this.style.opacity = "50%";
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
                        document.getElementById(`follow-element-${seriesId}`).children[1].classList.add("hidden");
                        document.getElementById(`follow-element-${seriesId}`).children[0].classList.add("hidden");
                        document.getElementById(`follow-btn-${seriesId}`).innerHTML = "Undo";
                    }
                    else {
                        document.getElementById(`follow-element-${seriesId}`).children[1].classList.remove("hidden");
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
                    document.getElementById("follow-btn").style.opacity = "100%";
                }
            }
        });
        return false;
    }
}
