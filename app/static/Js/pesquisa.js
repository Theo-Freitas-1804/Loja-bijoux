const btn = document.querySelector(".btn-filtro");
const painel = document.getElementById("painel-filtros");
const overlay = document.getElementById("overlay");

// ABRIR
btn.addEventListener("click", () => {
  painel.classList.remove("escondido");
  overlay.classList.remove("escondido");
});

// FECHAR clicando fora
overlay.addEventListener("click", () => {
  painel.classList.add("escondido");
  overlay.classList.add("escondido");
});

// EXTRA: fechar com ESC
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    painel.classList.add("escondido");
    overlay.classList.add("escondido");
  }
});