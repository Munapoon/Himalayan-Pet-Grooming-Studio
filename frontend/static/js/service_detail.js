
document.addEventListener('DOMContentLoaded', function () {
    const ratingLabels = document.querySelectorAll('.rating-input label');

    
    ratingLabels.forEach(label => {
        label.addEventListener('click', function () {
            const inputId = this.getAttribute('for');
            const input = document.getElementById(inputId);
            if (input) {
                input.checked = true;
            }
        });
    });
});
