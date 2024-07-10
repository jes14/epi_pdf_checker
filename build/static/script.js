function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;

    handleFiles(files);
}

function handleFiles(files) {
    if (files.length) {
        let file = files[0];
        if (file.type === "application/pdf") {
            uploadFile(file);
        } else {
            alert("Please upload a PDF file.");
        }
    }
}

function uploadFile(file) {
    let url = '/upload';
    let formData = new FormData();
    formData.append('pdf', file);

    fetch(url, {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          document.getElementById('text-content').textContent = data.text;
      }).catch(() => {
          alert("There was an error uploading the file.");
      });
}

let dropArea = document.getElementById('drop-area');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
});

dropArea.addEventListener('drop', handleDrop, false);
