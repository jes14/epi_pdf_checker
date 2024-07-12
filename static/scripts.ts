function updateFileName(): void {
    const fileInput = document.getElementById('file-input') as HTMLInputElement;
    const fileNameSpan = document.getElementById('file-name') as HTMLSpanElement;
    
    if (!fileInput || !fileNameSpan) {
        console.error('Element not found');
        return;
    }

    const file = fileInput.files?.[0];
    fileNameSpan.textContent = file ? file.name : 'No file chosen';
}