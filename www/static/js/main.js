$(".navbar .nav-link").on("click", function(){
    $(".navbar").find(".active_id").removeClass("active_id");
    $(this).addClass("active_id");
});

var modal = document.getElementById("checkout_modal");
var btn = document.getElementById("junior_checkout");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
