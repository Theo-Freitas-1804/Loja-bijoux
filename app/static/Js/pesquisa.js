document.addEventListener("DOMContentLoaded", function () {
  // =========================
  // FILTRO (PAINEL)
  // =========================
  const btn = document.querySelector(".btn-filtro");
  const painel = document.getElementById("painel-filtros");
  const overlay = document.getElementById("overlay");

  if (btn && painel && overlay) {
    btn.addEventListener("click", () => {
      painel.classList.remove("escondido");
      overlay.classList.remove("escondido");
    });

    overlay.addEventListener("click", () => {
      painel.classList.add("escondido");
      overlay.classList.add("escondido");
    });

    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") {
        painel.classList.add("escondido");
        overlay.classList.add("escondido");
      }
    });
  }

  // =========================
  // BUSCA DINÂMICA
  // =========================
  const input = document.getElementById("busca-input");

  if (!input) return; // evita erro em páginas sem busca

  const container = document.getElementById("resultado-busca");

  // =========================
  // RENDER DOS RESULTADOS
  // =========================
  function mostrarResultados(lista) {
    container.innerHTML = "";

    if (!lista.length) {
      container.innerHTML = "<p>Nenhum resultado</p>";
      return;
    }

    lista.forEach(produto => {
      container.innerHTML += `
        <div class="item-busca">
          <img src="${produto.imagem || ''}" width="40">
          <a href="/produto/${produto.id}">
            ${produto.nome}
          </a>
        </div>
      `;
    });
  }

  // =========================
  // DEBOUNCE + FETCH
  // =========================
  let timeout;

  input.addEventListener("input", function () {

    clearTimeout(timeout);

    const digitou = input.value.trim();

    // limpa se vazio
    if (!digitou) {
      container.innerHTML = "";
      return;
    }

    timeout = setTimeout(() => {

      fetch(`/api/pesquisa?item=${digitou}`)
        .then(res => {
          if (!res.ok) throw new Error("Erro na requisição");
          return res.json();
        })
        .then(data => {
          console.log("RESULTADO:", data);
          mostrarResultados(data);
        })
        .catch(err => {
          console.error("Erro:", err);
          container.innerHTML = "<p>Erro ao buscar</p>";
        });

    }, 300);
  });

});