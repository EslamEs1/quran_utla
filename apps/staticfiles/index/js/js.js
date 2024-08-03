$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        items: 3, // Number of items to display
        loop: true, // Enable looping
        margin: 30, // Margin between items
        nav: true, // Show navigation
        autoplay: true, // Enable autoplay
        autoplayTimeout: 3000, // Autoplay interval in milliseconds
        responsive: {
            0: {
                items: 1, // Number of items to display on small screens
            },
            600: {
                items: 3, // Number of items to display on medium screens
            },
            1000: {
                items: 3, // Number of items to display on large screens
            },
        },
    });
});
