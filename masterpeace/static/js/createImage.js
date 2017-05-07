//may need to initialize feedback 1-5 at 0, feedback is apart of the serializer.
//file to create a new image masterpeace post

function createImage(event) {
    event.preventDefault();
    let $form = {
      'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
      'tag': $('[name="tag"]').val(),
      'title': $('[name="title"]').val(),
      'owner': $('[name="owner"]').val(),
      'image': "data:image/png;base64," + $("#form-image").attr('value'),
      'artform': $('[name="artform"]').val(),
      'caption': $('[name="caption"]').val(),
      'allow_feedback': true,
      'feedback1': 0,
      'feedback2': 0,
      'feedback3': 0,
      'feedback4': 0,
      'feedback5': 0,
    }
    console.log($form);
    $.ajax({
        method: 'POST',
        url: "/api/image_mp/",
        data: $form,
        success: function(result) {
            console.log('success');
            window.location.replace("/");
        }
    });
}

console.log('hi there line 10');
$('#submitBtn').click(createImage);
