document.addEventListener("DOMContentLoaded", function () {
  const methodSelect = document.getElementById("id_contact_method");
  const contactLabel = document.getElementById("contact-label");
  const contactPrefix = document.getElementById("contact-prefix");
  const contactDetailGroup = document.getElementById("contact-detail-group");
  const contactInput = document.querySelector('#id_encrypted_contact_detail');
  function updateContactUI() {
    const method = methodSelect.value;
    const requiresDetail = ["instagram", "phone", "email"].includes(method);

    contactDetailGroup.style.display = requiresDetail ? "block" : "none";

    if (method === "instagram") {
      contactLabel.innerHTML = 'Instagram Username<span class="text-danger">*</span>';
      contactPrefix.classList.remove("visually-hidden");
      contactPrefix.textContent = "@";
    } else if (method === "phone") {
      contactLabel.innerHTML = 'Phone Number<span class="text-danger">*</span>';
      contactPrefix.classList.add("visually-hidden");
    } else if (method === "email") {
      contactLabel.innerHTML = 'Email Address<span class="text-danger">*</span>';
      contactPrefix.classList.add("visually-hidden");
    } else {
      contactLabel.innerHTML = 'Contact Detail<span class="text-danger">*</span>';
      contactPrefix.classList.add("visually-hidden");
    }
  }

  methodSelect.addEventListener("change", updateContactUI);
  updateContactUI(); // Run on page load
});
