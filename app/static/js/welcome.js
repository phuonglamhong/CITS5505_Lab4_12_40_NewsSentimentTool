/*
Welcome page functionality.

This file handles:
- Navigation to login page
*/

// Redirect user to login page.
function goLogin() {
    window.location.href = "/";
}

/*
Intersection Observer for scroll animations.

Adds animation classes when elements
enter the viewport.
*/

// Scroll animation
const observer = new IntersectionObserver(entries => {

    entries.forEach(entry => {
        // Animate element when visible
        if (entry.isIntersecting) {

            entry.target.classList.add(
                'opacity-100',
                'translate-y-0'
            );

        }

    });

});
/*
Apply initial hidden animation styles
to all animated sections.
*/
document.querySelectorAll('.animate-on-scroll').forEach(el => {

    el.classList.add(
        'opacity-0',
        'translate-y-10',
        'transition-all',
        'duration-700'
    );

    observer.observe(el);

});