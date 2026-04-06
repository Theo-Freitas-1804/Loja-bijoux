document.addEventListener("DOMContentLoaded", () => {
  alert("JS carregado");
  let fila = [];
  const form = document.getElementById("ficha-produtos");
  const btnAdicionar = document.getElementById("adicionar-a-fila");
  const btnEnviar = document.getElementById("btn-enviar");
  const inputFoto = document.getElementById("foto-acessorio");
  const nome = document.getElementById("Nome");
  const colecao = document.getElementById("Colecao");
  const tamanho = document.getElementById("Tamanho");
  const material = document.getElementById("Material");
  const preco = document.getElementById("Preco");
  const estoque = document.getElementById("qtd");
  const preview = document.getElementById("lista-preview");
  function criarProduto(){
    const tipoSelecionado =
    document.querySelector('input[name="categoria"]:checked');
    let listafotos = Array.from(inputFoto.files);
    return {
      nome: nome.value,
      colecao: colecao.value,
      tamanho: tamanho.value,
      material: material.value,
      preco: parseFloat(preco.value.replace(",", ".")) || 0,
      qtd: parseInt(estoque.value) || 0,
      fotos: listafotos,
      tipo: tipoSelecionado ? tipoSelecionado.value : null
    };
}

function validarProduto(produto){
  if(!produto.tipo){
    alert("Escolha o tipo de item");
    return false;
  }
  if(produto.fotos.length ===0){
    alert("Selecione uma foto");
    return false;
  }
  if(produto.tipo === "Bijuteria"){
    if(!produto.nome){
      alert("Nome obrigatório");
      return false;
  }
  if(produto.preco <= 0){
    alert("Preço inválido");
    return false;
  }

  if(produto.qtd <= 0){
    alert("Estoque inválido");
    return false;
  }

}
  return true;

}

function atualizarPreview(){
  preview.innerHTML = "";

  fila.forEach((item) => {
    const li = document.createElement("li");
    const containerImgs = document.createElement("div");
    containerImgs.classList.add("preview-container");
    li.innerHTML = `
    <strong>${item.nome || "Item sem nome"}</strong>
    | Tipo: ${item.tipo}
    | Preço: R$ ${item.preco.toFixed(2)}
    `;
    item.fotos.forEach((foto) => {
      const urlFoto = URL.createObjectURL(foto);
      const img = document.createElement("img");
      img.src = urlFoto;
      img.classList.add("preview-img");
      li.appendChild(img);
    });

    preview.appendChild(li); // ✔ dentro do loop
    
    
    
  });
}

function adicionarFila(){

const produto = criarProduto();

console.log("Produto criado:", produto);

if(!validarProduto(produto)) return;

fila.push(produto);

console.log("Fila atual:", fila);

atualizarPreview();

form.reset();

}

function enviarFila(){
  const dados = new FormData();
  
  if(fila.length === 0){
    alert("Nenhum item na fila");
    return;
  }

  fila.forEach((item) => {

    item.fotos.forEach((foto) => {
      dados.append("foto-acessorio", foto);
    });

    dados.append("qtd-fotos", item.fotos.length);
    dados.append("nome-bijuteria", item.nome);
    dados.append("colecao", item.colecao);
    dados.append("Tamanho", item.tamanho);
    dados.append("material", item.material);
    dados.append("preco", item.preco);
    dados.append("qtd", item.qtd);
    dados.append("categoria", item.tipo);

  });

  console.log([...dados.entries()]); // 👈 MELHOR QUE ALERT

  fetch("/admin/adicionar-novo-acessorio",{
    method:"POST",
    body:dados
  })
  .then(res=>res.text())
  .then(resposta=>{
    console.log(resposta);
    alert("Produtos enviados!");
    fila=[];
    atualizarPreview();
  })
  .catch(erro=>{
    console.error("Erro:",erro);
  });
}

btnAdicionar.addEventListener("click", adicionarFila);

btnEnviar.addEventListener("click", enviarFila);

});
