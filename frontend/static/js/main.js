// Main JavaScript for Himalayan Pet Studio

document.addEventListener('DOMContentLoaded', function () {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Clear all password fields on page load to prevent autofill
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.value = '';
        // Disable browser autofill
        input.setAttribute('autocomplete', 'off');
        input.setAttribute('data-form-type', 'other');
    });

    // Additional delay to ensure autofill is cleared
    setTimeout(() => {
        passwordInputs.forEach(input => {
            input.value = '';
        });
    }, 100);
});

// Toggle password visibility
function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    const icon = button.querySelector('i');

    if (!input) {
        console.error('Password input not found:', inputId);
        return;
    }

    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Navbar Scroll Effect
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    }
});