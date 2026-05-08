// ===============================
// ELEMENTOS
// ===============================
const carrinho = document.getElementById("carrinho-pip");
const container = document.getElementById("conteudo-carrinho");

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

      data.itens.forEach(item => {
        const html = `
          <div class="item-carrinho">
            <img src="/static/imagens/UPLOADS_FOTOS_BIJOUX/${item.imagem}">
            <div>
              <p>${item.nome}</p>
              <p>R$ ${item.preco}</p>
              <p>Qtd: ${item.quantidade}</p>
            </div>
          </div>
        `;
        container.innerHTML += html;
      });
    });
}

// ===============================
// ADICIONAR AO CARRINHO
// ===============================
document.querySelectorAll(".btn-carrinho").forEach(btn => {

  btn.addEventListener("click", () => {

    const id = btn.dataset.id;

    fetch(`/adicionar-carrinho/${id}`, {
      method: "POST"
    })

    .then(res => res.json())

    .then(() => {

      // feedback visual
      btn.classList.add("adicionado");

      btn.innerHTML = `
        <i class="ri-check-line"></i>
        Adicionado!
      `;

      atualizarCarrinho();
      abrirCarrinho();

      setTimeout(() => {

        btn.classList.remove("adicionado");

        btn.innerHTML = `
          <i class="ri-shopping-bag-line"></i>
          Adicionar ao carrinho
        `;

      }, 1500);

    });

  });

});
// ===============================
// BOTÃO FECHAR
// ===============================
const btnFechar = document.getElementById("fechar-carrinho");

if (btnFechar) {
  btnFechar.addEventListener("click", fecharCarrinho);
}

// ===============================
// LIMPAR CARRINHO
// ===============================
const btnLimpar = document.getElementById("btn-limpar");

if (btnLimpar) {
  btnLimpar.addEventListener("click", () => {
    fetch("/carrinho/limpar", { method: "POST" })
      .then(() => atualizarCarrinho());
  });
}

// ===============================
// EXPORT GLOBAL (IMPORTANTE)
// ===============================
window.abrirCarrinho = abrirCarrinho;