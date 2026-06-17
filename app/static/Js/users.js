const btnFiltro = document.querySelector("#btn-overlay")
const overlayFiltro = document.querySelector("#overlay")
const painel = document.querySelector("#filtro-admin")

btnFiltro.addEventListener("click", () => {
  overlayFiltro.classList.toggle("escondido")
  painel.classList.toggle("escondido")
})

overlayFiltro.addEventListener("click", () => {
  overlayFiltro.classList.toggle("escondido")
  painel.classList.toggle("escondido")
})