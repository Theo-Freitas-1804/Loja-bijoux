const overlay = document.querySelector(".overlay-modal")
function abrirModal({
  titulo , 
  mensagem ,
  confirmarMsg= "Confirmar",
  cancelarMsg= "Cancelar",
  onConfirmar= null
}) {
  document.querySelector("#modal-titulo").textContent = titulo;
  document.querySelector("#modal-mensagem").textContent= mensagem
  const btnconfirm = document.querySelector("#modal-confirm")
  const btncancel = document.querySelector("#modal-cancel")
  
  btnconfirm.textContent= confirmarMsg;
  btncancel.textContent= cancelarMsg;
  
  overlay.classList.remove("escondido");
  
  btnconfirm.onclick = () => {
    if (onConfirmar) {
      onConfirmar();
    }
    fecharModal();
  };
  
  btncancel.onclick = fecharModal;
}

function fecharModal() {
  
}


window.abrirModal = abrirModal;