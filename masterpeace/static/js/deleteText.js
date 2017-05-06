
let csrftoken = $('[name="csrfmiddlewaretoken"]').val();

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function delete_textMP(e) {
  console.log(e);
  console.log(e.target.id);
    e.preventDefault();
    console.log(e);
    var settings = {
        method: "DELETE",
        url: '/api/text_mp/' + e.target.id,
        success: function(result) {
            console.log('success')
            location.reload();
    }
  }
    $.ajax(settings);
};

function delete_imageMP(e) {
  console.log(e);
  console.log(e.target.id);
    e.preventDefault();
    console.log(e);
    var settings = {
        method: "DELETE",
        url: '/api/image_mp/' + e.target.id,
        success: function(result) {
            console.log('success')
            location.reload();
    }
  }
    $.ajax(settings);
};


$('.delete_text').click(delete_textMP);
$('.delete_image').click(delete_imageMP);
