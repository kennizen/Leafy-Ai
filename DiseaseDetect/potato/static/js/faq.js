function finishPreload() {
    gsap.to('.preloader-main', {
        opacity: 0,
        display: 'none',
        duration: 0.4,
    });
}

function getRandomColor() {
    var rcolor = [
        '#FF1744',
        '#C51162',
        '#D50000',
        '#D500F9',
        '#6200EA',
        '#304FFE',
        '#2979FF',
        '#00B0FF',
        '#18FFFF',
        '#1DE9B6',
        '#00E676',
        '#AEEA00',
        '#FFFF00',
        '#FF6D00',
        '#FF3D00',
    ];
    var random = rcolor[Math.floor(Math.random() * rcolor.length)];
    return random;
}

$('.questions').each(function (index, div) {
    $(div).css('border-left', '5px solid ' + getRandomColor());
});

$('.answers').each(function (index, div) {
    $(div).css('border-left', '5px solid ' + getRandomColor());
});

$('.answer-body').each(function (index, div) {
    $(div).css('border-left', '5px solid ' + getRandomColor());
});

//Get the button:
mybutton = document.getElementById('myBtn');

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (
        document.body.scrollTop > 100 ||
        document.documentElement.scrollTop > 100
    ) {
        mybutton.style.display = 'block';
    } else {
        mybutton.style.display = 'none';
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}
