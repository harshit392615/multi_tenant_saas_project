window.addEventListener("beforeunload", function (e) {
    console.log("UNLOAD TRIGGERED");
});
document.addEventListener("DOMContentLoaded", function () {

    console.log("SUBSCRIPTION JS LOADED");

    const CONFIG = {
        API_BASE: "http://127.0.0.1:8000/api/organization",
        SUBSCRIPTION_ENDPOINT: "/subscription/"
    };

    let payuPayload = null;

    function authHeaders(extra = {}) {
        const token = localStorage.getItem("access");
        return token
            ? { Authorization: `Bearer ${token}`, ...extra }
            : extra;
    }

    const proceedBtn = document.getElementById("proceed-btn");
    const payNowBtn = document.getElementById("pay-now-btn");

    proceedBtn.addEventListener("click", async function () {

        console.log("Proceed clicked");

        const firstname = document.querySelector("input[name='firstname']").value.trim();
        const email = document.querySelector("input[name='email']").value.trim();
        const title = document.querySelector("select[name='title']").value;

        const orgSlug = localStorage.getItem("current_org");
        if (!orgSlug) {
            alert("Organization not selected");
            return;
        }

        try {
            const res = await fetch(
                `${CONFIG.API_BASE}${CONFIG.SUBSCRIPTION_ENDPOINT}`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        ...authHeaders({ "X-ORG-SLUG": orgSlug })
                    },
                    body: JSON.stringify({ firstname, email, title })
                }
            );

            if (!res.ok) throw new Error(`HTTP ${res.status}`);

            payuPayload = await res.json();

            document.getElementById("summary-plan").textContent = title;
            document.getElementById("summary-email").textContent = email;

            document.querySelector(".subscription-card").style.display = "none";
            document.getElementById("payment-confirmation").style.display = "block";

        } catch (err) {
            console.error("Subscription initiation failed:", err);
            alert("Failed to initiate payment");
        }
    });

    payNowBtn.addEventListener("click", function () {

        if (!payuPayload) {
            alert("Payment data missing");
            return;
        }

        const payuForm = document.createElement("form");
        payuForm.method = "POST";
        payuForm.action = payuPayload.payu_url;

        Object.keys(payuPayload).forEach(key => {
            if (key === "payu_url") return;

            const input = document.createElement("input");
            input.type = "hidden";
            input.name = key;
            input.value = payuPayload[key];
            payuForm.appendChild(input);
        });

        document.body.appendChild(payuForm);
        payuForm.submit();
    });

});
