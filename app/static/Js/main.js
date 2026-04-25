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
    
}); // Fecha o DOMContentLoaded da linha 3

