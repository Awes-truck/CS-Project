$(".navbar .nav-link").on("click", function(){
    $(".navbar").find(".active_id").removeClass("active_id");
    $(this).addClass("active_id");
});
