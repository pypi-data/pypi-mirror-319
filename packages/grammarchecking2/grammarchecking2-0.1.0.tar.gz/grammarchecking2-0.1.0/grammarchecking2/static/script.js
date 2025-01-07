document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector('form');
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('result-section');
    
    // Ensure loading section is hidden initially
    loadingSection.classList.add('hidden');
    
    form.addEventListener('submit', function(event) {
        // Show loading spinner and hide result section
        loadingSection.classList.remove('hidden');
        resultSection.classList.add('hidden');

        // Optionally, disable the submit button during the process
        const btn = document.querySelector('.btn');
        btn.disabled = true;

        // Simulate delay or call actual API
        setTimeout(() => {
            // Hide the loading spinner and show the result section after 3 seconds
            loadingSection.classList.add('hidden');
            resultSection.classList.remove('hidden');

            // Re-enable the submit button
            btn.disabled = false;
        }, 3000); // Replace 3000 with actual API call time or process duration
    });
});