$('.wishlist-completed').on('click', function(e){
    completeItem($(this));
});

$('.wishlist-dropdown').on('click', function(e){
    e.preventDefault();
    $(this).parent().siblings('.copies').collapse('toggle');
    $(this).children('.glyphicon')
        .toggleClass('glyphicon-chevron-down')
        .toggleClass('glyphicon-chevron-up')
});

$("#create-form").submit(function(){
    var textField = $('#id_text');
    var submitButton = $('.wishlist-submit');

    submitButton.button('loading');
    if (textField.val() == '') return false;

    $.post("/item/", {
        text: textField.val(),
        csrfmiddlewaretoken: csrf
     },
    function(data,status){
        if (typeof data === "object") {
            for (var i=0; i < data.length; i++) {
                    $(".suggestions").append("<p><a href='#' data-index='"+i+"'>"+data[i].name+"</a></p>");
            }
        } else {
            $('.items').first().before(data);
        }

        $('.wishlist-completed').on('click', function(e){
          completeItem($('.items').first());
        });
        resetItemForm();

    })
    .fail(function(xhr) {
        console.log("Error: " + xhr.statusText);
        resetItemForm();
    })
    return false;
});

function resetItemForm(){
    var textField = $('#id_text');
    var submitButton = $('.wishlist-submit');

    submitButton.button('reset');
    textField.val('')

    $('.wishlist-dropdown').on('click', function(e){
        e.preventDefault();
        $(this).parent().siblings('.copies').collapse('toggle');
        $(this).children('.glyphicon')
            .toggleClass('glyphicon-chevron-down')
            .toggleClass('glyphicon-chevron-up')
    });
}

function completeItem(element){
    var element = element;
    var id = element.data('id');
    $.post("/item/"+id+'/', {
        itemId: id,
        completed: true,
        csrfmiddlewaretoken: csrf
     },
    function(data,status){
        // console.log("Data: " + data + "\nStatus: " + status);
    })
    .fail(function(xhr) {
        // console.log("Error: " + xhr.statusText);
    })
    .success(function(xhr) {
        $('#item-'+id).fadeOut(function(){
            element.remove();
        })
    });
    return false;
}

// CSRF Protection

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
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
