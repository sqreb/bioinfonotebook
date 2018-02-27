$(document).ready(function(){
    $(".dropdown-toggle").mouseover(
        function(){
            var this_id = $(this).attr("id");
            $("ul[aria-labelledby="+this_id+"]").show();
            $("ul.dropdown-menu[aria-labelledby!="+this_id+"]").hide();
        }
    );
});
