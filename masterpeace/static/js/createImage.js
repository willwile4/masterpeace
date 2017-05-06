//may need to initialize feedback 1-5 at 0, feedback is apart of the serializer.
//file to create a new image masterpeace post

function createImage() {
    console.log("create");
    $form = {
      'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val(),
      'tag': $('[name="tag"]')
    $form.append('tag', )

}

console.log('hi there line 10');
$('#submitBtn').click(createImage);
