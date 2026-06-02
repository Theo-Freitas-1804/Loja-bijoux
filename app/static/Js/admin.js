document.addEventListener("DOMContentLoaded", () => {
  
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
  
  const botoes = document.querySelectorAll(".btn-opcao");

botoes.forEach(botao => {

    botao.addEventListener("click", () => {

        botoes.forEach(b => {
            b.classList.remove("ativo");
        });

        botao.classList.add("ativo");

        document
            .querySelectorAll(".painel-admin")
            .forEach(p => {
                p.classList.add("escondido");
            });

        const menu = botao.dataset.menu;
        console.log(menu)
        console.log(document.querySelector(
        `#painel-${menu}`))
        
        const painelSelecionado =
            document.querySelector(
                `#painel-${menu}`
            );

        painelSelecionado.classList.remove(
            "escondido"
        );

    });

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
  
})