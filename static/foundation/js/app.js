$(document).foundation();

$(document).ready(function(){
   $('#complaint_id_text').keyup(function(){
        append_complaint_id($(this).val());
    });
});

function append_complaint_id(complaint_id){
    $('#search_link').attr("href","?td_id="+complaint_id);
}