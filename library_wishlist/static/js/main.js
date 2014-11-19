var searchResults = [];

initItemCompletedEvent($('.wishlist-completed'));

$('.wishlist-dropdown').on('click', function(e) {
    e.preventDefault();
    $(this).parent().siblings('.copies').collapse('toggle');
    $(this).children('.glyphicon')
        .toggleClass('glyphicon-chevron-down')
        .toggleClass('glyphicon-chevron-up');
});
$('.wishlist-collapse-all').on('click', function(e){
    e.preventDefault();
    $('.copies').collapse('show');
    $('.wishlist-dropdown').find('.glyphicon')
        .toggleClass('glyphicon-chevron-down')
        .toggleClass('glyphicon-chevron-up');
});

$("#create-form").submit(function() {
    var textField = $('#id_text');
    var submitButton = $('.wishlist-submit');

    if (textField.val() === '') return false;
    else submitButton.button('loading');

    $.post("/item/", {
            text: textField.val(),
            user_id: user_id,
            csrfmiddlewaretoken: csrf
        },
        function(data, status) {
            if (typeof data === "object") {
                initSearchResults(data);
            } else {
                $('.items').first().before(data);
                initItemCompletedEvent($('.items').first().find('.wishlist-completed'));
            }

            resetItemForm();

        })
        .fail(function(xhr) {
            console.log("Error: " + xhr.statusText);
            $(".search-results").empty().append("Kein Treffer unter <strong>\"" + textField.val() + "\"</strong> im GGG Katalog gefunden.");
            resetItemForm();
        });
    return false;
});

function resetItemForm() {
    var textField = $('#id_text');
    var submitButton = $('.wishlist-submit');

    submitButton.button('reset');
    textField.val('');

    $('.wishlist-dropdown').on('click', function(e) {
        e.preventDefault();
        $(this).parent().siblings('.copies').collapse('toggle');
        $(this).children('.glyphicon')
            .toggleClass('glyphicon-chevron-down')
            .toggleClass('glyphicon-chevron-up');
    });
}

function initItemCompletedEvent(items) {
    $.each(items, function(index, item) {
        $(item).on('click', function(e) {
            var id = $(this).data('id');
            completeItem(id);
        });
    });
}

function initSearchResults(data) {
    searchResults = [];
    $(".search-results").empty().append("<p><strong>Es wurden mehrere Suchergebnisse gefunden. Bitte das Gewünschte auswählen.</strong></p>");
    for (var i = 0; i < data.length; i++) {
        $(".search-results").append("<p><a href='#' data-index='" + i + "'>" + data[i].name + "</a></p>");
        searchResults.push(data[i]);
    }
    $(".search-results a").on("click", function(e) {
        e.preventDefault();
        var index = parseInt($(this).attr("data-index"));
        var item = JSON.stringify(searchResults[index]);

        $.ajax({
            type: "POST",
            url: "/itemSearchResult/",
            contentType: "application/json",
            data: item,
            dataType: "html",
            success: function(data, status) {
                $('.items').first().before(data);
                initItemCompletedEvent($('.items').first().find('.wishlist-completed'));
                resetItemForm();
                $(".search-results").empty();
            },
            error: function(xhr, status) {
                console.log("Error: " + xhr.statusText);
                resetItemForm();
            }
        });
        return false;

    });
}

function completeItem(id) {
    $.post("/item/" + id + '/', {
            itemId: id,
            completed: true,
            csrfmiddlewaretoken: csrf
        },
        function(data, status) {
            // console.log("Data: " + data + "\nStatus: " + status);
        })
        .fail(function(xhr) {
            // console.log("Error: " + xhr.statusText);
        })
        .success(function(xhr) {
            $('#item-' + id).fadeOut(function() {
                $(this).remove();
            });
        });
    return false;
}

// CSRF Protection

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
