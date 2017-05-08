//js file to create a user's profile upon registration.

function createProfile(e) {
    e.preventDefault();
    console.log('hi mom');
    console.log(e);
    var isChecked = $("#checkbox").prop("checked");
    let filename = $('#form-image').val()
    for(var i = 0; i < filename.length; i++) {
        if (filename[i] === '.') {
            fileType = filename.slice([i]);
        }
    }
    let $form = {
        "user": $('[name="user_id"]').val(),
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'pic': "data:image/" + fileType + ";base64," + $("#form-image").attr('value'),
        'bio': $('[name="bio"]').val(),
        'fb_link': $('[name="fb_link"]').val(),
        'insta_link': $('[name="insta_link"]').val(),
        'twitter_link': $('[name="twitter_link"]').val(),
        'allow_messages': isChecked,
    };
    console.log($form);
    var settings = {
        method: "POST",
        url: '/api/profile/',
        data: $form,
        success: function(result) {
            console.log('success')
            window.location.replace('/profile/' + $('[name="user_id"]').val() + '/')
      }
    }
    $.ajax(settings);
};


$('#create_profile').click(createProfile);
