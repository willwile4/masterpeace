//js file to edit a user's profile upon registration.
//currently getting a


let csrftoken = $('[name="csrfmiddlewaretoken"]').val();


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function editProfile(e) {
    e.preventDefault();
    let user =  $('[name="user_id"]').val();
    let profile = $('[name="profile"]').val();
    var isChecked = $("#checkbox").prop("checked");
    var filename = $('#form-image').val();
    for(var i = 0; i < filename.length; i++) {
        if (filename[i] === '.') {
            var fileType = filename.slice([i]);
        }
    }
    let $form = {
        "user": user,
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
        method: 'PATCH',
        url: '/api/profile/' + profile + '/',
        data: $form,
        success: function(result) {
            console.log('success');
            window.location.replace("/profile/" + user);
    }
  };
    $.ajax(settings);
}

$('#submitChanges').click(editProfile);
