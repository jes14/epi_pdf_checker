function updateFileName() {
    const fileInput = document.getElementById('file-input');
    const fileNameSpan = document.getElementById('file-name');

    if (!fileInput || !fileNameSpan) {
        console.error('Element not found');
        return;
    }

    const file = fileInput.files ? fileInput.files[0] : null;
    fileNameSpan.textContent = file ? file.name : 'No file chosen';
}
