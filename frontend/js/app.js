const output = document.getElementById("output");
const button = document.getElementById("backend-test-button");

button.addEventListener("click", async () => {
    output.textContent = "Calling Python backend...";

    try {
        const result = await window.pywebview.api.ping_backend();
        output.textContent = JSON.stringify(result, null, 2);
    } catch (error) {
        output.textContent = `Backend call failed:\n${error}`;
    }
});