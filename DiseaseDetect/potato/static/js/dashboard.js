$(document).ready(function () {
    $("#usersearch").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#usertable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$(document).ready(function () {
    $("#anssearch").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#anstable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});



function openDelete(){
  gsap.to('.delete-confirm-overlay', {opacity: 1, duration: .4, display:'block'});
  gsap.fromTo('.delete-confirm',{scale: 0}, {opacity:1, duration: .4, scale: 1, display:'block'});
}

function closeDelete(){
  gsap.to('.delete-confirm-overlay', {opacity: 0, duration: .4, display:'none'});
  gsap.fromTo('.delete-confirm',{opacity:1, duration: .4, scale: 1, display:'block'}, {opacity:0, duration: .4, scale: 0, display:'none'});
}


function tag(){
    let s = document.querySelector(".tag-form")
    s.classList.toggle("show")
}