//js file to report abusive users, increases report count in models, and
//notifies an administrator.

function reportImageAbuse(e) {
    console.log("hi");
    let post_id = $(this).attr('id');
    let reporting_user = $(this).attr('user');
    let $form = {
        'post_id': post_id,
        'reporting_user': reporting_user,
        }
    console.log($form);
    $.ajax({
        method: 'POST',
        url: 'api/abusive_image_report/',
        data: $form,
        success: function(result) {
            $('#post_'+ post_id).append('<p id="success-msg">Post Reported! Thank you!</p>');
            $('#success-msg').hide(1100).fadeOut();
        },
        error: function(result) {
            $('#post_' + post_id).append("<p id='error-msg' Something went wrong, please try again!");
            $('#error-msg').hide(1100).fadeOut();
        },
    })
}

$('.report-image').one('click', reportImageAbuse);
