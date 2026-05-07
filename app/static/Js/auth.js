document.addEventListener("DOMContentLoaded", function () {

  // ===============================
  // 🔄 FLIP CARD (login/cadastro)
  // ===============================
  const card = document.querySelector(".card");
  const btnEntrar = document.querySelector("#btn-virar-login");
  const btnCadastro = document.querySelector("#btn-virar-cadastro");

  if (btnEntrar && card) {
    btnEntrar.addEventListener("click", (e) => {
      e.preventDefault();
      card.classList.add("virado");
    });
  }

  if (btnCadastro && card) {
    btnCadastro.addEventListener("click", (e) => {
      e.preventDefault();
      card.classList.remove("virado");
    });
  }

  // ===============================
  // 👁️ TOGGLE SENHA
  // ===============================
  
  const button = document.getElementById("btn_senha");
  const inputSenha = document.getElementById("senha_cliente");
  const icone = document.getElementById("icone_senha");
  if (button && inputSenha && icone) {
    let visivel = false;
    button.addEventListener("click", () => {
      visivel = !visivel;
      inputSenha.type = visivel ? "text" : "password";
      // 🔥 troca ícone
      icone.classList.toggle("ri-eye-line", !visivel);
      icone.classList.toggle("ri-eye-close-line", visivel);
    });
  }
  // ===============================
  // ✏️ VALIDAÇÃO CAMPO LOGIN
  // ===============================
  const campo = document.querySelector('input[name="id_cliente"]');

  if (campo) {
    campo.addEventListener("input", () => {
      const valor = campo.value.trim();

      const ehEmail = valor.includes("@");
      const ehNome = valor.length >= 3;

      campo.classList.toggle("sucesso", ehEmail || ehNome);
      campo.classList.toggle("erro", !(ehEmail || ehNome));
    });
  }

  // ===============================
  // ⏳ LOADING BOTÃO
  // ===============================
  const forms = document.querySelectorAll(".form-login");

forms.forEach((form) => {
  form.addEventListener("submit", function (e) {
    const btn = form.querySelector('button[type="submit"]');

    if (!btn) return;

    e.preventDefault();

    btn.classList.add("loading");
    btn.textContent = "Entrando...";

    setTimeout(() => {
      btn.classList.remove("loading");
      btn.classList.add("success");
      btn.textContent = "Bem-vinda!";

      setTimeout(() => {
        form.submit();
      }, 800);
    }, 1200);
  });
});

});