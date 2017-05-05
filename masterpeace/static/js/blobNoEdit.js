//js file to turn an image into a blob, then store the blob in our API.


//this is a reference file. Please Do Not Alter!!
function textToImg(text) {
  //get ascii string into binary then into an array then into a blob.
  let file = document.getElementById('fileDisplayArea').innerHTML;
  let displayArea = document.getElementById('imageDisplay')
  console.log(file, typeof(file));

  img = document.createElement('img');
  img.src = "data:image/png;base64," + document.getElementById('fileDisplayArea').innerHTML;
  displayArea.append(img);
  // TODO get data via ajax to our DB our restful API
}

//turns an image into a blob
function imgToText() {
    // get file elem and get image
    let file = document.getElementById('imgFile');
    let img = document.getElementById('imgFile').files[0];
    let displayArea = document.getElementById('fileDisplayArea');
    //open a file reader and read in file, then turn it from binary to ascii
    var reader = new FileReader();
    reader.onload = function(event) {
        let contents = event.target.result;
        //turn to ascii string
        let asciiContents = btoa(contents);
        //add ascii string to form
        let form = {
            'file': asciiContents,
        }
        displayArea.append(form.file);
    };
    reader.onerror = function(event) {
        console.error('error, file could not be read');
    }
    //read file as a bit string
    reader.readAsBinaryString(img);
    // TODO send data via ajax to our DB our restful API
};

//add click event so that image is processed upon submit
$('#submitBtn').click(function(event) {
    event.preventDefault();
    imgToText();
});

$('#showBtn').click(function(event) {
    event.preventDefault();
    textToImg();
})
