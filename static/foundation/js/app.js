$(document).foundation();

$(document).ready(function(){
   $('.mark_resolved').click(function(){
       var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
       $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

       $.ajax({
           type: 'post',
           url: 'ajax_mark_as_resolved/',
           data:{
                complaint_id: parseInt($(this).attr("data-complaintID"))
           },
           success: function(arg){
               window.location.reload();
           },
           error: function(){
                alert("Temporary Error ! Contact Admin");
           }
       });
   });
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}