console.log("Javascript: Online!");

document.addEventListener("DOMContentLoaded", function () {

  // =========================
  // BOTÃO VER MAIS
  // =========================
  const conteudoOculto =
    document.getElementById("conteudo-oculto");

  const btnVerMais =
    document.getElementById("btn-ver-mais");

  if (btnVerMais && conteudoOculto) {

    btnVerMais.addEventListener("click", function () {

      conteudoOculto.classList.toggle("ativo");

      if (conteudoOculto.classList.contains("ativo")) {
        btnVerMais.textContent = "Ver Menos ▲";
      } else {
        btnVerMais.textContent = "Ver Mais ▼";
      }

    });

  }

  // =========================
  // MENU MOBILE
  // =========================
  
  const nav =
  document.getElementById("nav-menu");
  const btnMenu =
  document.querySelector(".menu-btn");
  if (btnMenu && nav) {

  // abrir/fechar menu
  btnMenu.addEventListener("click", (e) => {
    e.stopPropagation();
    console.log("clique")
    nav.classList.toggle("escondido");
    nav.classList.toggle("ativo");

  });

  // clique fora
  document.addEventListener("click", (e) => {

    const clicouDentroMenu =
      nav.contains(e.target);

    const clicouNoBotao =
      btnMenu.contains(e.target);

    if (!clicouDentroMenu && !clicouNoBotao) {

      nav.classList.remove("ativo");

    }

  });

}
  
  // =========================
  // ANIMAÇÃO DOS CARDS
  // =========================
  const elementos =
    document.querySelectorAll(".card-produto");

  if (elementos.length > 0) {

    const observer =
      new IntersectionObserver((entries) => {

        entries.forEach((entry) => {

          if (entry.isIntersecting) {
            entry.target.classList.add("ativo");
          }

        });

      });

    elementos.forEach((el) => observer.observe(el));

  }

  // =========================
  // BANNER ROTATIVO
  // =========================
  const banners =
    document.querySelectorAll(".banner");

  console.log("Banners:", banners.length);

  if (banners.length > 1) {

    let index = 0;

    setInterval(() => {

      // remove atual
      banners[index].classList.remove("ativo");

      // próximo
      index = (index + 1) % banners.length;

      // ativa próximo
      banners[index].classList.add("ativo");

    }, 4000);

  }
  
  // =========================
  // VALIDAÇÃO DA PESQUISA
  // =========================
  const formBusca = document.querySelector(".barra-pesquisa");

  if (formBusca) {
    const inputBusca = formBusca.querySelector("input");

    formBusca.addEventListener("submit", (e) => {
      if (!inputBusca.value.trim()) {
        e.preventDefault();
        mostrarToast("Digite algo para pesquisar.");
      }
    });
  }

  
});