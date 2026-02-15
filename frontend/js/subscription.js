document.addEventListener("DOMContentLoaded", () => {

    const API_URL = "http://127.0.0.1:8000/api/organization/subscription/";

    const generateBtn = document.getElementById("generateBtn");
    const confirmBtn = document.getElementById("confirmPaymentBtn");
    const paySection = document.getElementById("paySection");
    const errorBox = document.getElementById("errorBox");

    let paymentPayload = null;

    generateBtn.addEventListener("click", async () => {

        errorBox.textContent = "";

        const token = localStorage.getItem("access");
        const orgSlug = localStorage.getItem("current_org");
        const title = document.getElementById("plan").value;

        if (!token || !orgSlug) {
            errorBox.textContent = "Authentication required.";
            return;
        }

        if (!title) {
            errorBox.textContent = "Please select a subscription plan.";
            return;
        }

        try {

            generateBtn.disabled = true;
            generateBtn.textContent = "Processing...";

            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`,
                    "X-ORG-SLUG": orgSlug
                },
                body: JSON.stringify({ title })
            });

            if (!response.ok) {
                throw new Error("Failed to initiate payment");
            }

            paymentPayload = await response.json();

            paySection.style.display = "block";

            generateBtn.disabled = false;
            generateBtn.textContent = "Continue to Payment";

        } catch (error) {
            errorBox.textContent = error.message;
            generateBtn.disabled = false;
            generateBtn.textContent = "Continue to Payment";
        }
    });

    confirmBtn.addEventListener("click", () => {

        if (!paymentPayload) {
            errorBox.textContent = "Payment session not initialized.";
            return;
        }

        redirectToPayment(paymentPayload);
    });

    function redirectToPayment(payload) {

        // FORM USED ONLY FOR PAYU REDIRECTION
        const form = document.createElement("form");
        form.method = "POST";
        form.action = payload.payu_url;

        Object.keys(payload).forEach(key => {
            if (key === "payu_url") return;

            const input = document.createElement("input");
            input.type = "hidden";
            input.name = key;
            input.value = payload[key];
            form.appendChild(input);
        });

        document.body.appendChild(form);
        form.submit();
    }

});
