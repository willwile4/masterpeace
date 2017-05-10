//js file to turn an image into a blob, then store the blob in our API.

//this function shows a preview of the img on the screen.
function textToImg() {
  //get ascii string into binary then into an array then into a blob.
  var elem = document.getElementById('form-image');
  var file = elem.getAttribute('value');
  var displayArea = document.getElementById('form-image-preview');
  img = document.getElementById('form-image-preview');
  img.src = file;
}

//turns an image into a blob
function imgToText() {
    // get file elem and get image
    var file = document.getElementById('form-image').files[0];
    var imgField = document.getElementById('form-image');
    //open a file reader and read in file, then turn it from binary to ascii
    var reader = new FileReader();
    reader.onload = function(event) {
        var contents = event.target.result;
        //turn to ascii string
        var asciiContents = btoa(contents);
        var fileType = file.type
        console.log(file);
        console.log(fileType);
        imgField.setAttribute('value', "data:" + fileType + ";base64," + asciiContents);
    };
    reader.onerror = function(event) {
        console.error('error, file could not be read');
    };
    reader.onloadend = function(event) {
        textToImg();
    };
    //read file as a bit string
    reader.readAsBinaryString(file);
    // TODO send data via ajax to our DB our restful API

}

//add click event so that image is processed upon submit
var imgf = document.getElementById('form-image');
imgf.addEventListener('change', imgToText);
