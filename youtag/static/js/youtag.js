"use strict";

$(document).ready(function() {
    var nav = $('nav');
    var navTop = nav.offset().top;
    var navHeight = nav.outerHeight();
    var navPlaceholder = $('.nav-placeholder');
    navPlaceholder.height(navHeight);

    $(window).scroll(function() {
        var scrollPos = $(this).scrollTop();
        //console.log(scrollPos);
        if (scrollPos > navTop) {
            nav.addClass('nav-fixed');
            navPlaceholder.show();
        } else {
            nav.removeClass('nav-fixed');
            navPlaceholder.hide();
        }
    });

    $("#urlForm").validate({
        rules: {
            video: {
                required: true,
                youTubeUrlOnly: true
            },
            tag: {
                required: true
            }
        },
        messages: {
            video: {
                required: "Please enter a valid Youtube url",
                id_video: "The url should begin with http://wwwyoutube.com/..."
            },
            tag: "Please enter valid tags separated by commas"
        }
    });
});

jQuery.validator.addMethod("youTubeUrlOnly", function(value, element) {
    return this.optional(element) || /^.+youtube.com/.test(value);
}, "Only Youtube url only are allowed.");