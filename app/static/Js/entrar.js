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

});