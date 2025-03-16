// Script for index.html
const fileInput = document.getElementById('file-input');
const filesContainer = document.getElementById('files-container');
const uploadBtn = document.getElementById('upload-btn');
const fileDropArea = document.getElementById('file-drop-area');
const statusMessage = document.getElementById('status-message');
const appIdSelect = document.getElementById('app_id');
const uploadForm = document.getElementById('upload-form');
const filenamesInput = document.querySelector('input[name="filenames"]');

// Keep a global array to store selected files
let selectedFiles = [];

const allowedFormatsByApp = {
    'documentContext': ['pdf', 'doc', 'docx', 'txt'],
    'imageGenerator': ['jpg', 'jpeg', 'png', 'svg']
};

function getTodayDate() {
    const today = new Date();
    const year = today.getUTCFullYear();
    const month = String(today.getUTCMonth() + 1).padStart(2, '0');
    const day = String(today.getUTCDate()).padStart(2, '0');
    const hour = String(today.getUTCHours()).padStart(2, '0');
    const minute = String(today.getUTCMinutes()).padStart(2, '0');
    const second = String(today.getUTCSeconds()).padStart(2, '0');
    return `${year}${month}${day}${hour}${minute}${second}`;
}

function standardizeFileName(filename) {
    return filename.replace(/_/g, '-').replace(/\s+/g, '-').replace(/\./g, '-');
}

function generateFormattedFileName(file) {
    const mode = document.querySelector('input[name="upload-type"]:checked').value;
    const appId = document.getElementById('app_id').value || 'appId';
    const date = getTodayDate();
    
    if (!file) return `${appId}_${mode}_file_${date}`;
    
    const originalFilename = file.name;
    const lastDotIndex = originalFilename.lastIndexOf('.');
    const extension = lastDotIndex !== -1 ? originalFilename.slice(lastDotIndex + 1) : '';
    const nameWithoutExtension = lastDotIndex !== -1 ? originalFilename.slice(0, lastDotIndex) : originalFilename;
    const cleanFileName = standardizeFileName(nameWithoutExtension);
    
    return `${appId}_${mode}_${cleanFileName}_${date}.${extension}`;
}

// Validate file format based on selected application
function validateAllFiles(files) {
    const selectedApp = appIdSelect.value;
    
    if (!selectedApp) {
        return {
            valid: false,
            message: 'Please select an application.'
        };
    }
    
    if (!files || files.length === 0) {
        return {
            valid: false,
            message: 'Please select at least one file.'
        };
    }
    
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        
        if (!allowedFormatsByApp[selectedApp].includes(fileExtension)) {
            return {
                valid: false,
                message: `❌ Invalid file format: ${file.name}. Allowed formats: ${allowedFormatsByApp[selectedApp].join(', ')}`
            };
        }
    }
    
    return {
        valid: true,
        message: `✓ ${files.length} files ready to upload!`
    };
}

// Update the hidden filenames input with formatted filenames
function updateFilenamesInput() {
    const formattedFilenames = selectedFiles.map(file => generateFormattedFileName(file));
    
    // Remove any existing filename inputs
    const existingFilenameInputs = uploadForm.querySelectorAll('input[name="filenames"]');
    existingFilenameInputs.forEach(input => input.remove());
    
    // Create individual input elements for each filename
    formattedFilenames.forEach(filename => {
        const filenameInput = document.createElement('input');
        filenameInput.type = 'hidden';
        filenameInput.name = 'filenames';
        filenameInput.value = filename;
        uploadForm.appendChild(filenameInput);
    });
}

