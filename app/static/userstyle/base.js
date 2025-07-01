document.addEventListener('DOMContentLoaded', function () {
    const sidebarLinks = document.querySelectorAll('.sidebar-menu-link');
    const currentPathname = window.location.pathname;

    sidebarLinks.forEach(link => {
        link.classList.remove('active');
        const linkHref = link.getAttribute('href');
        if (linkHref) {
            const cleanedLinkHref = linkHref.endsWith('/') && linkHref.length > 1 ? linkHref.slice(0, -1) : linkHref;
            const cleanedCurrentPathname = currentPathname.endsWith('/') && currentPathname.length > 1 ? currentPathname.slice(0, -1) : currentPathname;
            if (cleanedLinkHref === cleanedCurrentPathname) {
                link.classList.add('active');
            }
            if (cleanedCurrentPathname === '/' && cleanedLinkHref === '/') {
                link.classList.add('active');
            }
        }
        const NotificationContainer = document.getElementById('NotificationContainer');
        const reciver = document.getElementById('reciver2');
        const notificationBox = NotificationContainer.querySelector('.notification-box');
        function showNotification(message, duration = 3000) {
            notificationBox.innerHTML = "";
            notificationBox.innerHTML = `<i class="fa-solid fa-info-circle text-primary me-2"></i> ${message}`;
            NotificationContainer.classList.add('show');
            setTimeout(() => {
                NotificationContainer.classList.remove('show');
            }, duration);
        }

        
        if (window.location.href.includes("/user-account/setting") && reciver.textContent.trim()) {
            showNotification(reciver.innerText);
        }
    });
});
