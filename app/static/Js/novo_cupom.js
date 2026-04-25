document.addEventListener("DOMContentLoaded", function () {

  const radios = document.querySelectorAll('input[name="tipo"]')
  const secoes = ["porcentagem", "fixo"]
  
  const check = document.getElementById("sem-expiracao")
  const data = document.getElementById("campo-data")
  check.addEventListener("change", () => {
  if (check.checked) {
    data.disabled = true
    data.value = ""
  } else {
    data.disabled = false
  }
})
  
  radios.forEach(radio => {
    radio.addEventListener("change", function () {

      // esconde tudo
      secoes.forEach(id => {
        document.getElementById(id).classList.add("escondido")
      })

      // mostra o selecionado
      const alvo = this.value
      document.getElementById(alvo).classList.remove("escondido")

    })
  })

})