//js file to edit a user's profile upon registration.
//currently getting a

function editProfile(e) {
    e.preventDefault();
    let user =  $('[name="user_id"]').val()
    let $form = {
        "user": user,
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        'pic': $("#form-image").attr('value'),
        'bio': $('[name="bio"]').val(),
        'fb_link': $('[name="fb_link"]').val(),
        'insta_link': $('[name="insta_link"]').val(),
        'twitter_link': $('[name="twitter_link"]').val(),
        'allow_messages': false,// fix this plz k thx $('[name="allow_messages"]').val(),
    };
    console.log($form);
    var settings = {
        headers: {
           'X-HTTP-Method-Override': 'PATCH'
        },
        url: '/api/profile/' + user + '/',
        Content-Type: 'application/json',
        data: $form,
        success: function(result) {
            console.log('success');
    }
    }
    $.ajax(settings);
};

$('#submitChanges').click(editProfile);
