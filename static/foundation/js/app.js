$(document).foundation();

$(document).ready(function(){
   $('.mark_resolved').click(function(){
       //setting up csrf token
        var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
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

   $('.send_response').click(function(){
       alert("working");
       // $('#new_response_modal').foundation('open');
       // $('#id_from_department').change(function(){
       //     $('#id_from_department').val(1);
       // });
   });
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}