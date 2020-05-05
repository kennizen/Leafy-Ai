function finishPreload() {
    gsap.to('.preloader-main', {
        opacity: 0,
        display: 'none',
        duration: 0.4,
    });
}

// process div

function process() {
    gsap.to('.pro-overlay', {
        opacity: 1,
        display: 'block',
        duration: 0.2,
    });
    gsap.to('.processing', {
        opacity: 1,
        display: 'block',
        duration: 0.2,
    });
}

//predict div display and image upload alert

div = document.getElementById('predict');
image = document.getElementById('file-2');
para = document.getElementById('res');
if (res.innerHTML == '') {
    div.style.display = 'none';
}

function check() {
    if (image.files.length == 0) {
        swal('No Image', 'Please select an image', 'error');
        return false;
    }
    return true;
}

//scroll to result div

$(document).ready(function () {
    // Handler for .ready() called.
    $('html, body').animate(
        {
            scrollTop: $('#predict').offset().top,
        },
        'slow'
    );
});

function showAllHistory() {
    gsap.to('.his-con', {
        overflow: 'auto',
        height: '810px',
        duration: 0.5,
    });
    gsap.to('.show-all-history', {
        display: 'none',
        duration: 0.01,
    });
    gsap.to('.show-less-history', {
        display: 'block',
    });
}

function showLessHistory() {
    document.querySelector('.his-con').scrollTop = 0;
    gsap.to('.his-con', {
        overflow: 'hidden',
        height: '250px',
        duration: 0.5,
    });
    gsap.to('.show-less-history', {
        display: 'none',
        duration: 0.01,
    });
    gsap.to('.show-all-history', {
        display: 'block',
    });
}
