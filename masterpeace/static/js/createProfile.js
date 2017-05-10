//js file to create a user's profile upon registration.

function createProfile(e) {
    e.preventDefault();
    var isChecked = $("#checkbox").prop("checked");
    let $form = {
        "user": $('[name="user_id"]').val(),
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
