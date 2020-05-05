function openDelete() {
    gsap.to('.delete-confirm-overlay', {
        opacity: 1,
        duration: 0.4,
        display: 'block',
    });
    gsap.fromTo(
        '.delete-confirm',
        {
            scale: 0,
        },
        {
            opacity: 1,
            duration: 0.4,
            scale: 1,
            display: 'block',
        }
    );
}

function closeDelete() {
    gsap.to('.delete-confirm-overlay', {
        opacity: 0,
        duration: 0.4,
        display: 'none',
    });
    gsap.fromTo(
        '.delete-confirm',
        {
            opacity: 1,
            duration: 0.4,
            scale: 1,
            display: 'block',
        },
        {
            opacity: 0,
            duration: 0.4,
            scale: 0,
            display: 'none',
        }
    );
}

function anDelete() {
    gsap.to('.delete-answer-overlay', {
        opacity: 1,
        duration: 0.4,
        display: 'block',
    });
    gsap.fromTo(
        '.delete-answer',
        {
            scale: 0,
        },
        {
            opacity: 1,
            duration: 0.4,
            scale: 1,
            display: 'block',
        }
    );
}

function anDeleteclose() {
    gsap.to('.delete-answer-overlay', {
        opacity: 0,
        duration: 0.4,
        display: 'none',
    });
    gsap.fromTo(
        '.delete-answer',
        {
            opacity: 1,
            duration: 0.4,
            scale: 1,
            display: 'block',
        },
        {
            opacity: 0,
            duration: 0.4,
            scale: 0,
            display: 'none',
        }
    );
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

$('.answers').each(function (index, div) {
    $(div).css('border-left', '5px solid ' + getRandomColor());
});

$('.answer-body').each(function (index, div) {
    $(div).css('border-left', '5px solid ' + getRandomColor());
});
