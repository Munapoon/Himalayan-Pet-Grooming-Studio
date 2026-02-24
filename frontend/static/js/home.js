/**
 * Homepage functionality for Himalayan Pet Studio
 * Handles hero carousel, horizontal service scroll, and navbar scroll effects.
 */

document.addEventListener('DOMContentLoaded', function () {
    // --- Navbar Scroll Effect ---
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    }

    // --- Hero Carousel Functionality ---
    const slides = document.querySelectorAll('.carousel-slide');
    const indicators = document.querySelectorAll('.indicator');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (slides.length > 0) {
        let currentSlide = 0;
        let autoPlayInterval;

        function showSlide(n) {
            slides.forEach(slide => slide.classList.remove('active'));
            indicators.forEach(indicator => indicator.classList.remove('active'));

            if (n >= slides.length) {
                currentSlide = 0;
            } else if (n < 0) {
                currentSlide = slides.length - 1;
            } else {
                currentSlide = n;
            }

            slides[currentSlide].classList.add('active');
            if (indicators[currentSlide]) {
                indicators[currentSlide].classList.add('active');
            }
        }

        function nextSlide() {
            showSlide(currentSlide + 1);
        }

        function prevSlide() {
            showSlide(currentSlide - 1);
        }

        function startAutoPlay() {
            autoPlayInterval = setInterval(nextSlide, 5000);
        }

        function stopAutoPlay() {
            clearInterval(autoPlayInterval);
        }

        // Event Listeners
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                nextSlide();
                stopAutoPlay();
                startAutoPlay();
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                prevSlide();
                stopAutoPlay();
                startAutoPlay();
            });
        }

        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', () => {
                showSlide(index);
                stopAutoPlay();
                startAutoPlay();
            });
        });

        // Start autoplay
        startAutoPlay();

        // Pause on hover
        const carousel = document.querySelector('.hero-carousel');
        if (carousel) {
            carousel.addEventListener('mouseenter', stopAutoPlay);
            carousel.addEventListener('mouseleave', startAutoPlay);
        }
    }

    // --- Service Section Scroll Logic ---
    const scrollContainer = document.querySelector('.scroll-container');
    const progressBar = document.getElementById('scrollProgressBar');
    const servicePrev = document.getElementById('servicePrev');
    const serviceNext = document.getElementById('serviceNext');

    if (scrollContainer) {
        // Update progress bar on scroll
        scrollContainer.addEventListener('scroll', function () {
            const scrollLeft = scrollContainer.scrollLeft;
            const scrollWidth = scrollContainer.scrollWidth - scrollContainer.clientWidth;
            if (scrollWidth > 0 && progressBar) {
                const scrollPercentage = (scrollLeft / scrollWidth) * 100;
                progressBar.style.width = scrollPercentage + '%';
            }
        });

        // Initialize progress bar width
        const scrollWidth = scrollContainer.scrollWidth - scrollContainer.clientWidth;
        if (progressBar) {
            progressBar.style.width = scrollWidth > 0 ? '0%' : '100%';
        }

        // Scroll controls
        const scrollAmount = 400;
        if (servicePrev) {
            servicePrev.addEventListener('click', () => {
                scrollContainer.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            });
        }
        if (serviceNext) {
            serviceNext.addEventListener('click', () => {
                scrollContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            });
        }
    }

    // --- Service Card Click Handlers ---
    document.querySelectorAll('.service-card[data-url]').forEach(function (card) {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function () {
            window.location.href = this.getAttribute('data-url');
        });
    });

    // --- Booking Button Click Handlers ---
    document.querySelectorAll('[data-book-url]').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.stopPropagation();
            window.location.href = this.getAttribute('data-book-url');
        });
    });
});
