document.addEventListener("DOMContentLoaded", function () {
  console.log("checkout.js carregou")
  const btncontinue = document.querySelector("#btn-continuar")
  const card = document.querySelector(".checkout-card")
  console.log(btncontinue)
  console.log(card)
  btncontinue.addEventListener("click", () => {
    console.log("clicou")
    card.classList.toggle("virado")
  })
  
  const btnVoltar =
  document.querySelector("#btn-voltar")
  if (btnVoltar && card) {
    btnVoltar.addEventListener("click", (e) => {
      e.preventDefault()
      card.classList.remove("virado")
  })
}
  
})