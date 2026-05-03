console.log("Javascript: Online!");

document.addEventListener('DOMContentLoaded', function() {
    // --- LÓGICA 1: BOTÃO VER MAIS ---
    const conteudo_oculto = document.getElementById('conteudo-oculto');
    const btnvermais = document.getElementById('btn-ver-mais');
    if (btnvermais && conteudo_oculto) {
        btnvermais.addEventListener('click', function() {
            conteudo_oculto.classList.toggle('ativo');
            if (conteudo_oculto.classList.contains('ativo')) {
                btnvermais.textContent = 'Ver Menos ▲';
            } else {
                btnvermais.textContent = 'Ver Mais ▼';
            }
        });
    }
    
    const nav = document.getElementById("nav-menu");
    const btn = document.getElementById("btn-menu");
    if (btn && nav) {
      btn.addEventListener("click", () => {
        nav.classList.toggle("ativo");
    });
    }
    
    const elementos = document.querySelectorAll(".card-produto");
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("ativo");
    }
  });
});
elementos.forEach((el) => observer.observe(el));

// --- LÓGICA 3: BANNER ROTATIVO ---
const banners = document.querySelectorAll(".banner");

console.log("banners:", banners.length);

if (banners.length > 1) {
  let index = 0;

  setInterval(() => {
    // remove ativo atual
    banners[index].classList.remove("ativo");

    // próximo índice
    index = (index + 1) % banners.length;

    // ativa próximo
    banners[index].classList.add("ativo");

  }, 4000); // troca a cada 4s
}

// Lógica 4 - Erro na pesquisa //

const formBusca = document.querySelector(".barra-pesquisa")
const inputBusca = formBusca.querySelector("input");
const erro = document.querySelector(".erro-busca");

formBusca.addEventListener("submit", (e) => {
  if (!inputBusca.value.trim()) {
    e.preventDefault();

    erro.classList.remove("escondido");

    setTimeout(() => {
      erro.classList.add("escondido");
    }, 2000);

  } else {
    erro.classList.add("escondido");
  }
});

}); // Fecha o DOMContentLoaded da linha 3

