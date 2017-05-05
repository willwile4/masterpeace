//js file to turn an image into a blob, then store the blob in our API.
// next: retrive the blob and put it on the page

function textToImg(text) {
  //get ascii string into binary then into an array then into a blob.
  let elem = document.getElementById('image');
  let file = elem.getAttribute('value');
  let displayArea = document.getElementById('preview');
  console.log(file, typeof(file));

  img = document.getElementById('preview');
  img.src = "data:image/png;base64," + file;
  //displayArea.append(img);
  // TODO get data via ajax to our DB our restful API
}

//turns an image into a blob
function imgToText() {
    // get file elem and get image
    let file = document.getElementById('image').files[0];
    let imgField = document.getElementById('image');
    //open a file reader and read in file, then turn it from binary to ascii
    var reader = new FileReader();
    reader.onload = function(event) {
        let contents = event.target.result;
        //turn to ascii string
        let asciiContents = btoa(contents);
        imgField.setAttribute('value', asciiContents);
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

};

//add click event so that image is processed upon submit
var imgf = document.getElementById('image');
console.log(imgf);
imgf.addEventListener('change', imgToText);
