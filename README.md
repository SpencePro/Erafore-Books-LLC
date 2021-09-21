# Erafore Books LLC

### Overview

This is the website for the company Erafore Books LLC, which was created by Ian Rodgers. The books are self-published and sold through Amazon. Ian Rodgers specializes in Fantasy and Science Fiction works, creating series of books, standalone novels, and collections of short stories. This website was created as a way to increase the company's internet presence and exposure for marketing purposes. It was also created as a practical test/demonstration of my abilities as a developer, and as a learning experience, it has been invaluable. 

### Tech Stack

The website is built using the following technologies:

- Django web framework
- JavaScript (vanilla)
- HTML5
- CSS3
- Bootstrap
- AJAX
- MySQL

It is deployed with Heroku. Images were edited with GIMP editing software. 

### Features

The website is a full-featured web application with the following features:

- Display books and lore information from the database
- Filter the book and lore results based on various combinations of filters
- Infinite scroll to display books and lore
- Search function for books
- Allow users to create an account and sign in/out of the website
- Allow users to follow/unfollow series they like, and add/remove books to/from an individualized wishlist
- Email service set up to send emails to users to verify registration and reset password
- Email service also sends notifications of marketing (new book releases, books go on sale, series you follow are updated) by email to users who consent to receive them
- Allow users to update email settings to opt out of or allow various categories of emails to be sent to them
- Allow users to delete their account
- Desktop and mobile responsive for various screen sizes
- Optimized for Google Chrome, Firefox, and Microsoft Edge; soon to be tested in Safari 

### Design Decisions

The decision to use Django as the backend framework was due to its robustness as a "batteries included" web framework with especially strong security and database capabilities. Django's strong focus on security (such as requiring CSRF tokens for all POST requests, the inherent security of the ORM system for preventing SQL injection, and defenses against header injections for email messages sent) allowed me to focus on other aspects of the development and gave me the confidence to include user security aspects. I found Django's ORM system especially appealing for working with the database, as it sped up the creation of the database system and is, I find, more human-readable than a similar implementation in pure SQL would be. 

MySQL was chosen as the database as it is a highly scalable, widely used system with copious community support, ideal for small to mid-level databases, and perhaps more importantly, is natively supported by Django.

The design philosophy of the front end was to make it as user friendly as possible; to me, this meant giving as much feedback to the user as possible, and creating a smooth, seamless user experience. As a result, AJAX is used extensively to display new information to the user without reloading the page. A fade in effect is used in many places as I believe it is more aesthetically pleasing, even relaxing, to look at. Loading wheels from Bootstrap were added liberally throughout, where appropriate, to ensure users with slower internet connections are able to receive visual feedback on calls to the server, such as in logging in, registering, and loading more book results. 

An "infinite scroll" effect was used with AJAX and the backend to update the page content when the user scrolls to the bottom of the page. This was primarily done for performance purposes, to limit data transferred per call to the server; instead of transferring all of the data at once, potentially slowing down the loading of the webpage, this limits the amount of data sent to the client at a time. The infinite scrolling aspect of it was done for visual aethetic purposes and seamlessness of user experience. 

Images were edited with GIMP and then converted to .avif format (at the official website, [avif.io](https://avif.io/)) due to the excellent compression and quality retention of that format. Images are also included in .jpg format as a backup to account for .avif's relatively low (at time of writing) support among older browsers.