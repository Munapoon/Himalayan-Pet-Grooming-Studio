/**
 * Admin Panel base interactions.
 */
document.addEventListener('DOMContentLoaded', function () {
    // Auto-dismiss alerts after 5 seconds to keep the interface clean
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                // Fallback if bootstrap object is not available
                alert.style.display = 'none';
            }
        }, 5000);
    });
});
