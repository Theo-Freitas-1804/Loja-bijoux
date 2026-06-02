document.addEventListener("DOMContentLoaded", () => {

  console.log("JS carregado");

  const foto = document.querySelector("#foto");
  const btnAnt = document.querySelector("#ant");
  const btnProx = document.querySelector("#prox");
  const btncarrinho = document.querySelector(".btn-carrinho")
  let indice = 0;

  foto.src = imagens[indice];

  function atualizarBotoes() {
    if (indice === 0) {
      btnAnt.disabled = true;
      btnAnt.classList.add("desativado");
    } else {
      btnAnt.disabled = false;
      btnAnt.classList.remove("desativado");
    }

    if (indice === imagens.length - 1) {
      btnProx.disabled = true;
      btnProx.classList.add("desativado");
    } else {
      btnProx.disabled = false;
      btnProx.classList.remove("desativado");
    }
  }

  function trocarFoto(direcao) {
    if (direcao === "prox") {
      indice++;
    } else {
      indice--;
    }

    if (indice < 0) indice = 0;
    if (indice >= imagens.length) indice = imagens.length - 1;

    foto.src = imagens[indice];

    atualizarBotoes();
    
    foto.style.opacity = 0;
    setTimeout(() => {
  foto.src = imagens[indice];
  foto.style.opacity = 1;

  }, 200);
  }

  // 🔥 LISTENERS (o que faltava)
  btnProx.addEventListener("click", () => trocarFoto("prox"));
  btnAnt.addEventListener("click", () => trocarFoto("ant"));
  atualizarBotoes();
  
btncarrinho.addEventListener(
    "click",
    async () => {

        const id =
            btncarrinho.dataset.id;

        const resposta =
            await fetch(
                `/adicionar-carrinho/${id}`,
                {
                    method: "POST"
                }
            );

        const dados =
            await resposta.json();

        console.log(dados);

        if(resposta.ok) {
          btncarrinho.classList.add("sucesso")
          abrirCarrinho();
          setTimeout(() => {
            btncarrinho.classList.remove("sucesso")
          } , 1800)
        }
      
     });
});