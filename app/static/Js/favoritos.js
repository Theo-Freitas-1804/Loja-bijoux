alert("JS dos favoritos carregado");

document.addEventListener("DOMContentLoaded", function () {

  document.querySelectorAll(".btn-favorito").forEach(btn => {

    btn.addEventListener("click", async () => {

      const id = btn.dataset.id;

      const res = await fetch(`/favoritar/${id}`, {
        method: "POST"
      });

      const data = await res.json();

      // pega o ícone EXISTENTE
      const icone = btn.querySelector("i");

      // animação
      icone.classList.add("animando");

      setTimeout(() => {
        icone.classList.remove("animando");
      }, 600);

      // troca apenas a classe
      if (data.status === "adicionado") {

        icone.classList.remove("ri-heart-line");
        icone.classList.add("ri-heart-fill");

      } else {

        icone.classList.remove("ri-heart-fill");
        icone.classList.add("ri-heart-line");
      }

    });

  });

});