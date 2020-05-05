// page load animations

function finishPreload() {
    gsap.to('.preloader-main', {
        opacity: 0,
        display: 'none',
        duration: 0.4,
    });
    // gsap.from('.bg-left', {
    //   opacity: 0,
    //   duration: .7,
    //   x: -90
    // });
    // gsap.from('.bg-right', {
    //   opacity: 0,
    //   duration: .7,
    //   x: 90
    // });

    // var tl = gsap.timeline({
    //   defaults: {
    //     duration: .7
    //   }
    // });

    // tl.from('#logo-name', {
    //     opacity: 0,
    //     x: 20
    //   })
    //   .from('#logo-img', {
    //     opacity: 0
    //   })
    //   .from('.menu-btn', {
    //     opacity: 0,
    //     x: 20
    //   }, "-=1.2")
    //   .to('.gsap3', {
    //     opacity: 1
    //   }, "-=.9")
    //   .from('.gsap', {
    //     opacity: 0,
    //     y: -20,
    //     stagger: 0.3
    //   })
    //   .to('.gsap1', {
    //     opacity: 1,
    //     stagger: 0.3
    //   }, "-=1")
    //   .from('#robot', {
    //     opacity: 0,
    //     y: 20,
    //     stagger: 0.2
    //   }, "-=1.2");
    gsap.fromTo(
        '.robot',
        { y: -10, ease: Quad.easeInOut },
        { y: 10, duration: 1, repeat: -1, yoyo: true, ease: Quad.easeInOut }
    );
    gsap.fromTo(
        '.chat-tooltip',
        { y: -10, ease: Quad.easeInOut },
        { y: 10, duration: 1, repeat: -1, yoyo: true, ease: Quad.easeInOut }
    );
    gsap.fromTo(
        '.robot-shadow',
        { scale: 1, ease: Quad.easeInOut },
        { scale: 1.1, duration: 1, repeat: -1, yoyo: true, ease: Quad.easeInOut }
    );
}

function showChat() {
    gsap.fromTo('.chat', { scale: 0 }, { display: 'flex', scale: 1, duration: 0.5 });
    gsap.to('.chat-overlay', { display: 'block', opacity: 1, duration: 0.2 });
}

function hideChat() {
    gsap.fromTo('.chat', { scale: 1 }, { display: 'none', scale: 0, duration: 0.5 });
    gsap.to('.chat-overlay', { display: 'none', opacity: 0, duration: 0.2 });
}
