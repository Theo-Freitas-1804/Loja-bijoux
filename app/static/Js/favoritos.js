alert("JS dos favoritos carregado");
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".btn-favorito").forEach(btn => {
    
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      const res = await fetch(`/favoritar/${id}`, {
        method: "POST"
      });
      const data = await res.json();
      if (data.status === "adicionado") {
        btn.classList.add("ativo");
        btn.innerHTML = '<i class="ri-heart-fill"></i>';
      } else {
        btn.classList.remove("ativo");
        btn.innerHTML = '<i class="ri-heart-line"></i>';
      }
    });
    
  });
});