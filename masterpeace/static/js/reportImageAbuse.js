//js file to report abusive users, increases report count in models, and
//notifies an administrator.


//notify admin by sending a message
function reportImageAbuse(e) {
    let post_id = $(this).attr('id');
    let reporting_user = $(this).attr('user');
    let $form = {
        'post_id': post_id,
        'reporting_user': reporting_user,
        }
    $.ajax({
        method: 'POST',
        url: 'api/abusive_image_report/',
        data: $form,
        success: function(result) {
            $('#success-msg').empty();
            $('#post_'+ post_id).append('<p id="success-msg">Post Reported! Thank you!</p>');
            $('#success-msg').delay(1000).fadeOut();
        },
        error: function(result) {
            $('#error-msg').empty();
            $('#post_' + post_id).append("<p id='error-msg' Something went wrong, please try again!");
            $('#error-msg').delay(1000).fadeOut();
        },
    })
}

$('.report-image').one('click', reportImageAbuse);
