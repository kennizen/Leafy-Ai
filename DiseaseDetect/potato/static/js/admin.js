function show(value) {
    let ad = document.getElementById('admin-email-send');
    let sub = document.getElementById('U-subject');
    let bod = document.getElementById('U-body');

    gsap.fromTo(
        '#email-overlay',
        { opacity: 0, display: 'none', y: -20 },
        { opacity: 1, display: 'block', duration: 0.5, y: 0 }
    );
    gsap.to('.email-overlay-cover', { opacity: 1, display: 'block', duration: 0.2 });

    document.getElementsByName('R-mail')[0].placeholder = value;

    document.getElementById('submitMail').onsubmit = (e) => {
        e.preventDefault();
        ad.innerHTML = 'Sending...';
        ad.disabled = true;
        $.ajax({
            type: 'POST',
            url: '/sendMail/',
            data: {
                subject: $('input[name=Subject]').val(),
                body: $('textarea[name=Body]').val(),
                mail: value,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function () {
                gsap.to('.email-overlay-cover', { opacity: 0, display: 'none', duration: 0.2 });
                gsap.fromTo(
                    '#email-overlay',
                    { opacity: 1, display: 'block', y: 0 },
                    {
                        opacity: 0,
                        display: 'none',
                        duration: 0.5,
                        y: 20,
                        onComplete: () => {
                            sub.value = '';
                            bod.value = '';
                            ad.disabled = false;
                            ad.innerHTML = 'Send';
                            swal('Success', 'Mail Sent', 'success');
                        },
                    }
                );
            },
        });
    };
}

function hide() {
    gsap.fromTo(
        '#email-overlay',
        { opacity: 1, display: 'block', y: 0 },
        {
            opacity: 0,
            display: 'none',
            duration: 0.5,
            y: 20,
        }
    );
    gsap.to('.email-overlay-cover', { opacity: 0, display: 'none', duration: 0.2 });
}
