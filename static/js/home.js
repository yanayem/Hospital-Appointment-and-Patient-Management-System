// =========================
// UNIVERSAL SLIDER FUNCTION
// =========================
function createSlider(sliderSelector, cardSelector, nextBtnSelector, prevBtnSelector, intervalTime = 4000) {
  const slider = document.querySelector(sliderSelector);
  const track = slider.querySelector(".slider-track") || slider.querySelector(".doctor-track") || slider.querySelector(".service-track");
  const cards = track.querySelectorAll(cardSelector);
  const nextBtn = slider.querySelector(nextBtnSelector);
  const prevBtn = slider.querySelector(prevBtnSelector);
  
  let index = 0;
  const gap = parseInt(window.getComputedStyle(cards[0]).marginRight);
  const cardWidth = cards[0].offsetWidth + gap;

  // Update slide position
  function updateSlide() {
    const visible = Math.floor(slider.offsetWidth / cardWidth);
    track.style.transform = `translateX(-${index * cardWidth}px)`;
    
    // Loop: go back to start if at the end
    if (index >= cards.length - visible) {
      setTimeout(() => { index = 0; track.style.transition = 'none'; track.style.transform = `translateX(0)`; }, 500);
    }
  }

  // Manual next
  nextBtn.addEventListener("click", () => {
    const visible = Math.floor(slider.offsetWidth / cardWidth);
    index++;
    if (index > cards.length - visible) index = 0;
    track.style.transition = 'transform 0.5s ease';
    updateSlide();
  });

  // Manual prev
  prevBtn.addEventListener("click", () => {
    const visible = Math.floor(slider.offsetWidth / cardWidth);
    index--;
    if (index < 0) index = cards.length - visible;
    track.style.transition = 'transform 0.5s ease';
    updateSlide();
  });

  // Auto slide
  let autoSlide = setInterval(() => {
    const visible = Math.floor(slider.offsetWidth / cardWidth);
    index++;
    if (index > cards.length - visible) index = 0;
    track.style.transition = 'transform 0.5s ease';
    updateSlide();
  }, intervalTime);

  // Pause on hover
  slider.addEventListener("mouseenter", () => clearInterval(autoSlide));
  slider.addEventListener("mouseleave", () => {
    autoSlide = setInterval(() => {
      const visible = Math.floor(slider.offsetWidth / cardWidth);
      index++;
      if (index > cards.length - visible) index = 0;
      track.style.transition = 'transform 0.5s ease';
      updateSlide();
    }, intervalTime);
  });

  window.addEventListener('resize', updateSlide);
}

// Initialize sliders
createSlider(".doctor-slider", ".doctor-card", ".next", ".prev", 4000);
createSlider(".service-slider", ".service-card", ".next", ".prev", 4000);

// =========================
// FADE-IN ANIMATION ON SCROLL
// =========================
const animatedElements = document.querySelectorAll(".animate");
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) entry.target.classList.add("visible");
  });
}, { threshold: 0.2 });

animatedElements.forEach(el => observer.observe(el));
