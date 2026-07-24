// =========================
// TOAST GLOBAL
// =========================
function mostrarToast(mensagem, categoria = "success") {

    const toast = document.getElementById("toast");

    if (!toast) return;

    toast.textContent = mensagem;

    // opcional: muda a cor conforme a categoria
    toast.className = "";
    toast.classList.add("ativo", categoria);

    setTimeout(() => {
        toast.classList.remove("ativo");
    }, 2500);
}

window.mostrarToast = mostrarToast;

// =========================
// FLASH DO FLASK
// =========================
if (typeof flashes !== "undefined" && flashes.length > 0) {
    flashes.forEach(([categoria, mensagem]) => {
        mostrarToast(mensagem, categoria);
    });
}