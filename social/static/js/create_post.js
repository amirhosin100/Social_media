const imageUpload = document.getElementById("imageUpload");
const currentImage = document.getElementById("currentImage");
const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");

let images = [];

let currentIndex = 0;

imageUpload.addEventListener("change", (e) => {
    const files = Array.from(e.target.files);
    images = files.map(file => URL.createObjectURL(file));
    currentIndex = 0;
    showImage();
});

function showImage() {
    if (images.length > 0) {
        currentImage.src = images[currentIndex];
        currentImage.style.transform = "translateX(0)";
    } else {
        currentImage.src = "";
    }
}

prevBtn.addEventListener("click", () => {
    if (images.length > 0) {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        showImage();
    }
});

nextBtn.addEventListener("click", () => {
    if (images.length > 0) {
        currentIndex = (currentIndex + 1) % images.length;
        showImage();
    }
});

// --- مدیریت تگ‌ها ---
const tagInput = document.getElementById("tagInput");
const tagsList = document.getElementById("tagsList");
const tagsHidden = document.getElementById("tagsHidden");

var tags = [];

tagInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && this.value.trim() !== "") {
        e.preventDefault();
        const tagText = this.value.trim();
        tags.push(tagText);
        renderTags();
        this.value = "";
    }
});

function renderTags() {
    tagsList.innerHTML = "";
    tags.forEach((tag, index) => {
        const tagEl = document.createElement("div");
        tagEl.className = "tag";
        tagEl.innerHTML = `${tag} <span onclick="removeTag(${index})">&times;</span>`;
        tagsList.appendChild(tagEl);
    });
    tagsHidden.value = tags.join(",");
}

function removeTag(index) {
    tags.splice(index, 1);
    renderTags();
}
