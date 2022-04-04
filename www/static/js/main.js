// Modal implementation used on the Subscription page
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

// International country code implementation
// Inspired by https://github.com/miguelgrinberg/flask-phone-input/blob/master/templates/index.html
 var phone_field = document.getElementById('phone');
 phone_field.style.position = 'absolute';
 phone_field.style.top = '-9999px';
 phone_field.style.left = '-9999px';
 phone_field.parentElement.insertAdjacentHTML('beforeend', '<div><input type="tel" class="form-control" id="_phone"></div>');
 var intl_phone_field = document.getElementById('_phone');
 var intl_phone_iti = window.intlTelInput(intl_phone_field, {
     initialCountry: 'gb' ,
     separateDialCode: true,
     utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/16.0.4/js/utils.js",
 });
 intl_phone_iti.setNumber(phone_field.value);
 intl_phone_field.addEventListener('blur', function() {
     phone_field.value = intl_phone_iti.getNumber();
 });
