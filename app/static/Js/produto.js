document.addEventListener("DOMContentLoaded", () => {

  console.log("JS carregado");

  const fotos = document.querySelector("#foto");
  const btnAnt = document.querySelector("#ant");
  const btnProx = document.querySelector("#prox");
  const addcart = document.querySelector(".btn-carrinho")
  const carrinhoi = addcart.querySelector("i")
  
  console.log("foto:", fotos);
  console.log("btnAnt:", btnAnt);
  console.log("btnProx:", btnProx);
  
  let indice = 0;

  fotos.src = imagens[indice];

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
    if (indice >= imagens.length) indice = fotos.length - 1;

    fotos.src = imagens[indice];

    atualizarBotoes();
    
    fotos.style.opacity = 0;
    setTimeout(() => {
      fotos.src = imagens[indice];
      fotos.style.opacity = 1;
    }, 200);
  }

  // 🔥 LISTENERS (o que faltava)
  btnProx.addEventListener("click", () => trocarFoto("prox"));
  btnAnt.addEventListener("click", () => trocarFoto("ant"));
  atualizarBotoes();
  
addcart.addEventListener(
    "click",
    async () => {

        const id = addcart.dataset.id;

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
          setTimeout(() => {
            carrinhoi.classList.remove("ri-shopping-cart-2-line")
            carrinhoi.classList.add("ri-shopping-cart-2-fill")
            abrirCarrinho();
            
          } , 1800)
        }
      
     });
});