//js file to create an image masterpeace
//need to initialize feedback 1-5 at 0, feedback is apart of the serializer.
//file to create a new image masterpeace post

function createImage(event) {
    event.preventDefault();
    let isChecked = $("#checkbox").prop("checked");
    let filename = $('#form-image').val()
    for(var i = 0; i < filename.length; i++) {
        if (filename[i] === '.') {
            fileType = filename.slice([i+1]);
        }
    }
    let $form = {
      'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
      'title': $('[name="title"]').val(),
      'owner': $('[name="owner"]').val(),
      'image': "data:image/" + fileType + ";base64," + $("#form-image").attr('value'),
      'artform': $('[name="artform"]').val(),
      'caption': $('[name="caption"]').val(),
      'tag': $('[name="tag"]').val(),
      'allow_feedback': isChecked,
      'feedback1': 0,
      'feedback2': 0,
      'feedback3': 0,
      'feedback4': 0,
      'feedback5': 0,
    }


    $.ajax({
        method: 'POST',
        url: "/api/image_mp/",
        data: $form,
        traditional: true;
        success: function(result) {
            console.log('success');
            window.location.replace("/");
        }
    });
}

$('#submitBtn').click(createImage);
