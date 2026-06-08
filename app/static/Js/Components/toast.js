// =========================
// TOAST GLOBAL
// =========================
function mostrarToast(mensagem) {

  const toast =
    document.getElementById("toast");

  if (!toast) return;

  toast.textContent = mensagem;

  toast.classList.add("ativo");

  setTimeout(() => {
    toast.classList.remove("ativo");
  }, 2500);

}

// exporta globalmente
window.mostrarToast = mostrarToast;