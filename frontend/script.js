const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("fileInput");
const resultsDiv = document.getElementById("results");
const catalogueInfo = document.getElementById("catalogue-info");
const preview = document.getElementById("preview");

// Click to upload
dropZone.onclick = () => fileInput.click();

// File select
fileInput.onchange = () => {
  if (fileInput.files.length > 0) {
    handleFile(fileInput.files[0]);
  }
};

// Drag & drop
dropZone.ondragover = (e) => {
  e.preventDefault();
  dropZone.style.opacity = "0.7";
};

dropZone.ondragleave = () => {
  dropZone.style.opacity = "1";
};

dropZone.ondrop = (e) => {
  e.preventDefault();
  dropZone.style.opacity = "1";
  if (e.dataTransfer.files.length > 0) {
    handleFile(e.dataTransfer.files[0]);
  }
};

// Handle image
function handleFile(file) {
  // Show image preview
  preview.src = URL.createObjectURL(file);
  preview.style.display = "block";

  // Clear old results
  resultsDiv.innerHTML = "";
  catalogueInfo.innerText = "Analyzing image...";

  uploadImage(file);
}

// Upload to backend
function uploadImage(file) {
  const formData = new FormData();
  formData.append("image", file);

  fetch("/analyze", {
    method: "POST",
    body: formData
  })
    .then((res) => res.json())
    .then((data) => {
      // Catalogue + accuracy info
      catalogueInfo.innerText =
        `Catalogue Size: ${data.total_aesthetics} | ` +
        `Prediction Accuracy: ${data.accuracy}% | ` +
        `Results are generated only from the catalogue`;

      // Render results
      resultsDiv.innerHTML = "";
      data.results.forEach((r) => {
        const card = document.createElement("div");
        card.className = "result-card";

        card.innerHTML = `
          <strong>${r.aesthetic}</strong> — ${r.match}%
          <div class="progress">
            <div class="progress-bar" style="width:${r.match}%"></div>
          </div>
        `;

        resultsDiv.appendChild(card);
      });
    })
    .catch((err) => {
      console.error(err);
      catalogueInfo.innerText = "Error analyzing image. Please try again.";
    });
}
