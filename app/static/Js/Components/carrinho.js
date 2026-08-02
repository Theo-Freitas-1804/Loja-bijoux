// ===============================
// ELEMENTOS
// ===============================
const carrinho =
  document.getElementById("carrinho-pip");

const container =
  document.getElementById("conteudo-carrinho");

// ===============================
// ABRIR / FECHAR CARRINHO
// ===============================
function abrirCarrinho() {

  if (carrinho) {
    carrinho.classList.add("ativo");
  }

}

function fecharCarrinho() {

  if (carrinho) {
    carrinho.classList.remove("ativo");
  }

}

// ===============================
// BUSCAR DADOS DO CARRINHO
// ===============================
function atualizarCarrinho() {

  fetch("/carrinho/dados")

    .then(res => res.json())

    .then(data => {

      if (!container) return;

      container.innerHTML = "";

      if (!data.itens.length) {

        container.innerHTML = `
          <p class="carrinho-vazio">
            Seu carrinho está vazio 🛒
          </p>
        `;

        return;
      }

      data.itens.forEach(item => {

        container.innerHTML += `
          <div class="item-carrinho">

            <img src="/static/imagens/UPLOADS_FOTOS_BIJOUX/${item.imagem}">

            <div>
              <p>${item.nome}</p>
              <p>R$ ${item.preco}</p>
              <p>Qtd: ${item.quantidade}</p>
            </div>

          </div>
        `;

      });

    })

    .catch(err => {

      console.error(
        "Erro ao atualizar carrinho:",
        err
      );

    });

}

// ===============================
// ADICIONAR AO CARRINHO
// ===============================
document
  .querySelectorAll(".btn-carrinho")

  .forEach(btn => {

    btn.addEventListener("click", () => {
      
      console.log("CARRINHO.JS DISPAROU");
      
      // ===============================
      // VERIFICA LOGIN
      // ===============================
      const logado =
        btn.dataset.logado === "true";

      if (!logado) {

        mostrarToast(
          "🔒 Faça login para usar o carrinho"
        );

        return;
      }

      // ===============================
      // ID PRODUTO
      // ===============================
      const id = btn.dataset.id;

      // ===============================
      // FETCH
      // ===============================
      fetch(`/adicionar-carrinho/${id}`, {
        method: "POST"
      })

      .then(res => res.json())

      .then(() => {

        // anima botão
        btn.classList.add("adicionado");

        // atualiza dados
        atualizarCarrinho();

        // abre depois
        setTimeout(() => {

          abrirCarrinho();

        }, 1200);

        // remove animação
        setTimeout(() => {

          btn.classList.remove("adicionado");

        }, 1500);

      })

      .catch(err => {

        console.error(
          "Erro no carrinho:",
          err
        );

      });

    });

  });

// ===============================
// FECHAR CARRINHO
// ===============================
const btnFechar =
  document.getElementById("fechar-carrinho");

if (btnFechar) {

  btnFechar.addEventListener(
    "click",
    fecharCarrinho
  );

}

// ===============================
// LIMPAR CARRINHO
// ===============================
const btnLimpar =
  document.getElementById("btn-limpar");

if (btnLimpar) {

  btnLimpar.addEventListener("click", () => {

    fetch("/carrinho/limpar", {
      method: "POST"
    })

    .then(() => {

      atualizarCarrinho();

    });

  });

}

// ===============================
// CARREGA AO ABRIR A PÁGINA
// ===============================
document.addEventListener(
  "DOMContentLoaded",
  atualizarCarrinho
);

// ===============================
// EXPORT GLOBAL
// ===============================
window.abrirCarrinho = abrirCarrinho;
window.atualizarCarrinho =atualizarCarrinho