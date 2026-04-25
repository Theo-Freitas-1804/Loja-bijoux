document.addEventListener("DOMContentLoaded", function () {

  const form = document.querySelector(".form-add");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const codigo = form.querySelector("input").value;

    fetch("/meus-cupons/novo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ codigo: codigo })
    })
    .then(res => res.json())
    .then(data => {
      const box = document.querySelector("#info-cupom");
      const texto = document.querySelector("#texto-cupom");

      texto.textContent = data.mensagem;
      box.style.display = "block";

      const btnok = document.querySelector("#confirmacao");

      if (btnok) {
        btnok.addEventListener("click", () => {
          box.style.display = "none";
        });
      }
    });

  });

});