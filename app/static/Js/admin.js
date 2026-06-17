console.count("admin.js carregado");
document.addEventListener("DOMContentLoaded", () => {
// 1 - Controla as seções da página //  
  const btnMais = document.getElementById("btn-mais");
  const painelMais = document.getElementById("painel-mais");
  
  btnMais.addEventListener("click", () => {

  painelMais.classList.toggle("escondido");
});
    
  const btnMarketing = document.getElementById("btn-marketing");
  const submenuMarketing = document.getElementById("submenu-marketing");

  btnMarketing.addEventListener("click", () => {
    submenuMarketing.classList.toggle("escondido");
  });
    
  const filtros = document.querySelectorAll(".filtro-periodo button")
  const custom = document.querySelector("#custom")
  const datas = document.querySelector(".datas-person")
  
  filtros.forEach(filtro => {
    filtro.addEventListener("click" , () => {
      filtros.forEach(f => {
        f.classList.remove("ativo")
      })
      filtro.classList.add("ativo")
      const dias = filtro.dataset.dias;
      if (dias) {
        window.location.href =`${window.location.pathname}?dias=${dias}`;
      }
    })
  })
  custom.addEventListener("click", () => {
    console.log("clivou em mim")
    datas.classList.toggle("escondido")
    console.log(datas.className)
  })
  
  const mais = document.querySelectorAll(".mais")
  const recentes = document.querySelector(".clientes-recentes")
  mais.forEach(i =>{
    i.addEventListener("click" , () => {
      console.log("clique")
      i.classList.toggle("ri-arrow-down-s-line")
      i.classList.toggle("ri-arrow-up-s-line")
      recentes.classList.toggle("escondido")
    })
  })
  
  const infos = document.querySelectorAll(".info")

infos.forEach(info => {

    const popup =
        info.parentElement.querySelector(
            ".tooltip-metrica"
        )

    info.addEventListener("click", () => {

        popup.classList.toggle("escondido")

    })

})
// Fecha o DOM 
})