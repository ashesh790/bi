// function for add and remove class from navigation menu bar 

$(document).ready(function () {
    $(this).click(function () {
        $('.nav-item .nav-link.active').removeClass('active');
        $('.nav-item .nav-link').addClass("active");
    });
});