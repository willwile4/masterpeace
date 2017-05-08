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

let filename = $('#form-image').val()
for(var i = 0; i < filename.length; i++) {
    if (filename[i] === '.') {
        fileType = filename.slice([i]);
    }
}

function editProfile(e) {
    e.preventDefault();
    let user =  $('[name="user_id"]').val();
    let profile = $('[name="profile"]').val();
    let $form = {
        "user": user,
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'pic': "data:image/" + fileType + "png;base64," + $("#form-image").attr('value'),
        'bio': $('[name="bio"]').val(),
        'fb_link': $('[name="fb_link"]').val(),
        'insta_link': $('[name="insta_link"]').val(),
        'twitter_link': $('[name="twitter_link"]').val(),
        'allow_messages': false,// fix this plz k thx $('[name="allow_messages"]').val(),
    };
    console.log($form);
    var settings = {
        // headers: {
        //    'X-HTTP-Method-Override': 'PATCH'
        // },
        method: 'PATCH',
        url: '/api/profile/' + profile + '/',
        // contenttype: application/json,
        data: $form,
        success: function(result) {
            console.log('success');
             history.go(-1);
    }
  };
    $.ajax(settings);
}

$('#submitChanges').click(editProfile);