// Display all selected files
function displayFiles() {
    filesContainer.innerHTML = '';
    
    if (selectedFiles && selectedFiles.length > 0) {
        for (let i = 0; i < selectedFiles.length; i++) {
            const fileElement = document.createElement('div');
            fileElement.className = 'file-name';
            fileElement.style.display = 'block';
            fileElement.style.marginBottom = '5px';
            fileElement.style.padding = '8px';
            fileElement.style.backgroundColor = '#f0f0f0';
            fileElement.style.borderRadius = '4px';
            fileElement.style.display = 'flex';
            fileElement.style.justifyContent = 'space-between';
            
            const fileNameSpan = document.createElement('span');
            fileNameSpan.textContent = selectedFiles[i].name;
            fileElement.appendChild(fileNameSpan);
            
            const removeBtn = document.createElement('span');
            removeBtn.textContent = '✕';
            removeBtn.style.cursor = 'pointer';
            removeBtn.style.color = 'red';
            removeBtn.style.fontWeight = 'bold';
            removeBtn.dataset.index = i;
            
            removeBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                removeFile(parseInt(this.dataset.index));
                return false;
            });
            
            fileElement.appendChild(removeBtn);
            filesContainer.appendChild(fileElement);
        }
    }
    
    // Update the hidden filenames input
    updateFilenamesInput();
}

// Remove a file from the selection
function removeFile(index) {
    // Remove the file from our array
    selectedFiles.splice(index, 1);
    
    // Update display and validation
    displayFiles();
    updateFormStatus();
}

// Update form status and button state
function updateFormStatus() {
    // Create a FileList-like object for validation
    const validationResult = validateAllFiles(selectedFiles);
    statusMessage.textContent = validationResult.message;
    uploadBtn.disabled = !validationResult.valid || selectedFiles.length === 0;
}

// Validate form before submission
function validateForm() {
    return validateAllFiles(selectedFiles).valid;
}

// Handle form submission
uploadForm.addEventListener('submit', function(e) {
    if (!validateForm()) {
        e.preventDefault();
        return false;
    }
    
    // Update the filenames input one last time before submission
    updateFilenamesInput();
    
    // Clear any existing files from the form
    const existingFileInputs = uploadForm.querySelectorAll('input[name="files"]');
    existingFileInputs.forEach(input => input.remove());
    
    // Create form-compatible file inputs
    selectedFiles.forEach(file => {
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.name = 'files';
        fileInput.style.display = 'none';
        fileInput.files = dataTransfer.files;
        
        uploadForm.appendChild(fileInput);
    });
    
    // Show uploading message
    statusMessage.textContent = '⚡ Uploading...';
    
    // Allow the form to submit normally
    return true;
});

// Handle file selection
fileInput.addEventListener('change', function() {
    if (this.files && this.files.length > 0) {
        // Add new files to our array, checking for duplicates
        Array.from(this.files).forEach(file => {
            const isDuplicate = selectedFiles.some(existingFile => 
                existingFile.name === file.name && existingFile.size === file.size);
                
            if (!isDuplicate) {
                selectedFiles.push(file);
            }
        });
        
        // Reset the file input to allow selecting the same file again
        this.value = '';
        
        // Update display and validation
        displayFiles();
        updateFormStatus();
    }
});

// Handle drag and drop
fileDropArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    this.style.borderColor = '#5352ed';
    this.style.backgroundColor = 'rgba(83, 82, 237, 0.1)';
});

fileDropArea.addEventListener('dragleave', function() {
    this.style.borderColor = '#ff4757';
    this.style.backgroundColor = 'rgba(255, 71, 87, 0.05)';
});

fileDropArea.addEventListener('drop', function(e) {
    e.preventDefault();
    this.style.borderColor = '#ff4757';
    this.style.backgroundColor = 'rgba(255, 71, 87, 0.05)';
    
    if (e.dataTransfer.files.length > 0) {
        // Add new files to our array, checking for duplicates
        Array.from(e.dataTransfer.files).forEach(file => {
            const isDuplicate = selectedFiles.some(existingFile => 
                existingFile.name === file.name && existingFile.size === file.size);
                
            if (!isDuplicate) {
                selectedFiles.push(file);
            }
        });
        
        // Update display and validation
        displayFiles();
        updateFormStatus();
    }
});

// Add validation on app_id change
appIdSelect.addEventListener('change', function() {
    updateFormStatus();
});
