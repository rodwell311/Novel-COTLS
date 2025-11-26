document.addEventListener('DOMContentLoaded', () => {
    // Intersection Observer for fade-in animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const fadeElements = document.querySelectorAll('.fade-in');
    fadeElements.forEach(el => observer.observe(el));

    // Reading Progress Bar
    const progressBar = document.getElementById('progress-bar');
    if (progressBar) {
        window.addEventListener('scroll', () => {
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
            const clientHeight = document.documentElement.clientHeight || document.body.clientHeight;
            
            const scrolled = (scrollTop / (scrollHeight - clientHeight)) * 100;
            progressBar.style.width = scrolled + '%';
        });
    }

    // Font Size Adjuster
    const increaseFontBtn = document.getElementById('increase-font');
    const decreaseFontBtn = document.getElementById('decrease-font');
    const chapterContent = document.querySelector('.chapter-content');

    if (increaseFontBtn && decreaseFontBtn && chapterContent) {
        let currentFontSize = parseFloat(window.getComputedStyle(chapterContent).fontSize);

        increaseFontBtn.addEventListener('click', () => {
            currentFontSize += 2;
            chapterContent.style.fontSize = currentFontSize + 'px';
        });

        decreaseFontBtn.addEventListener('click', () => {
            currentFontSize = Math.max(12, currentFontSize - 2);
            chapterContent.style.fontSize = currentFontSize + 'px';
        });
    }
});
