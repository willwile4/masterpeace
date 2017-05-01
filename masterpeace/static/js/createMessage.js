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
};


$('#create_message').click(createMessage);
