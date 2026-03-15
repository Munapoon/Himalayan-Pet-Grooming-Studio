/**
 * Admin Panel base interactions.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss floating toast messages after 4 seconds
    const toasts = document.querySelectorAll('.admin-toast');
    toasts.forEach(function (toast, index) {
        setTimeout(function () {
            toast.classList.add('removing');
            setTimeout(function () {
                toast.remove();
                // Remove the container if empty
                const container = document.getElementById('admin-toast-container');
                if (container && container.children.length === 0) {
                    container.remove();
                }
            }, 300);
        }, 4000 + index * 300); // stagger multiple messages
    });
});
