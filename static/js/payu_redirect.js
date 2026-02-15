document.addEventListener("DOMContentLoaded", function () {

    const dataContainer = document.getElementById("payu-data");

    if (!dataContainer) {
        console.error("PayU data container not found");
        return;
    }

    const payuUrl = dataContainer.dataset.payu_url;

    if (!payuUrl) {
        console.error("PayU URL missing");
        return;
    }

    // Create form dynamically
    const form = document.createElement("form");
    form.method = "POST";
    form.action = payuUrl;

    // All required PayU fields
    const fields = {
        key: dataContainer.dataset.key,
        txnid: dataContainer.dataset.txnid,
        amount: dataContainer.dataset.amount,
        productinfo: dataContainer.dataset.productinfo,
        firstname: dataContainer.dataset.firstname,
        email: dataContainer.dataset.email,
        phone: dataContainer.dataset.phone,
        surl: dataContainer.dataset.surl,
        furl: dataContainer.dataset.furl,
        hash: dataContainer.dataset.hash
    };

    Object.entries(fields).forEach(([name, value]) => {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        form.appendChild(input);
    });

    document.body.appendChild(form);

    // Small delay ensures DOM stability
    setTimeout(() => {
        form.submit();
    }, 100);

});
