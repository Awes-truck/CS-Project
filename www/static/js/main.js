let top_button = document.getElementById("back-to-top");
const sections = document.querySelectorAll("section");
const navItem = document.querySelectorAll(".navbar-nav a.nav-item.nav-link");
const contactItem = document.querySelectorAll(".socials li");
const socialsList = document.getElementsByClassName("socials");

// Scroll event handler
$(window).on('scroll', function () {
    //--------NAVBAR TOGGLER---------//

    if ( $(window).scrollTop() > 10 ) {
        $('.navbar').addClass('active');
        top_button.style.display = "block";
    } else {
        $('.navbar').removeClass('active');
        top_button.style.display = "none";
    }

    //------ACTIVE TAB--------//
    let current = "";
    sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - sectionHeight / 3) {
            current = section.getAttribute("id");
        }
    });
    navItem.forEach((item) => {
        $(item).removeClass("active_id");
        if (item.classList.contains(current)) {
            $(item).addClass("active_id");
        }
    });

    //---------ADD ANIMATION CLASS ONCE 'CONTACT' TAG IS HIT-----------//
    if (current === "contact"){
        socialsList[0].style.flexDirection = "row";
        contactItem.forEach((i) => {
            $(i).addClass('move');
        })
    } else {
        contactItem.forEach((i) => {
            socialsList[0].style.flexDirection = "column";
            $(i).removeClass('move');
        })
    }
});

// $(document).keydown(function(event) {
// if (event.ctrlKey==true && (event.which == '61' || event.which == '107' || event.which == '173' || event.which == '109'  || event.which == '187'  || event.which == '189'  ) ) {
//         event.preventDefault();
//      }
//     // 107 Num Key  +
//     // 109 Num Key  -
//     // 173 Min Key  hyphen/underscore key
//     // 61 Plus key  +/= key
// });
// document.addEventListener('wheel', function (event) {
//        if (event.ctrlKey == true) {
//            event.preventDefault();
//        }
// });
//
// document.addEventListener('touchmove', function (event) {
//   if (event.scale !== 1) { event.preventDefault(); }
// }, false);


$('#back-to-top').on("click", function(){
    $('html,body').scrollTop(0);
});

$(".navbar .nav-link").on("click", function(){
    $(".navbar").find(".active_id").removeClass("active_id");
    $(this).addClass("active_id");
});

$(document).ready(function() {
    setTimeout(function(){
        $('body').addClass('loaded');
    }, 800);
});

const inViewport = (entries, observer) => {
    entries.forEach(entry => {
        entry.target.classList.toggle("is-inViewport", entry.isIntersecting);
    });
};

const Obs = new IntersectionObserver(inViewport);
const obsOptions = {}; //See: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API#Intersection_observer_options

// Attach observer to every [data-inviewport] element:
const ELs_inViewport = document.querySelectorAll('[data-inviewport]');
ELs_inViewport.forEach(EL => {
    Obs.observe(EL, obsOptions);
});
