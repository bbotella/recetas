// Search functionality for Tía Carmen's Recipe Website

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchForm = document.querySelector('form');
    
    // Add some interactivity to the search
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            // You could add live search suggestions here
            if (this.value.length > 2) {
                // Future: implement autocomplete
            }
        });
        
        // Focus on search input when page loads
        searchInput.focus();
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Add loading state to search form
    if (searchForm) {
        searchForm.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Buscando...';
                submitBtn.disabled = true;
            }
        });
    }
    
    // Add hover effects to recipe cards
    const recipeCards = document.querySelectorAll('.recipe-card');
    recipeCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Add click tracking for analytics (placeholder)
    document.addEventListener('click', function(e) {
        if (e.target.matches('.recipe-card a, .recipe-card')) {
            // Future: track recipe views
            console.log('Recipe clicked:', e.target.textContent);
        }
    });
});

// Utility functions
function highlightSearchTerm(text, term) {
    if (!term) return text;
    const regex = new RegExp(`(${term})`, 'gi');
    return text.replace(regex, '<span class="search-highlight">$1</span>');
}

function formatIngredients(ingredients) {
    // Future: better ingredient formatting
    return ingredients;
}

// Future: Add favorites functionality
function toggleFavorite(recipeId) {
    // Placeholder for favorites feature
    console.log('Toggle favorite for recipe:', recipeId);
}