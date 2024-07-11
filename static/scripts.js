
function updateFileName() {
    const fileInput = document.getElementById('file-input');
    const fileNameSpan = document.getElementById('file-name');
    const file = fileInput.files[0];
    fileNameSpan.textContent = file ? file.name : 'No file chosen';
}