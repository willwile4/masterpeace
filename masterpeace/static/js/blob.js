//js file to turn an image into a blob, then store the blob in our API.
// next: retrive the blob and put it on the page

function textToImg(text) {
  window.onload = function() {
  var fileInput = document.getElementById('imgFile');
  var fileDisplayArea = document.getElementById('fileDisplayArea');

  fileInput.addEventListener('change', function(e) {
    var file = fileInput.files[0];
    var textType = /text.*/;
    console.log(file);

  if (file.type.match(textType)) {
    var reader = new FileReader();

    reader.onload = function(e) {
      fileDisplayArea.innerText = reader.result;
      console.log(reader.result);
      var image = new Image();
      // change text to img on screen
      var source_string = `data:image/png;base64,${reader.result}`;
      image.src = source_string;
      document.body.appendChild(image);
    }
      reader.readAsText(file);
  } else {
      fileDisplayArea.innerText = "File not supported!";
  }
});
}
}

//turns an image into a blob
function imgToText() {
    // get file elem and get image
    let file = document.getElementById('imgFile');
    let img = document.getElementById('imgFile').files[0];
    let displayArea = document.getElementById('fileDisplayArea');
    console.log(file);
    console.log(img);
    //open a file reader and read in file, then turn it from binary to ascii
    var reader = new FileReader();
    reader.onload = function(event) {
        var contents = event.target.result;
        //turn to ascii string
        let asciiContents = btoa(contents);
        //add ascii string to form
        var form = new FormData();
        form.append('file', asciiContents);
        console.log(form);
        displayArea.append(form);
    };
    reader.onerror = function(event) {
        console.error('error, file could not be read');
    }
    //read file as a bit string
    reader.readAsBinaryString(img);
    //send via ajax to our DB via API

    // this conditional isn't ideal, but works for MVP
    // if(imgFile.type.slice(0,5) === 'image') {
    //     console.log('hi');
    //     var img = Image();
    //     img.src = imgFile;
    //     console.log(imgFile);
    //     // console.log(imgFile);
    //     // console.log(imgFile.type);
    //     // let aFile = btoa(imgFile);
    //     // console.log(aFile);
    //     // let bFile = atob(aFile);
    //     //$('#fileDisplayArea').append($('<img src=\'' + imgFile.name + '\'/>'));
    //     //build json form for send via ajax
    //     let $postData = {
    //         'pic': imgFile.value,
    //         'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
    //     }
    //     console.log($postData);
        //ajax request to send image to DB
        // $.ajax({
        //     type: 'PATCH',
        //     url: '/api/profile/8/',
        //     data: $postData,
        //     //contentType: 'application/json',
        //     success: function(result) {
        //         alert("success");
        //     }
    //     // });
    // } else {
    //     fileDisplayArea.innerText = "File not supported!";
    // }
    // fileElem.addEventListener('change', function(e) {
    //   console.log('here');
    //   let textType = /image.*/;
    //   console.log(textType);
    //     if (file.type.match(testType)) {
    //         console.log('match');
    //         var reader = new FileReader();
    //
    //         reader.onload = function(e) {
    //             imgBlob = btoa($file);
    //             console.log(imgBlob);
    //             return imgBlob;
    //         }
    // } else {
    //     fileDisplayArea.innerText = "File not supported!";
    // }
    // });
    console.log('end');
};

//add click event so that image is processed upon submit
$('#submitBtn').click(function(event) {
    event.preventDefault();
    imgToText();
});

// function toDataURL(url, callback) {
//   var xhr = new XMLHttpRequest();
//   xhr.onload = function() {
//     var reader = new FileReader();
//     reader.onloadend = function() {
//       callback(reader.result);
//     }
//     reader.readAsDataURL(xhr.response);
//   };
//   xhr.open('GET', url);
//   xhr.responseType = 'blob';
//   xhr.send();
// }
//
// // toDataURL('', function(dataUrl) {
//   console.log('RESULT:', dataUrl)
// })
