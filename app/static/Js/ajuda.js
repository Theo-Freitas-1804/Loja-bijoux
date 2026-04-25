document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("form-chat");
  const input = document.getElementById("input-chat");
  const resposta = document.getElementById("chat-box");

  const btn = document.querySelector("#nova-chamada");
  const intro = document.querySelector(".introducao");

  console.log("btn:", btn);
  console.log("form:", form);
  console.log("intro:", intro);

  // 👉 botão abrir chat
  if (btn && form && intro) {
    btn.addEventListener("click", () => {
      form.classList.remove("escondido");
      intro.classList.add("escondido");
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

      if (!mensagem) return; // evita envio vazio

      // 👤 usuário
      const userMsg = document.createElement("div");
      userMsg.className = "msg user";
      userMsg.textContent = mensagem;
      resposta.appendChild(userMsg);

      input.value = "";

      // 🤖 loading
      const loading = document.createElement("div");
      loading.className = "msg bot";
      loading.textContent = "Digitando...";
      resposta.appendChild(loading);

      fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pergunta: mensagem })
      })
      .then(res => res.json())
      .then(data => {
        loading.remove();

        const botMsg = document.createElement("div");
        botMsg.className = "msg bot";
        botMsg.textContent = data.mensagem;
        resposta.appendChild(botMsg);

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