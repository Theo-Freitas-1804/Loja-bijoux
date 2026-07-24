document.addEventListener("DOMContentLoaded", () => {

  // =========================
  // CARD
  // =========================

  const card =
    document.querySelector(".checkout-card")

  const btnContinue =
    document.querySelector("#btn-continuar")

  const btnVoltar =
    document.querySelector("#btn-voltar")

  // =========================
  // ETAPAS
  // =========================

  const etapas =
    document.querySelectorAll(".etapa")

  const etapa1 = etapas[0]
  const etapa2 = etapas[1]
  const etapa3 = etapas[2]

  const etapaFrete =
    document.querySelector(".subetapa-topo")

  // =========================
  // INPUTS
  // =========================

  const selectEndereco =
    document.querySelector("#enderecos")

  const selectFrete =
    document.querySelector("#frete")

  const selectHorario =
    document.querySelector("#horario")

  const pagamentos =
    document.querySelectorAll(".pagamento-item")

  const agendamentoBox =
    document.querySelector("#agendamento-box")

  // =========================
  // HELPERS
  // =========================

  function ativar(etapa) {

    etapa.classList.remove("inativo")

  }

  function concluir(etapa) {

    etapa.classList.add("concluida")

  }

  // =========================
  // VIRAR CARD
  // =========================

  btnContinue.addEventListener("click", () => {

    card.classList.add("virado")

  })

  btnVoltar.addEventListener("click", (e) => {

    e.preventDefault()

    card.classList.remove("virado")

  })

  // =========================
  // ENDEREÇO -> FRETE
  // =========================

  selectEndereco.addEventListener("change", () => {

    concluir(etapa1)

    ativar(etapaFrete)

  })

  // =========================
  // FRETE -> ETAPA 2
  // =========================

  selectFrete.addEventListener("change", () => {

    concluir(etapaFrete)

    ativar(etapa2)

  })

  // =========================
  // HORÁRIO -> ETAPA 3
  // =========================

  selectHorario.addEventListener("change", () => {

    concluir(etapa2)

    ativar(etapa3)

    // calendário

    if (
      selectHorario.value === "agendado"
    ) {

      agendamentoBox.style.display = "flex"

    } else {

      agendamentoBox.style.display = "none"

    }

  })

  // =========================
  // PAGAMENTO
  // =========================
  
  const inputPagamento =
  document.querySelector("#forma_pagamento")
  
  pagamentos.forEach((botao) => {

    botao.addEventListener("click", () => {

      pagamentos.forEach((item) => {

        item.classList.remove("ativo")

      })

      botao.classList.add("ativo")
      
      inputPagamento.value = botao.dataset.pagamento
      
      concluir(etapa3)

    })

  })
  
  
  
})