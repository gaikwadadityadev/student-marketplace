/**
 * Student Marketplace - Main JavaScript
 * Handles frontend interactions and AJAX requests
 */

// Search functionality with debounce
let searchTimeout;
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 500ms of no typing
                if (this.value.length >= 3 || this.value.length === 0) {
                    const form = this.closest('form');
                    if (form) {
                        form.submit();
                    }
                }
            }, 500);
        });
    }
});

// Image gallery functionality
function changeMainImage(imageSrc, element) {
    const mainImage = document.getElementById('mainImage');
    if (mainImage) {
        mainImage.src = imageSrc;
        // Update active thumbnail
        document.querySelectorAll('.product-thumbnail').forEach(thumb => {
            thumb.classList.remove('active');
        });
        if (element) {
            element.classList.add('active');
        }
    }
}

// Rating input interaction
document.addEventListener('DOMContentLoaded', function() {
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    if (ratingInputs.length > 0) {
        ratingInputs.forEach(radio => {
            radio.addEventListener('change', function() {
                const rating = parseInt(this.value);
                const labels = document.querySelectorAll('.rating-input label');
                labels.forEach((label, index) => {
                    const starIndex = 5 - index;
                    const icon = label.querySelector('i');
                    if (icon) {
                        if (starIndex <= rating) {
                            icon.classList.remove('bi-star');
                            icon.classList.add('bi-star-fill');
                        } else {
                            icon.classList.remove('bi-star-fill');
                            icon.classList.add('bi-star');
                        }
                    }
                });
            });
        });
    }
});

// Add to cart (placeholder)
function addToCart(productId) {
    // TODO: Implement cart functionality
    alert('Add to cart functionality will be implemented soon!');
}

// Add to wishlist (placeholder)
function addToWishlist(productId) {
    // TODO: Implement wishlist functionality
    alert('Wishlist functionality will be implemented soon!');
}

// Mark review as helpful
function markHelpful(reviewId) {
    // TODO: Implement AJAX call to mark review as helpful
    fetch(`/api/reviews/helpful`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ review_id: reviewId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Thank you for your feedback!');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Filter form auto-submit on change
document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const selects = filterForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }
});

// Smooth scroll to reviews section
function scrollToReviews() {
    document.getElementById('reviews').scrollIntoView({ behavior: 'smooth' });
}

// Product image zoom on hover (optional enhancement)
document.addEventListener('DOMContentLoaded', function() {
    const productImages = document.querySelectorAll('.product-image-container img');
    productImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});
