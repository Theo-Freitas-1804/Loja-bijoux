document.addEventListener("DOMContentLoaded" , () =>{
  
  const btnFiltro = document.querySelector("#btn-overlay")
  const overlayFiltro = document.querySelector("#overlay")
  const painel = document.querySelector("#filtro-admin")
  
  btnFiltro.addEventListener("click", () => {
    overlayFiltro.classList.remove("escondido")
    painel.classList.remove("escondido")
  })
  
  overlayFiltro.addEventListener("click", () => {
    overlayFiltro.classList.add("escondido")
    painel.classList.add("escondido")
  })
  
  const selectfiltro =
  document.querySelector(
    'select[name="opcao"]'
  )
  
  const filtros = document.querySelectorAll(".filtro-grupo-admin")
  
  const form = document.querySelector("#admin-form")
  const btnSubmit = form.querySelector('button[type="submit"]')
  
  function EsconderFiltros() {

  document
    .querySelectorAll(".filtro-grupo-admin")
    .forEach(grupo => {
      grupo.classList.add("escondido")
    })

  document
    .querySelector("#titulo-filtro")
    .classList.add("escondido")

  }
  
  function atualizarPainel() {

  EsconderFiltros()

  const mapaFiltros = {
    "ticket_medio": "#ticket",
    "pedidos": "#pedidos",
    "atividades": "#atividade",
    "compra": "#ultimo-pedido"
  }

  const seletor =
    document.querySelector(
      mapaFiltros[selectfiltro.value]
    )

  if (seletor) {
    seletor.classList.remove("escondido")
  }

  document
    .querySelector("#titulo-filtro")
    .classList.remove("escondido")

  form.classList.remove("escondido")
}
  
  selectfiltro.addEventListener(
  "change",
  atualizarPainel
  )
  
  atualizarPainel()
  
  form.addEventListener("submit", async (e) => {
    console.log("Enviei o form!")
    e.preventDefault()
    const dados = Object.fromEntries(new FormData(form))
    const params =
      new URLSearchParams(dados)
  
    const resposta =
  await fetch(
    `/admin/api/clientes?${params}`
  )

  console.log("status:", resposta.status)

  if(resposta.ok) {
    overlayFiltro.classList.add("escondido")
    painel.classList.add("escondido")
  }

const resultado =
  await resposta.json()

console.log(resultado)
    document.querySelector(
      "#coluna-filtro"
    ).textContent =
      resultado.coluna
  
    const linhas =
      document.querySelectorAll(
        "#dados-clientes tbody tr"
      )
  
    linhas.forEach(linha => {
  
      const id =
        Number(
          linha.children[0].textContent
        )
  
      const cliente =
        resultado.dados.find(
          c => c.id === id
        )
  
      if (!cliente) return
  
      linha.children[5].textContent =
        cliente.valor
    })
  })
  
  const btnsadmin = document.querySelectorAll(".toggle")
  btnsadmin.forEach(btn =>{
    btn.addEventListener("click" , () =>{
      const coluna = btn.dataset.coluna
      document.querySelectorAll(
    `[data-coluna="${coluna}"]`).forEach(elemento =>{ 
      elemento.classList.toggle("escondido")
    })
      
    })
  })
  
  const btncolunas = document.querySelector("#btn-colunas")
  
  const painelColunas= document.querySelector("#painel-colunas")
  
  btncolunas.addEventListener("click", () => {
    overlayFiltro.classList.remove("escondido")
    painelColunas.classList.remove("escondido")
  })
  overlayFiltro.addEventListener("click" , ()=>{
    overlayFiltro.classList.add("escondido")
    painelColunas.classList.add("escondido")
  })
})
