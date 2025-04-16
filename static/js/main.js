function reloadPreview(button) {
    const previewUrl = button.getAttribute('data-preview');
    if (!previewUrl) return;

    // Add spinning animation
    const icon = button.querySelector('i');
    icon.classList.add('fa-spin');

    // Find the closest project card and its image
    const card = button.closest('.featured-project-card');
    const img = card.querySelector('img');
    
    if (img) {
        // Create new image object to preload
        const newImg = new Image();
        
        newImg.onload = function() {
            // Update actual image only after new one is loaded
            img.src = newImg.src;
            // Remove spinning animation
            icon.classList.remove('fa-spin');
        };

        // Add timestamp and optimize preview parameters
        newImg.src = `${previewUrl}&t=${Date.now()}&width=600&quality=85&crop=true`;
        
        // Set timeout to remove spinner if image takes too long
        setTimeout(() => {
            icon.classList.remove('fa-spin');
        }, 500); // Reduced from 1000ms to 500ms
    }
}