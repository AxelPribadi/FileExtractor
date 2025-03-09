const fileInput = document.getElementById('file-input');
const fileName = document.getElementById('file-name');
const uploadBtn = document.getElementById('upload-btn');
const fileDropArea = document.getElementById('file-drop-area');
const statusMessage = document.getElementById('status-message');
        
// Handle file selection
fileInput.addEventListener('change', function() {
    if (this.files.length > 0) {
        // Create file name element if it doesn't exist
        if (!document.getElementById('file-name')) {
            const nameElement = document.createElement('div');
            nameElement.id = 'file-name';
            nameElement.className = 'file-name';
            fileDropArea.appendChild(nameElement);
        }
        
        // Display file name
        const fileNameElement = document.getElementById('file-name');
        fileNameElement.textContent = this.files[0].name;
        fileNameElement.style.display = 'block';
        
        // Update status
        statusMessage.textContent = '✓ File ready to upload!';
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
        fileInput.files = e.dataTransfer.files;
        
        // Create file name element if it doesn't exist
        if (!document.getElementById('file-name')) {
            const nameElement = document.createElement('div');
            nameElement.id = 'file-name';
            nameElement.className = 'file-name';
            fileDropArea.appendChild(nameElement);
        }
        
        // Display file name
        const fileNameElement = document.getElementById('file-name');
        fileNameElement.textContent = e.dataTransfer.files[0].name;
        fileNameElement.style.display = 'block';
        
        // Update status
        statusMessage.textContent = '✓ File ready to upload!';
    }
});
        


const allowedFormats = ['pdf', 'doc', 'docx', 'txt'];

// Handle upload button click
uploadBtn.addEventListener('click', function() {
    if (!fileInput.files || fileInput.files.length === 0) {
        statusMessage.textContent = 'Please select a file first.';
        return;
    }
    
    const file = fileInput.files[0];
    const uploadType = document.querySelector('input[name="upload-type"]:checked').value;
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    // Check if file format is allowed
    if (!allowedFormats.includes(fileExtension)) {
        statusMessage.textContent = '❌ Invalid file format. Allowed formats: PDF, DOC, DOCX, TXT.';
        return;
    }

    // In a real application, you'd send the file to a server here
    console.log(`Uploading file: ${file.name}`);
    console.log(`Upload type: ${uploadType}`);
    
    statusMessage.textContent = '⚡ Uploading...';
    
    // Simulate upload process
    setTimeout(() => {
        statusMessage.textContent = '✅ Upload complete!';
    }, 1500);
});
