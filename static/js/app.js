function formatBytes(bytes) {
    if (!bytes) return "0 KB";
    const units = ["B", "KB", "MB"];
    let size = bytes;
    let unit = 0;
    while (size >= 1024 && unit < units.length - 1) {
        size /= 1024;
        unit += 1;
    }
    return `${size.toFixed(unit === 0 ? 0 : 1)} ${units[unit]}`;
}

function initUploadForm() {
    const form = document.querySelector("[data-upload-form]");
    if (!form) return;

    const input = form.querySelector("[data-file-input]");
    const dropzone = form.querySelector("[data-dropzone]");
    const previewPanel = form.querySelector("[data-preview-panel]");
    const previewImage = form.querySelector("[data-preview-image]");
    const fileName = form.querySelector("[data-file-name]");
    const fileSize = form.querySelector("[data-file-size]");
    const submitButton = form.querySelector("[data-submit-button]");

    function showPreview(file) {
        if (!file) return;
        previewImage.src = URL.createObjectURL(file);
        fileName.textContent = file.name;
        fileSize.textContent = formatBytes(file.size);
        previewPanel.hidden = false;
    }

    input.addEventListener("change", () => showPreview(input.files[0]));

    ["dragenter", "dragover"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.add("is-dragover");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropzone.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.remove("is-dragover");
        });
    });

    dropzone.addEventListener("drop", (event) => {
        const file = event.dataTransfer.files[0];
        if (!file) return;
        input.files = event.dataTransfer.files;
        showPreview(file);
    });

    form.addEventListener("submit", () => {
        submitButton.textContent = "Analizando...";
        submitButton.classList.add("is-loading");
    });
}

document.addEventListener("DOMContentLoaded", initUploadForm);
