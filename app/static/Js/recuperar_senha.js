// ===== ETAPAS =====
const formEmail = document.getElementById("form-email");
const etapaEmail = document.getElementById("etapa-email");
const etapaCodigo = document.getElementById("etapa-codigo");
const novasenha = document.getElementById("nova-senha")
// quando enviar email
formEmail.addEventListener("submit", function(e) {

  etapaEmail.classList.add("escondido");
  etapaCodigo.classList.remove("escondido");

});

const inputs = document.querySelectorAll(".codigo input");

inputs.forEach((input, index) => {

  input.addEventListener("input", () => {
    if (input.value.length === 1 && index < inputs.length - 1) {
      inputs[index + 1].focus();
    }
  });

  input.addEventListener("keydown", (e) => {
    if (e.key === "Backspace" && input.value === "" && index > 0) {
      inputs[index - 1].focus();
    }
  });

});

document.getElementById("form-codigo").addEventListener("submit", function(e) {
  e.preventDefault();

  let codigo = "";

  inputs.forEach(input => {
    codigo += input.value;
  });

  console.log("Código digitado:", codigo);

  // 👉 troca de etapa aqui
  etapaCodigo.classList.add("escondido");
  novasenha.classList.remove("escondido");

});