alert("JS carregado");

document.addEventListener("DOMContentLoaded", () => {
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
    return {
      nome: nome.value,
      colecao: colecao.value,
      tamanho: tamanho.value,
      material: material.value,
      preco: parseFloat(preco.value.replace(",", ".")) || 0,
      qtd: parseInt(estoque.value) || 0,
      foto: inputFoto.files[0],
      tipo: tipoSelecionado ? tipoSelecionado.value : null
};
}

function validarProduto(produto){
  if(!produto.tipo){
    alert("Escolha o tipo de item");
    return false;
  }
  if(!produto.foto){
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
  fila.forEach(item => {
    const li = document.createElement("li");
    const urlFoto = URL.createObjectURL(item.foto);
    li.innerHTML = `
    <img src="${urlFoto}" width="60" style="border-radius:5px;margin-right:10px;">
    <strong>${item.nome || "Item sem nome"}</strong>
    | Tipo: ${item.tipo}
    | Preço: R$ ${item.preco.toFixed(2)}
`;
  preview.appendChild(li);

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
  if(fila.length === 0){
    alert("Nenhum item na fila");
    return;
}
  const dados = new FormData();

  fila.forEach((item)=>{
  
  dados.append("foto-acessorio", item.foto);
  dados.append("nome-bijuteria", item.nome);
  dados.append("colecao", item.colecao);
  dados.append("Tamanho", item.tamanho);
  dados.append("material", item.material);
  dados.append("preco", item.preco);
  dados.append("qtd", item.qtd);
  dados.append("categoria", item.tipo);
  
  });
  
  alert([...dados.entries()]);
  /* futuro envio real */
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