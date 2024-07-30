document.addEventListener('DOMContentLoaded', (event) => {
    const fileDropArea = document.getElementById('file-drop-area');
    const fileInput = document.getElementById('file-input');
    const fileLabel = document.getElementById('file-label');

    fileDropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileDropArea.classList.add('dragover');
    });

    fileDropArea.addEventListener('dragleave', (e) => {
        fileDropArea.classList.remove('dragover');
    });

    fileDropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileDropArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileLabel.textContent = files[0].name;
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (fileInput.files.length > 0) {
            fileLabel.textContent = fileInput.files[0].name;
        }
    });
});

function toggleTopXInput(checkbox) {
    var topXGroup = document.getElementById('top_x_group');
    if (checkbox.checked) {
        topXGroup.style.display = 'block';
        document.getElementById('top_x').required = true;
    } else {
        topXGroup.style.display = 'none';
        document.getElementById('top_x').required = false;
    }
}

function validateForm() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var oneChecked = Array.prototype.slice.call(checkboxes).some(x => x.checked);
    var fileInput = document.getElementById('file-input');
    var formError = document.getElementById('form-error');

    formError.classList.add('d-none'); // Hide the error div initially

    if (!oneChecked && fileInput.files.length === 0) {
        formError.textContent = "Please select at least one operation and a file to upload.";
        formError.classList.remove('d-none');
        return false;
    }

    if (!oneChecked) {
        formError.textContent = "Please select at least one operation.";
        formError.classList.remove('d-none');
        return false;
    }

    if (fileInput.files.length === 0) {
        formError.textContent = "Please select a file to upload.";
        formError.classList.remove('d-none');
        return false;
    }

    return true;
}
