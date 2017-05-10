//js file to edit a user's profile upon registration.
//currently getting a


var csrftoken = $('[name="csrfmiddlewaretoken"]').val();


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
    var user =  $('[name="user_id"]').val();
    var profile = $('[name="profile"]').val();
    var isChecked = $("#checkbox").prop("checked");
    var $form = {
        "user": user,
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'pic': $("#form-image").attr('value'),
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
            window.location.replace('/profile/' + user)

    }
  };
    $.ajax(settings);
}

$('#submitChanges').click(editProfile);
