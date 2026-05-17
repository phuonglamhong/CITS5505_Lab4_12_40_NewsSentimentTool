function goLogin() {
    window.location.href = "/";
}


// Scroll animation
const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add(
                'opacity-100',
                'translate-y-0'
            );

        }

    });

});

document.querySelectorAll('.animate-on-scroll').forEach(el => {

    el.classList.add(
        'opacity-0',
        'translate-y-10',
        'transition-all',
        'duration-700'
    );

    observer.observe(el);

});