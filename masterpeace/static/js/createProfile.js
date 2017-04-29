//js file to create a profile via ajax. users are directed here upon registration.
//known bug: any user can update any profile 4/28

function createProfile(e) {
    e.preventDefault();
    var post_data = { 'bio': $('#bio').val(),
                      'allow_messages': false, //$('#allowMessages').val(),
                      'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                      'user': $('#user_id').val(),
                      'user_id': $('#user_id').val(),
        };
    var settings = {
        method: "POST",
        url: '/api/profile/',
        data: post_data,
    }
    $.ajax(settings);
};


$('#create_profile').click(createProfile);
