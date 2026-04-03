// ===============================
// ELEMENTOS
// ===============================
const carrinho = document.getElementById("carrinho-pip");
const container = document.getElementById("conteudo-carrinho");

console.log(container);

// ===============================
// ABRIR / FECHAR CARRINHO
// ===============================
function abrirCarrinho() {
  carrinho.classList.add("ativo");
}

function fecharCarrinho() {
  carrinho.classList.remove("ativo");
}


// ===============================
// BUSCAR DADOS DO CARRINHO
// ===============================
function atualizarCarrinho() {
  fetch("/carrinho/dados")
    .then(res => res.json())
    .then(data => {
      // 👇 🔥 TESTE AQUI
    console.log("DADOS COMPLETOS:", data);
    console.log("ITENS:", data.itens);
    console.log(data.itens.length);
    const container = document.getElementById("conteudo-carrinho");
    
    console.log(`O valor de Container é ${container} `)
    
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
      console.log("PASSOU AQUI 😏"); // 👈 COLOCA AQUI

      atualizarCarrinho();
      abrirCarrinho();
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

document.getElementById("btn-limpar").addEventListener("click", () => {
  alert("clicou em mim")
  fetch("/carrinho/limpar", {
    method: "POST"
  })
  .then(() => {
    atualizarCarrinho();
  });
});