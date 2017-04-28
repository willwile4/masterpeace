//js file to update user profile via ajax/api

$('#btn').click(function(event) {
    event.preventDefault();
    let $info = $('#profile_form :input');
    let $form = [];
    for(var i = 0; i < $info.length; i++) {
        $form.push($info[i].name + "\": \"" + $info[i].value);
    };

    $.ajax({
        type: 'POST',
        url: "/api/profile/",
        data: $form,   // NEEDS TO BE A DICT/JSON OBJECT, currently an array
        success: function(result) {
            console.log('good job!');
        }
    });
});
