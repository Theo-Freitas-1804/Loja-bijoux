const btn = document.getElementById("btn-perfil");
const menu = document.getElementById("menu-dropdown");

// ===============================
// DROPDOWN PERFIL
// ===============================
if (btn && menu) {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    menu.classList.toggle("escondido");
  });

  document.addEventListener("click", (e) => {
    if (!menu.contains(e.target) && !btn.contains(e.target)) {
      menu.classList.add("escondido");
    }
  });
}

// ===============================
// ABRIR CARRINHO PELO DROPDOWN
// ===============================
const btnVer = document.getElementById("btn-ver-carrinho");

if (btnVer) {
  btnVer.addEventListener("click", (e) => {
    e.preventDefault();

    if (menu) {
      menu.classList.add("escondido"); // fecha dropdown
    }

    if (window.abrirCarrinho) {
      window.abrirCarrinho(); // abre carrinho
    }
  });
}