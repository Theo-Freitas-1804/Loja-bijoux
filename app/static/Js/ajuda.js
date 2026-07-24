let anexosPendentes = []

function CriarRespostaBot(nome, hora, mensagem, classeExtra = "", imagens = []) {

  const botContainer = document.createElement("div");
  botContainer.className = `mensagem-bot ${classeExtra}`;

  const botTopo = document.createElement("div");
  botTopo.className = "topo-msg";

  const botNome = document.createElement("small");
  botNome.textContent = nome;

  const botHora = document.createElement("small");
  botHora.textContent = hora;

  botTopo.appendChild(botNome);
  botTopo.appendChild(botHora);

  const botMsg = document.createElement("div");
  botMsg.className = "msg bot";

  botMsg.innerHTML = mensagem;

  // ==========================
  // Imagens da resposta
  // ==========================

  if (imagens) {

    // Aceita tanto uma string quanto uma lista
    const lista = Array.isArray(imagens) ? imagens : [imagens];

    for (const caminho of lista) {

      const imagem = document.createElement("img");

      imagem.src = caminho;
      imagem.classList.add("imagem-chat");

      botMsg.appendChild(imagem);

    }

  }

  botContainer.appendChild(botTopo);
  botContainer.appendChild(botMsg);

  return botContainer;

}

function adicionarMidia(arquivo , areapreview) {
  if (!arquivo) return;

  const img = document.createElement("img");
  const item = document.createElement("div")
  
  
  item.className = "preview-item"
  img.src = URL.createObjectURL(arquivo);
  
  const btnexcluir = document.createElement("button")
  btnexcluir.className= "remover-btn"
  btnexcluir.innerHTML = "<i class='ri-close-line'></i>"
  btnexcluir.addEventListener("click" , ()=>{
    item.remove()
  })
  item.appendChild(img)
  item.appendChild(btnexcluir)
  areapreview.appendChild(item)
}

function abrirSeletorMidia(input) {
  input.click();
}

function selecionarMidia(input , areapreview) {
  const arquivo = input.files[0]
  if(!arquivo) return;
  anexosPendentes.push(arquivo)
  console.log(anexosPendentes);
  adicionarMidia(arquivo , areapreview)
}

document.addEventListener("DOMContentLoaded", () => {
  
  const form = document.getElementById("form-chat");
  const input = document.getElementById("input-chat");
  const resposta = document.getElementById("chat-box");

  const btn = document.querySelector("#nova-chamada");
  const intro = document.querySelector(".introducao");
  
  // Menu select de imagens //
  
  const btnmidia = document.querySelector("#btn-arquivo")
  const inputmidia = document.querySelector("#input-midia")
  
  const areapreview = document.querySelector(".anexos-pendentes")
  
  

  
  // 👉 botão abrir chat
  if (btn && form && intro) {

    btn.addEventListener("click", () => {

      form.classList.remove("escondido");
      intro.classList.add("escondido");

      // evita duplicar mensagem inicial
      if (document.querySelector(".mensagem-boasvindas")) {
        return;
      }

      const agora = new Date();

      const hora =
        agora.getHours().toString().padStart(2, "0") +
        ":" +
        agora.getMinutes().toString().padStart(2, "0");

      const mensagemBoasVindas = CriarRespostaBot(
        atendente.nome,
        hora,
        saudacaoInicial,
        "mensagem-boasvindas"
      );

      resposta.appendChild(mensagemBoasVindas);

      resposta.scrollTop = resposta.scrollHeight;

    });

  }

  // 👉 envio de mensagem
  if (form) {

    form.addEventListener("submit", function(e) {

      e.preventDefault();

      if (intro) {
        intro.classList.add("escondido");
      }

      const mensagem = input.value.trim();

      if (!mensagem) return;

      // =========================
      // 👤 MENSAGEM USUÁRIA
      // =========================

      const userContainer = document.createElement("div");
      userContainer.className = "user-container";

      const userTopo = document.createElement("div");
      userTopo.className = "topo-msg";

      const userNome = document.createElement("small");
      userNome.textContent = nomeCliente;

      const agora = new Date();

      const horaUsuario =
        agora.getHours().toString().padStart(2, "0") +
        ":" +
        agora.getMinutes().toString().padStart(2, "0");

      const userHora = document.createElement("small");
      userHora.textContent = horaUsuario;

      userTopo.appendChild(userNome);
      userTopo.appendChild(userHora);

      const userMsg = document.createElement("div");
      userMsg.className = "msg user";
      userMsg.textContent = mensagem;

      userContainer.appendChild(userTopo);
      userContainer.appendChild(userMsg);

      resposta.appendChild(userContainer);

      resposta.scrollTop = resposta.scrollHeight;

      input.value = "";

      // =========================
      // 🤖 LOADING
      // =========================

      const loading = document.createElement("div");
      loading.className = "msg bot";
      loading.textContent = "Digitando...";

      resposta.appendChild(loading);

      resposta.scrollTop = resposta.scrollHeight;

      // =========================
      // 🤖 FETCH BOT
      // =========================
      
      const formData = new FormData();
      formData.append("pergunta", mensagem);
      for (const arquivo of anexosPendentes) {
        formData.append("arquivos", arquivo);
      }
      
      fetch("/chat", {

        method: "POST",
        body: formData
      })

      .then(res => res.json())

      .then(data => {

        loading.remove();
        
        for (const msg of data.mensagens) {
          const respostaBot = CriarRespostaBot(
            msg.atendente.nome,
            msg.hora,
            msg.mensagem,
            "",
            msg.imagens
          );
          resposta.appendChild(respostaBot);
        }
        


        resposta.scrollTop = resposta.scrollHeight;

      })

      .catch(() => {

        loading.remove();

        const erro = document.createElement("div");
        erro.className = "msg bot";
        erro.textContent = "Erro ao buscar resposta 😢";

        resposta.appendChild(erro);

      });

    });

  }
  
  const btnextra = document.querySelector("#btn-popup-mais")
  
  const painelopcoes = document.querySelector(".popup-mais")
  
  btnextra.addEventListener("click" , () =>{
    painelopcoes.classList.toggle("escondido")
  })
  
  const btnlimpar = document.querySelector("#btn-limpar")
  const btnnovo = document.querySelector("#btn-novo")
  btnlimpar.addEventListener("click" , () =>{
    resposta.innerHTML = ""
    mostrarToast("A conversa foi limpa , mas está salva no seu histórico.")
    intro.classList.remove("escondido")
    painelopcoes.classList.add("escondido")
  })
  btnnovo.addEventListener("click" , ()=>{
    abrirModal({
      titulo: "Nova conversa",
      mensagem: "Deseja abrir uma nova conversa? A atual continuará disponível no histórico.",
      confirmarMsg: "Sim, abrir",
      cancelarMsg: "Não, continuar",
      onConfirmar: () => {
        resposta.innerHTML = "";
        mostrarToast("Nova conversa iniciada!");
      }
    });
  })
  
  // Ligando o input de mídia //
  
  btnmidia.addEventListener("click", () => abrirSeletorMidia(inputmidia));
  
  inputmidia.addEventListener("change", () => {
    selecionarMidia(inputmidia, areapreview);
  });
  
  for (const arquivo of inputmidia.files) {
    adicionarMidia(arquivo , areapreview);
  }
  
});