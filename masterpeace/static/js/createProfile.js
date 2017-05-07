//js file to create a user's profile upon registration.
//currently posting pic as a text file, but default appears in api.
//should be the value attr of the input element, which is the ascii string.

function createProfile(e) {
    e.preventDefault();
    console.log('hi mom');
    console.log(e);
    let $form = {
        "user": $('[name="user_id"]').val(),
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'pic': "data:64;base64," + $("#form-image").attr('value'),
        'bio': $('[name="bio"]').val(),
        'fb_link': $('[name="fb_link"]').val(),
        'insta_link': $('[name="insta_link"]').val(),
        'twitter_link': $('[name="twitter_link"]').val(),
        'allow_messages': false, // fix this plz k thx $('[name="allow_messages"]').val(),
    };
    console.log($form);
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
