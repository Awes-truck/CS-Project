$(".navbar .nav-link").on("click", function(){
    $(".navbar").find(".active_id").removeClass("active_id");
    $(this).addClass("active_id");
});

var modals = document.getElementsByClassName('modal');
var btns = document.getElementsByClassName("openmodal");
var spans = document.getElementsByClassName("close");

for(let i=0;i<btns.length;i++){
    btns[i].onclick = function() {
        modals[i].style.display = "block";
    }
}

for(let i=0;i<spans.length;i++){
    spans[i].onclick = function() {
        modals[i].style.display = "none";
    }
 }

 window.onclick = function(event) {
     for(let i=0;i<modals.length;i++){
         if (event.target == modals[i]) {
             modals[i].style.display = "none";
         }
     }
 }
