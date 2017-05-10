function createTextFeedback(e) {
    e.preventDefault();
    var $icon = e.currentTarget.id;
    var $mp_id = e.currentTarget.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id;
    let $form = {
        "critic": $('[name="critic_id"]').val(),
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        "masterpeace": $mp_id,
        "icon": $icon,
    };
    var settings = {
        method: "POST",
        url: '/api/text_feedback/',
        data: $form,
        success: function(result) {
            console.log('success')
    }
  }
    $.ajax(settings);
    // console.log($("#" + $icon + ".counter"));
    var feedbackCounter = parseInt($("#" + $icon + ".counter")['0'].innerHTML);
    // console.log(feedbackCounter);
    $("#" + $icon + ".counter").html(feedbackCounter + 1);
};

function createImageFeedback(e) {
    e.preventDefault();
    console.log('image feedback form');
    // console.log(e);
    var $icon = e.currentTarget.id;
    var $mp_id = e.currentTarget.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.id;
    let $form = {
        "critic": $('[name="critic_id"]').val(),
        'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
        "masterpeace": $mp_id,
        "icon": $icon,
    };
    // console.log($form);
    var settings = {
        method: "POST",
        url: '/api/image_feedback/',
        data: $form,
        success: function(result) {
            console.log('success')
      }
    }
    $.ajax(settings);
    // var counters = $('.counter').length;
    var feedbackCounter = parseInt($("#" + $icon + ".counter")['0'].innerHTML);
    // console.log(feedbackCounter);
    $("#" + $icon + ".counter").html(feedbackCounter + 1);
};

$('.text_feedback_button').click(createTextFeedback);
$('.image_feedback_button').click(createImageFeedback);
