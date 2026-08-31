document.addEventListener('DOMContentLoaded', function() {
    // Add to Cart Buttons Interaction
    const cartButtons = document.querySelectorAll('.btn-add-cart');
    
    cartButtons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Item successfully added to cart!');
        });
    });

    // Smooth Scrolling for Navigation Links
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});