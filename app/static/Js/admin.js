document.addEventListener("DOMContentLoaded", () => {
  
  const btnMais = document.getElementById("btn-mais");
const painelMais = document.getElementById("painel-mais");

btnMais.addEventListener("click", () => {
    painelMais.classList.toggle("escondido");
});

const btnMarketing = document.getElementById("btn-marketing");
const submenuMarketing = document.getElementById("submenu-marketing");

btnMarketing.addEventListener("click", () => {
    submenuMarketing.classList.toggle("escondido");
});
})