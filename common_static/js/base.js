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

function header() {
        var header_nav_dropdown_tv_width = $('#header_nav_dropdown_tv').outerWidth();
            var header_nav_btn_width = $('#header_nav_btn').outerWidth();
            var header_nav_logo_width = $('#header_logo').outerWidth();
            var all_width = header_nav_dropdown_tv_width + header_nav_btn_width + header_nav_logo_width;
            if ($(window).width() - all_width > 30) {
                $('#header_nav_dropdown_tv').hide();
                $('#header_nav_btn').show();
            } else {
                $('#header_nav_dropdown_tv').show();
                $('#header_nav_btn').hide();
            }
    }

$(document).ready(header);
$(window).resize(header);