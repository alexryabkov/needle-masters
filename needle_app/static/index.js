//jQuery to collapse the navbar on scroll
$(window).scroll(function() {
    if ($('.navbar').offset().top > 50) {
        $('.navbar-fixed-top').addClass('top-nav-collapse');
    } else {
        $('.navbar-fixed-top').removeClass('top-nav-collapse');
    }
});


$(function() {
    //jQuery for page scrolling feature - requires jQuery Easing plugin
    $(document).on('click', 'a.page-scroll', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });

    // "Lightcase" plugin stuff
    $('a[data-rel^=lightcase]').lightcase();

    // Validate Contact form
    $("#contact-form").validate();
});


// AJAX wrapper for pagination
function getImageData(categ, num) {
    var request_url = '/' + categ + '/' + num;
    var item_col = '.' + categ + '-item';

    $(item_col).show().css('opacity', 0);
    console.log("getImageData called!");
    $.ajax({
        // Triggering "gallery_pagination" server method
        url: request_url,
        success: function(response) {
            console.log(request_url + ': ' + response);
            $(item_col).each(function(index) {
                if (index < response.length) {
                    $(this).find('a').attr('href', response[index].filepath);
                    $(this).find('img').attr('src', response[index].filepath);
                    $(this).find('.price').text(response[index].item_price + " руб.");
                    $(this).find('.item-name').text(response[index].item_name);
                    $(this).find('p').text(response[index].description);
                    $(this).animate({
                        opacity: 1
                    }, 1000);
                } else {
                    $(this).hide();
                };
            });
        },
        error: function(error) {
            console.log(error);
        }
    });
};

// "Bootpag" plugin init function
function paginateImages(pages_per_category) {
    $(function() {
        for (categ in pages_per_category) {
            getImageData(categ, 1);
            $('div[id^=' + categ + '-pagination]').bootpag({
                total: pages_per_category[categ],
                maxVisible: 4,
                firstLastUse: true,
                first: '<span aria-hidden="true">&laquo;</span>',
                prev: '<span aria-hidden="true">&lsaquo;</span>',
                next: '<span aria-hidden="true">&rsaquo;</span>',
                last: '<span aria-hidden="true">&raquo;</span>'
            }).on('page', function(event, num) {
                // In case of rapid page switch we should stop any
                // currently running animation and start new page handling
                $(':animated').stop(true, true);
                getImageData(event.currentTarget.id.split('-pagination')[0],
                    num);
            });
        };
    });
};
