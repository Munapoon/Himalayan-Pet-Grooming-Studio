/**
 * Appointment List page interaction logic.
 * Handles making appointment cards clickable for easy access to details.
 */
document.addEventListener('DOMContentLoaded', function () {
    const appointmentCards = document.querySelectorAll('.appointment-card[data-url]');

    appointmentCards.forEach(function (card) {
        card.addEventListener('click', function () {
            const detailUrl = this.getAttribute('data-url');
            if (detailUrl) {
                window.location.href = detailUrl;
            }
        });
    });
});
