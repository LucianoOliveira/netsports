// Function to handle court selection
function addCourtEventListeners(selectedValue) {
    const courtElements = document.querySelectorAll('.Court');
    
    courtElements.forEach(court => {
        court.addEventListener('click', function() {
            const selectedCourts = document.querySelectorAll('.selectedCourt');
            const isAlreadySelected = court.classList.contains('selectedCourt');
            
            if ((selectedCourts.length < selectedValue || isAlreadySelected) && !isCourtDisabled(court)) {
                court.classList.toggle('selectedCourt');
            }
        });
    });
}

// Function to check if the court is disabled
function isCourtDisabled(court) {
    return court.style.pointerEvents === 'none' || court.style.opacity === '0.5';
}

// Show courts on page load with default value
document.addEventListener('DOMContentLoaded', function() {
    const defaultSelectedValue = parseInt(document.getElementById('court-number').value);
    addCourtEventListeners(defaultSelectedValue);
    updateCourtDisplay(defaultSelectedValue);

    // Change event for dropdown
    document.getElementById('court-number').addEventListener('change', function() {
        const selectedValue = parseInt(this.value);

        // Clear all selected courts
        const selectedCourts = document.querySelectorAll('.selectedCourt');
        selectedCourts.forEach(selectedCourt => {
            selectedCourt.classList.remove('selectedCourt');
        });

        updateCourtDisplay(selectedValue);
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

// Function to update court display based on selected value
function updateCourtDisplay(selectedValue) {
    const courtElements = document.querySelectorAll('.Court');
    courtElements.forEach((court, index) => {
        if (index < selectedValue) {
            court.classList.remove('selectedCourt');
        } else {
            court.classList.remove('selectedCourt');
            court.style.pointerEvents = selectedValue >= index + 1 ? 'none' : 'auto';
            court.style.opacity = selectedValue >= index + 1 ? '0.5' : '1';
        }
    });
}
