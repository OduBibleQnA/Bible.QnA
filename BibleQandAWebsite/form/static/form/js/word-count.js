document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.getElementById("id_shortened_testimony");
    const wordCount = document.getElementById("word-count");

    if (!textarea || !wordCount) return;

    function updateWordCount() {
        const words = textarea.value.trim().split(/\s+/).filter(Boolean);
        const count = words.length;

        wordCount.classList.remove("text-danger", "text-muted");

        if (count < 50) {
            wordCount.style.display = "block";
            wordCount.textContent = `Need ${50 - count} more word${10 - count === 1 ? '' : 's'}`;
            wordCount.classList.add("text-danger");
        } else if (count > 175) {
            wordCount.style.display = "block";
            wordCount.textContent = `${count} / 175 (too many)`;
            wordCount.classList.add("text-danger");
        } else {
            wordCount.style.display = "block";
            wordCount.textContent = `${count} / 175`;
            wordCount.classList.add("text-muted");
        }
    }

    textarea.addEventListener("input", updateWordCount);
    updateWordCount(); // Trigger on load
});
