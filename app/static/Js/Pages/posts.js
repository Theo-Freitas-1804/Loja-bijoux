
document.addEventListener("DOMContentLoaded", ()=>{
  
  
  const btnforms = document.querySelector("#ativar-form")
  const editar = document.querySelector("#aba-editar")
  const novobtn = document.querySelector("#aba-novo")
  const overlayforms = document.querySelector("#overlay-atendentes")
  const formeditar = document.querySelector(".form-editar")
  const formnovo= document.querySelector("#form-novo")
  
  const painelnovo = document.querySelector("#painel-novo")
  const paineleditar= document.querySelector("#painel-editar") 
  
  const editaratendente = document.querySelector(".pip-editar-atendente")
  const checkatendente =
    document.querySelectorAll("input[name='atendentes']");
  
  
  const inputid = document.querySelector("#id-atendente")
  const inputnome = document.querySelector("#nome-atendente")
  const inputcargo =document.querySelector("#cargo-atendente")
  const inputfuncoes = document.querySelector("#funcoes-atendente")
  
  const foto = document.getElementById("foto-atendente");
  const icone = document.getElementById("icone-atendente");

  const promoverbtn = document.querySelector("#select-promover")
  const overlaypromover = document.querySelector("#overlay-bijoux")
  
  const fecharpromover = document.querySelector(".btn-fechar")
  
  console.log("Valor do input" , inputid)
  console.log("Valor do input" , inputnome)
  console.log("Valor do input" , inputcargo)
  console.log("Valor do input" , inputfuncoes)
  
  
  checkatendente.forEach((check) => {
      check.checked = false;
  });
 
  btnforms.addEventListener("click" , ()=>{
    overlayforms.classList.remove("escondido")
  })
  
  editar.addEventListener("click" , () => {
    paineleditar.classList.remove("escondido")
    painelnovo.classList.add("escondido")
    editar.classList.add("ativa")
    novobtn.classList.remove("ativa")
  })
  
  novobtn.addEventListener("click" , ()=>{
    paineleditar.classList.add("escondido")
    painelnovo.classList.remove("escondido")
    editar.classList.remove("ativa")
    novobtn.classList.add("ativa")
  })
  
  overlayforms.addEventListener("click", (event) => {
    if (event.target === event.currentTarget) {
      overlayforms.classList.add("escondido")
    }
  });
  
  checkatendente.forEach((check) => {
    check.addEventListener("change" , async (event)=> {
      editaratendente.classList.remove("escondido")
      
      const id = event.target.value;
      console.log(id);
      
      const url = `/admin/api/gerenciar/atendente/${id}`;
      console.log(url);
      
      const resposta = await fetch(url)
      
      const dados = await resposta.json()
      console.log(dados)
      
      inputid.value = dados.id
      inputnome.value = dados.nome 
      inputcargo.value = dados.cargo
      inputfuncoes.value = dados.especialidade.join(" , ")
      foto.src = dados.foto_url
      if (dados.foto_url) {
        foto.src = dados.foto_url;
        foto.classList.remove("escondido");
        icone.classList.add("escondido");
      } else {
        foto.classList.add("escondido");
        icone.classList.remove("escondido");
      }
    })
  })
  
  formeditar.addEventListener("submit", async (event) => {
    event.preventDefault();
    const dados = new FormData(formeditar);
    const resposta = await fetch(formeditar.action, {
        method: "POST",
        body: dados
    });
    const retorno = await resposta.json();

    console.log(retorno);
    
    if(resposta.ok) {
      abrirModal({titulo: "Salvar alterações", mensagem: "Deseja realmente salvar este atendente?"});
    } else {
      abrirModal({titulo: "Salvar alterações", mensagem: "Erro ao salvar alterações"});
    }
    
  });
  
  promoverbtn.addEventListener("click" , ()=>{
    overlaypromover.classList.remove("escondido")
  })
  fecharpromover.addEventListener("click" , ()=>{
    overlaypromover.classList.add("escondido")
  })
})