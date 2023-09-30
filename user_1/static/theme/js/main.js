// media query 
$(document).ready(function () {
    // Define the media query for average mobile devices
    var mediaQuery = window.matchMedia('(max-width: 820px)');

    // Function to handle the media query change
    if (mediaQuery.matches) {
        // Apply styles for average mobile devices
        $('.p_type_btn').addClass('col-4');
        $('.p_type_btn').removeClass('col-1');
    } else {
        // Remove styles for average mobile devices
        $('.p_type_btn').addClass('col-1');
        $('.p_type_btn').removeClass('col-4');
    }
});
(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();

    // Initiate the wowjs
    new WOW().init();

    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 45) {
            $('.nav-bar').addClass('sticky-top');
        } else {
            $('.nav-bar').removeClass('sticky-top');
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Header carousel
    $(".header-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1500,
        items: 1,
        dots: true,
        loop: true,
        nav: true,
        navText: [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 24,
        dots: false,
        loop: true,
        nav: true,
        navText: [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            992: {
                items: 2
            }
        }
    });

})(jQuery);

// for load place in website 
$(document).ready(function () {
    var auto_complete;
    var id = "place_name";
    auto_complete = new google.maps.places.Autocomplete((document.getElementById(id)), {
        types: ['geocode'],
    })
});

var x = document.getElementById("demo");
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    console.log(position);
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;
    console.log(lat, lng);
    $("#latitude").val(lat);
    $("#longitude").val(lng);
}
getLocation();

function toaster_call(message) {
    if (message == null || message == "") {
        return;
    }
    else {
        $.fn.toaster(message, {
            duration: 2000,
            position: "bottom-center",
        });
    }
}

/**
 * Makes an AJAX call to the specified URL using the given method, synchronous/asynchronous mode, and data.
 * @param {string} method - The HTTP method to use for the request (e.g., "GET", "POST").
 * @param {boolean} sync_async - Specifies whether the request should be synchronous (true) or asynchronous (false).
 * @param {string} url - The URL to which the request should be made.
 * @param {Object} data - The data to be sent with the request, in object format.
 * @returns {XMLHttpRequest} - The XMLHttpRequest object used to make the request.
 */
function ajax_call(method, sync_async, url, data) {
    const xhr = new XMLHttpRequest();

    // Create a new XMLHttpRequest object 
    xhr.open(method, url, sync_async);

    if (method === "POST" || method === "post") {
        const csrftoken = $("[name=csrfmiddlewaretoken]").val();
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
    }

    // Set the request headers
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    // Convert the data to JSON format
    const jsonData = JSON.stringify(data);


    // Send the request
    xhr.send(jsonData);

    // Define the callback function to handle the response
    xhr.onreadystatechange = function () {

        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                console.log(xhr)
                return xhr.data;
            } else {
                // Request encountered an error
                console.log(xhr.status + ': ' + xhr.responseText);
                toaster_call("Error..");
            }
        }
    };
}
