document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');

    // Toggle sidebar size when mouse hovers
    sidebar.addEventListener('mouseenter', () => {
        sidebar.classList.add('expanded');
        content.classList.add('expanded');
    });

    sidebar.addEventListener('mouseleave', () => {
        sidebar.classList.remove('expanded');
        content.classList.remove('expanded');
    });
});
