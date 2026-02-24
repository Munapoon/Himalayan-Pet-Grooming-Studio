/**
 * Service Detail page interaction logic.
 * Primarily handles the interactive rating selection.
 */
document.addEventListener('DOMContentLoaded', function () {
    const ratingLabels = document.querySelectorAll('.rating-input label');

    // Attach click events to rating labels to ensure radio input synchronization
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
