//js file for uploading imgs to amazon's bucket.
(function() {
    document.getElementById('file_input').onchange = function() {
        var files = document.getElementById('file_input').files;
        var file = files[0]
        if(!file) {
            return alert('No file selected');
        }
        getSignedRequest(file);
    }
})();

function getSignedRequest(file){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/sign_s3?file_name="+file.name+"&file_type="+file.type);
    xhr.onreadystatechange = function(){
        if(xhr.readyState === 4){
            if(xhr.status === 200){
                var response = JSON.parse(xhr.responseText);
                uploadFile(file, response.signed_request, response.url);
            }
            else{
                alert('Could not get signed URL.'); //justification: its an emergency notification.
            }
        }
    };
    xhr.send()
}

function uploadFile(file, s3Data, url){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data);
    xhr.setRequestHeader('x-amz-acl', 'public-read');
    var postData = new FormData();
    console.log(url, s3Data);
    postData.append('signed_request', s3Data)   //form data object
    postData.append('url', url)
    // for(key in s3Data.fields){
    //     postData.append(key, s3Data.fields[key]);
    //     console.log(key, s3Data.fields[key]);
    //     // postData[key]=s3Data.fields[key];
    // }
    console.log(file)
    postData.append('file', file, file.name);
    console.log(postData)
    xhr.onreadystatechange = function() {
        if(xhr.readyState === 4){
            if(xhr.status === 200 || xhr.status === 204){
                document.getElementById("preview").src = url;
                document.getElementById("avatar-url").value = url;
            }
            else {
                alert("Could not upload file"); //justification: its an emergency notification
            }
        }
    };
    xhr.send(postData);
}
