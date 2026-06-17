const overlay = document.querySelector(".overlay")
const painel = document.querySelector("#filtro-admin")

btnFiltro.addEventListener("click", () => {
  overlay.classList.remove("escondido")
  painel.classList.remove("escondido")
})

overlay.addEventListener("click", () => {
  overlay.classList.add("escondido")
  painel.classList.add("escondido")
})