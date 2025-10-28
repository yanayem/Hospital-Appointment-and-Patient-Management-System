// Animate elements on scroll
const animatedElements = document.querySelectorAll("[data-animate]");

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      entry.target.classList.add("animate");
      observer.unobserve(entry.target); // Optional: animate once
    }
  });
}, {
  threshold: 0.2
});

animatedElements.forEach(el => {
  observer.observe(el);
});
