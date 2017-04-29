
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
    console.log($('#createProfile :input'));
    // var $post_data = $("#createProfile :input");

    // for(var i = 0; i < $post_data.length; i++) {
    //     console.log($post_data);
    // //     if(!$post_data[i].attr('id', '#create_profile')) {
    // //         $form[$post_data[i].name] = $post_data[i].value
    // //   }
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
