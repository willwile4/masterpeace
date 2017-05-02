function createMessage(e) {
    e.preventDefault();
    let $form = {
        "content": $('[name="content"]').val(),
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'to_user': $('[name="to_user"]').val(),
        'from_user': $('[name="from_user"]').val(),
    };

    var settings = {
        method: "POST",
        url: '/api/message/',
        data: $form,
        success: function(result) {
            console.log('success')
    }
    }
    $.ajax(settings);
    var content = $('[name="content"]').val()
    $('#messageList').append('<li class="sent"><span class="sent">' + content + '</span></li>');
    var content = document.getElementById("content")
    content.value = '';
};

$("#content").keypress(function (e) {
    if(e.which == 13 && !e.shiftKey) {
      createMessage(e);
    }
});
$('#create_message').click(createMessage);
