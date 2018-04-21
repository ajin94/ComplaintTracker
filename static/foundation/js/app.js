$(document).foundation();

$(document).ready(function(){
   $('.mark_resolved').click(function(){
       //setting up csrf token
        setup_ajax();
        //making ajax request
        $.ajax({
            type: 'post',
            url: 'ajax_mark_as_resolved/',
            data:{
            complaint_id: parseInt($(this).attr("data-complaintID"))
            },
            success: function(arg){
                if (arg == 'success'){
                    window.location.reload();
                }
            },
            error: function(){
                alert("Temporary Error ! Contact Admin");
            }
        });
   });

   $('.mark_as_read').click(function(e){
       setup_ajax();
       $.ajax({
           type: 'post',
           url: 'ajax_mark_as_read/',
           data: {
               messageID: parseInt($(this).attr('data-messageID'))
           },
           success: function(args){
               if (args == "success"){
                    window.location.reload();
               }
           },
           error: function(){
               alert("Temporary Error! Contact Admin");
           }
       });
   });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setup_ajax(){
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}