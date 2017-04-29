//js file to create a user's profile upon registration.
//known bugs: any user can create a profile for user's without a profile.

function createProfile(e) {
    e.preventDefault();
    let $form = {
        "user": $('[name="user_id"]').val(),
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'pic': $('[name="pic"]').val(),
        'bio': $('[name="bio"]').val(),
        'fb_link': $('[name="fb_link"]').val(),
        'insta_link': $('[name="insta_link"]').val(),
        'twitter_link': $('[name="twitter_link"]').val(),
        'allow_messages': $('[name="allow_messages"]').val(),
    };

    var settings = {
        method: "POST",
        url: '/api/profile/',
        data: $form,
        success: function(result) {
            console.log('success')
    }
    }
    $.ajax(settings);
};


$('#create_profile').click(createProfile);
