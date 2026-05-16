// SIDEBAR.JS — Responsive drawer sidebar

document.addEventListener('DOMContentLoaded', function () {
    var sidebar  = document.querySelector('.sidebar');
    var topbar   = document.querySelector('.topbar');
    if (!sidebar || !topbar) return;

    // Create overlay (dark background behind drawer)
    var overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    // Create topbar hamburger button
    var menuBtn = document.createElement('button');
    menuBtn.className = 'sidebar-menu-btn';
    menuBtn.title = 'Open menu';
    menuBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
    topbar.insertBefore(menuBtn, topbar.firstChild);

    // Create sidebar close button
    var closeBtn = document.createElement('button');
    closeBtn.className = 'sidebar-close-btn';
    closeBtn.innerHTML = '<i class="fa-solid fa-xmark"></i>';
    sidebar.insertBefore(closeBtn, sidebar.firstChild);

    function openDrawer() {
        sidebar.classList.add('drawer-open');
        overlay.classList.add('active');
    }

    function closeDrawer() {
        sidebar.classList.remove('drawer-open');
        overlay.classList.remove('active');
    }

    function checkWidth() {
        if (window.innerWidth <= 768) {
            sidebar.classList.add('drawer-mode');
            menuBtn.style.display = 'flex';
        } else {
            sidebar.classList.remove('drawer-mode');
            sidebar.classList.remove('drawer-open');
            overlay.classList.remove('active');
            menuBtn.style.display = 'none';
        }
    }

    menuBtn.addEventListener('click', openDrawer);
    closeBtn.addEventListener('click', closeDrawer);
    overlay.addEventListener('click', closeDrawer);
    window.addEventListener('resize', checkWidth);

    checkWidth();
});
