document.addEventListener("DOMContentLoaded", () => {

  const copiar = document.querySelector("#copiar")

  if (!copiar) return

  copiar.addEventListener("click", async () => {

    const codigo = copiar.dataset.codigo

    await navigator.clipboard.writeText(codigo)

    mostrarToast("Código copiado!")

  })

})