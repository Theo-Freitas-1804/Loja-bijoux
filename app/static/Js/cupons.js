document.addEventListener("DOMContentLoaded", function () {

  const form = document.querySelector(".form-add");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);

    fetch("/meus-cupons/resgatar", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {

      abrirModal({
        titulo: data.sucesso
          ? "Cupom Resgatado"
          : "Erro",

        mensagem: data.mensagem,

        confirmarMsg: "OK",
        cancelarMsg: "",

        onConfirmar: () => {
          if (data.sucesso) {
            location.reload();
          }
        }
      });

    });

  });

  document.querySelectorAll(".validade").forEach(el => {

    const dataExpira = el.dataset.expira;

    if (!dataExpira) return;

    function atualizar() {

      const agora = new Date();
      const expira = new Date(dataExpira);

      const diff = expira - agora;

      if (diff <= 0) {
        el.textContent = "Expirado";
        return;
      }

      const dias = Math.floor(
        diff / (1000 * 60 * 60 * 24)
      );

      const horas = Math.floor(
        (diff % (1000 * 60 * 60 * 24))
        / (1000 * 60 * 60)
      );

      const minutos = Math.floor(
        (diff % (1000 * 60 * 60))
        / (1000 * 60)
      );
      
      if (dias > 0) {
        el.textContent =`Expira em ${dias} dia${dias > 1 ? "s" : ""} e ${horas} hora${horas > 1 ? "s" : ""}`;
      } else if (horas > 0) {
        el.textContent =`Expira em ${horas} hora${horas > 1 ? "s" : ""} e ${minutos} minuto${minutos > 1 ? "s" : ""}`;
        
      } else {
        el.textContent =
        `Expira em ${minutos} minuto${minutos > 1 ? "s" : ""}`;
        
      }
      
    }

    atualizar();

    setInterval(
      atualizar,
      60000
    );

  });

});