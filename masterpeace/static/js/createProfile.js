console.log('js works here');

function createProfile(e) {
    e.preventDefault();
    console.log('hi mom');
    var post_data = { 'bio': $('#bio').val(),
                      'allow_messages': false, //$('#allowMessages').val(),
                      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                      'user': $('#user_id').val(),
        };
    console.log(post_data);
    var settings = {
        method: "POST",
        url: '/api/profile/',
        data: post_data,
    }
    $.ajax(settings);
};


$('#create_profile').click(createProfile);
