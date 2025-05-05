
document.addEventListener("DOMContentLoaded", function () {
    const textarea = document.querySelector(".auto-resize");

    function autoResize(el) {
      el.style.height = "auto";
      el.style.height = el.scrollHeight + "px";
    }

    textarea.addEventListener("input", () => autoResize(textarea));

    // Trigger initial resize if prefilled
    autoResize(textarea);
});

