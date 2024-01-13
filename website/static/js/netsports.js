document.addEventListener('DOMContentLoaded', function () {
    // Initialize Flatpickr
    flatpickr("#date_NonStop", {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        minuteIncrement: 15,
        onChange: function (selectedDates, dateStr, instance) {
            const formContainer = document.getElementById('form-container');
            if (selectedDates.length > 0) {
                formContainer.style.display = 'block';
            } else {
                formContainer.style.display = 'none';
            }
        }
    });

    // Event listener for court number dropdown
    document.getElementById('court-number').addEventListener('change', function () {
        const selectedValue = parseInt(this.value);

        // Update court display
        updateCourtDisplay(selectedValue);
    });

    // Event listener for court cards
    const courtElements = document.querySelectorAll('.Court');
    courtElements.forEach(court => {
        court.addEventListener('click', function () {
            const isAlreadySelected = court.classList.contains('selectedCourt');
            const selectedCourts = document.querySelectorAll('.selectedCourt');
            const selectedValue = parseInt(document.getElementById('court-number').value);

            if ((selectedCourts.length < selectedValue || isAlreadySelected) && !court.classList.contains('disabledCourt')) {
                court.classList.toggle('selectedCourt', !isAlreadySelected);

                // Update selected count label and total number of players
                updateSelectedCountLabel();
                updateTotalPlayers(selectedValue);
            } else {
                alert(`You can only select ${selectedValue} court(s).`);
            }
        });
    });
});

// Function to update court display based on selected value
function updateCourtDisplay(selectedValue) {
    const courtElements = document.querySelectorAll('.Court');
    courtElements.forEach((court, index) => {
        court.classList.remove('selectedCourt', 'disabledCourt');
    });

    // Update selected count label and total number of players
    updateSelectedCountLabel();
    updateTotalPlayers(selectedValue);
}

// Function to update the selected count label
function updateSelectedCountLabel() {
    const selectedCourts = document.querySelectorAll('.selectedCourt');
    const selectedCountLabel = document.getElementById('selectedCountLabel');
    const selectedValue = parseInt(document.getElementById('court-number').value);

    if (selectedCourts.length > selectedValue) {
        selectedCourts.forEach(selectedCourt => {
            selectedCourt.classList.remove('selectedCourt');
        });

        alert(`You can only select ${selectedValue} court(s).`);
    }

    selectedCountLabel.textContent = `${selectedCourts.length} court${selectedCourts.length !== 1 ? 's' : ''} selected`;
}

// Function to update total number of players
function updateTotalPlayers(selectedValue) {
    const numPlayerTotal = document.getElementById('num_player_total');
    numPlayerTotal.value = selectedValue * 4;
}
