document.addEventListener("DOMContentLoaded", function () {

  const botoes = document.querySelectorAll(".opcao-lista");
  const secoes = document.querySelectorAll(".opcao-nav");

  botoes.forEach(botao => {
    botao.addEventListener("click", function () {

      // 🔥 remove ativo de todos
      botoes.forEach(b => b.classList.remove("ativo"));

      // 🔥 ativa o clicado
      this.classList.add("ativo");

      // 🔥 pega o alvo do data-*
      const alvo = this.dataset.aba;

      // 🔥 esconde todas as seções
      secoes.forEach(secao => secao.classList.add("escondido"));

      // 🔥 mostra a seção correspondente
      const secaoAtiva = document.querySelector(`#${alvo}`);
      if (secaoAtiva) {
        secaoAtiva.classList.remove("escondido");
      }

    });
  });

});