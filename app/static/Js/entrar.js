document.addEventListener("DOMContentLoaded", function () {

  let button = document.getElementById("btn_senha");
  let inputSenha = document.getElementById("senha_cliente");

  let ver = document.getElementById("ver_senha");

  let visivel = false;
  
  button.addEventListener("click", function () {
    visivel = !visivel;
    if (visivel) {
      inputSenha.type = "text";
      ver.className = "ri-eye-close-line";
    } else {
      inputSenha.type = "password";
      ver.className = "ri-eye-line";
    }
});

const campo = document.querySelector('input[name="id_cliente"]');
campo.addEventListener("input", function() {
  const valor = campo.value.trim();
  const ehEmail = valor.includes("@");
  const ehNome = valor.length >= 3; // mínimo aceitável
  if (ehEmail || ehNome) {
    campo.classList.remove("erro");
    campo.classList.add("sucesso");
  } else {
    campo.classList.remove("sucesso");
    campo.classList.add("erro");
  }
});

const form = document.querySelector(".form-login");
const btn = document.querySelector("#entrar");

form.addEventListener("submit", function (e) {
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

  }, 1200); // 👈 faltava tempo aqui
});

});