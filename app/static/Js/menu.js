document.addEventListener("DOMContentLoaded", () => {

  const btn = document.getElementById("btn-perfil");
  const menu = document.getElementById("menu-dropdown");
  const busca = document.querySelector(".barra-pesquisa");
  const fotoInterna = document.querySelector("#menu-dropdown .foto-perfil");

  console.log("busca:", busca);
  console.log("fotoInterna:", fotoInterna);

  // 👉 ABRIR
  if (btn) {
    btn.addEventListener("click", () => {
      console.log("clicou");

      menu.classList.remove("escondido");
      btn.classList.add("escondido");

      if (busca) busca.classList.add("escondido");
    });
  }

  // 👉 FECHAR
  if (fotoInterna) {
    fotoInterna.addEventListener("click", () => {
      menu.classList.add("escondido");
      btn.classList.remove("escondido");

      if (busca) busca.classList.remove("escondido");
    });
  }

});