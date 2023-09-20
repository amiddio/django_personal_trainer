var csrftoken = $("[name=csrfmiddlewaretoken]").val();
var url_login = '/account/login';

function like() {

    var like = $(this);
    var model = like.data('model');
    var pk = like.data('id');
    var action = like.data('action');
    var dislike = like.next();

    $.ajax({
        url: "/vote/" + model + "/" + action,
        type: 'POST',
        data: {'pk': pk},
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(data) {
            like.find("[data-count='like']").text(data.like_count);
            dislike.find("[data-count='dislike']").text(data.dislike_count);
        },
        statusCode: {
            500: function() {
                console.error("Internal server error on module LikeDislike");
            },
            401: function() {
                window.location.href = url_login;
            }
        }
    });
}

function dislike() {

    var dislike = $(this);
    var model = dislike.data('model');
    var pk = dislike.data('id');
    var action = dislike.data('action');
    var like = dislike.prev();

    $.ajax({
        url: "/vote/" + model + "/" + action,
        type: 'POST',
        data: {'pk': pk},
        beforeSend: function(xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        },
        success: function(data) {
            like.find("[data-count='like']").text(data.like_count);
            dislike.find("[data-count='dislike']").text(data.dislike_count);
        },
        statusCode: {
            500: function() {
                console.error("Internal server error on module LikeDislike");
            },
            401: function() {
                window.location.href = url_login;
            }
        }
    });
}

$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});
