//js file to report text abuse

function reportTextAbuse(e) {
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
        url: 'api/abusive_text_report/',
        data: $form,
        success: function(result) {
            $('#post_'+ post_id).append('<p id="success-msg">Post Reported! Thank you!</p>');
            $('#success-msg').hide(1100).fadeOut();
        },
        error: function(result) {
            $('#post_' + post_id).append("<p id='error-msg' Something went wrong, please try again!");
            $('#error-msg').delay(1100).fadeOut();
        },
    })
}

$('.report-text').one('click', reportTextAbuse);
