// Function to handle court selection
function addCourtEventListeners(selectedValue) {
    const courtElements = document.querySelectorAll('.Court');
    courtElements.forEach(court => {
        court.addEventListener('click', function() {
            const selectedCourts = document.querySelectorAll('.selectedCourt');
            if (selectedCourts.length < selectedValue || court.classList.contains('selectedCourt')) {
                court.classList.toggle('selectedCourt');
            }
        });
    });
}

// Show courts on page load with default value
document.addEventListener('DOMContentLoaded', function() {
    const defaultSelectedValue = parseInt(document.getElementById('court-number').value);
    addCourtEventListeners(defaultSelectedValue);

    // Change event for dropdown
    document.getElementById('court-number').addEventListener('change', function() {
        const selectedValue = parseInt(this.value);
        const courtElements = document.querySelectorAll('.Court');
        const availableCourts = document.querySelectorAll('.Court:not([style*="opacity: 0.5"])');
        
        courtElements.forEach((court, index) => {
            if (index < availableCourts.length) {
                court.classList.remove('selectedCourt');
            } else {
                court.classList.remove('selectedCourt');
                court.style.pointerEvents = selectedValue > availableCourts.length ? 'none' : 'auto';
                court.style.opacity = selectedValue > availableCourts.length ? '0.5' : '1';
            }
        });

        addCourtEventListeners(selectedValue);
    });

    // Form submission validation
    document.getElementById('courtForm').addEventListener('submit', function(event) {
        const selectedCourts = document.querySelectorAll('.selectedCourt');
        const selectedValue = parseInt(document.getElementById('court-number').value);
        if (selectedCourts.length !== selectedValue) {
            event.preventDefault(); // Prevent form submission if counts don't match
            alert(`Please select exactly ${selectedValue} court(s).`);
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#date_NonStop", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        minuteIncrement: 15,
        onChange: function(selectedDates, dateStr, instance) {
            const formContainer = document.getElementById('form-container');
            if (selectedDates.length > 0) {
                formContainer.style.display = 'block';
            } else {
                formContainer.style.display = 'none';
            }
        }
    });
});