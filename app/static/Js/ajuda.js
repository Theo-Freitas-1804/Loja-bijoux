document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("form-chat");
  const input = document.getElementById("input-chat");
  const resposta = document.getElementById("chat-box");

  const btn = document.querySelector("#nova-chamada");
  const intro = document.querySelector(".introducao");

  // 👉 botão abrir chat
  if (btn && form && intro) {

    btn.addEventListener("click", () => {

      form.classList.remove("escondido");
      intro.classList.add("escondido");

      // evita duplicar mensagem inicial
      if (document.querySelector(".mensagem-boasvindas")) {
        return;
      }

      // =========================
      // 🤖 SAUDAÇÃO INICIAL
      // =========================

      const botContainer = document.createElement("div");
      botContainer.className = "mensagem-bot mensagem-boasvindas";

      const botTopo = document.createElement("div");
      botTopo.className = "topo-msg";

      const botNome = document.createElement("small");
      botNome.textContent = nomeAtendente;

      const botHora = document.createElement("small");

      const agora = new Date();

      botHora.textContent =
        agora.getHours().toString().padStart(2, "0") +
        ":" +
        agora.getMinutes().toString().padStart(2, "0");

      botTopo.appendChild(botNome);
      botTopo.appendChild(botHora);

      const botMsg = document.createElement("div");
      botMsg.className = "msg bot";
      botMsg.textContent = saudacaoInicial;

      botContainer.appendChild(botTopo);
      botContainer.appendChild(botMsg);

      resposta.appendChild(botContainer);

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

      fetch("/chat", {

        method: "POST",

        headers: {
          "Content-Type": "application/json"
        },

        body: JSON.stringify({
          pergunta: mensagem
        })

      })

      .then(res => res.json())

      .then(data => {

        loading.remove();

        // =========================
        // 🤖 MENSAGEM BOT
        // =========================

        const botContainer = document.createElement("div");
        botContainer.className = "mensagem-bot";

        const botTopo = document.createElement("div");
        botTopo.className = "topo-msg";

        const botNome = document.createElement("small");
        botNome.textContent = data.atendente;

        const botHora = document.createElement("small");
        botHora.textContent = data.hora;

        botTopo.appendChild(botNome);
        botTopo.appendChild(botHora);

        const botMsg = document.createElement("div");
        botMsg.className = "msg bot";
        botMsg.innerHTML = data.mensagem;

        botContainer.appendChild(botTopo);
        botContainer.appendChild(botMsg);

        resposta.appendChild(botContainer);

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

});