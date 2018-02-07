$(document).ready(function(){
    $("button").click(
        function(){
            var button_toggle = $(this).attr("data-toggle");
            if(button_toggle == "collapse"){
                var target_id = $(this).attr("data-target");
                $(target_id).slideToggle();
            }
        }
    );
});
