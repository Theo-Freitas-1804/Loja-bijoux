document.addEventListener("DOMContentLoaded", () => {

  // ===============================
  // 🔄 FLIP CARD (login/cadastro)
  // ===============================
  const card = document.querySelector(".card");
  const btnEntrar = document.querySelector("#btn-virar-login");
  const btnCadastro = document.querySelector("#btn-virar-cadastro");
  const frente = document.querySelector(".front");
  const verso = document.querySelector(".back");
  btnEntrar?.addEventListener("click", (e) => {
    console.log("Entrar clicado");
    e.preventDefault();
    card.classList.add("virado");
    ajustarAltura()
  });

  btnCadastro?.addEventListener("click", (e) => {
    e.preventDefault();
    card.classList.remove("virado");
    ajustarAltura()
  });
  
  // ===============================
// 👁️ TOGGLE SENHAS
// ===============================

document.querySelectorAll(".campo-senha").forEach((campo) => {

    const input = campo.querySelector("input");
    const botao = campo.querySelector(".btn-senha");
    const icone = campo.querySelector(".icone-senha");

    botao.addEventListener("click", () => {

        const visivel = input.type === "password";

        input.type = visivel ? "text" : "password";

        icone.classList.toggle("ri-eye-line", !visivel);
        icone.classList.toggle("ri-eye-close-line", visivel);

    });

});
  
  // ===============================
  // 🔒 VALIDAÇÃO SENHAS CADASTRO
  // ===============================
  const senhaCadastro = document.getElementById("senha");
  const confirmarSenha = document.getElementById("confirmar_senha");
  const msgSenha = document.getElementById("msg-senha");

  function validarSenhas() {

    if (!senhaCadastro || !confirmarSenha || !msgSenha) return;

    if (confirmarSenha.value === "") {

      confirmarSenha.classList.remove("erro", "sucesso");
      msgSenha.textContent = "";
      msgSenha.className = "";

      return;

    }

    const iguais = senhaCadastro.value === confirmarSenha.value;

    confirmarSenha.classList.toggle("sucesso", iguais);
    confirmarSenha.classList.toggle("erro", !iguais);

    if (iguais) {

      msgSenha.textContent = "✓ As senhas coincidem";
      msgSenha.className = "sucesso";

    } else {

      msgSenha.textContent = "✕ As senhas não coincidem";
      msgSenha.className = "erro";

    }

  }

  senhaCadastro?.addEventListener("input", validarSenhas);
  confirmarSenha?.addEventListener("input", validarSenhas);
  
  // ===============================
  // 🪪 MÁSCARA CPF
  // ===============================

  document.querySelectorAll(".campo-cpf").forEach((campo) => {
    campo.addEventListener("input", () => {
      let valor = campo.value.replace(/\D/g, "");
      valor = valor.substring(0, 11);
      valor = valor.replace(/^(\d{3})(\d)/, "$1.$2");
      valor = valor.replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3");
      valor = valor.replace(/\.(\d{3})(\d)/, ".$1-$2");
      campo.value = valor;
    });
  });
  // ===============================
  // ✏️ VALIDAÇÃO CAMPO LOGIN
  // ===============================
  const campo = document.querySelector('input[name="id_cliente"]');

  campo?.addEventListener("input", () => {

    const valor = campo.value.trim();

    const ehEmail = valor.includes("@");
    const ehNome = valor.length >= 3;

    campo.classList.toggle("sucesso", ehEmail || ehNome);
    campo.classList.toggle("erro", !(ehEmail || ehNome));

  });

  // ===============================
  // ⏳ LOADING BOTÕES
  // ===============================
  const forms = document.querySelectorAll(".form-login");

  forms.forEach((form) => {

    form.addEventListener("submit", (e) => {

      const btn = form.querySelector('button[type="submit"]');

      if (!btn) return;

      // ---------------------------
      // Cadastro
      // ---------------------------
      if (form.classList.contains("form-cadastro")) {

        if (senhaCadastro.value !== confirmarSenha.value) {

          e.preventDefault();

          confirmarSenha.focus();

          msgSenha.textContent = "✕ As senhas não coincidem";
          msgSenha.className = "erro";

          return;

        }

      }

      e.preventDefault();

      btn.classList.add("loading");

      if (form.classList.contains("form-cadastro")) {

        btn.textContent = "Criando conta...";

      } else {

        btn.textContent = "Entrando...";

      }

      setTimeout(() => {

        btn.classList.remove("loading");
        btn.classList.add("success");

        if (form.classList.contains("form-cadastro")) {

          btn.textContent = "Conta criada!";

        } else {

          btn.textContent = "Bem-vinda!";

        }

        setTimeout(() => {

          form.submit();

        }, 800);

      }, 1200);

    });

  });
  
  function ajustarAltura() {
    if (!card || !frente || !verso) return;
    const altura = Math.max(frente.scrollHeight,verso.scrollHeight);
    card.style.height = altura + "px";
  }
  
  ajustarAltura()
  window.addEventListener("resize" , ajustarAltura)
});