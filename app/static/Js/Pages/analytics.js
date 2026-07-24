document.addEventListener("DOMContentLoaded", () => {

  const canvas = document.querySelector("#grafico");
  const ctx = canvas.getContext("2d");
  const graficos = [
    {
      funcao: GraficoDiasSemana ,
      dados: dados
    } ,
    {
      funcao: GraficoPedidosCliente,
      dados: comparativo
    } ,
    {
      funcao: GraficoPedidosHora ,
      dados: PedidosHora
    }
    
  ]
  
  let indexGrafico = 0;
  let graficoAtual = graficos[indexGrafico].funcao(ctx , graficos[indexGrafico].dados
  )
  
  const indicadores = document.querySelector(".indice");
  graficos.forEach(() => {
    const bolinha = document.createElement("div");
    bolinha.classList.add("bolinha");
    indicadores.appendChild(bolinha);
  });
  
  function atualizarIndicadores(){
    const bolinhas = document.querySelectorAll(".bolinha");
    bolinhas.forEach((bolinha, indice)=>{
        bolinha.classList.toggle(
            "ativa",
            indice === indexGrafico
        );
    });
  }
  
  const botoesGrafico = document.querySelectorAll(".toggle-grafico");
  const anterior= document.querySelector("#anterior")
  const proximo = document.querySelector("#proximo")
  
  
  function atualizarBotoes() {

    if (indexGrafico === 0) {
      anterior.disabled = true;
      anterior.classList.add("desativado");
    } else {
      anterior.disabled = false;
      anterior.classList.remove("desativado");
    }

    if (indexGrafico=== graficos.length - 1) {
      proximo.disabled = true;
      proximo.classList.add("desativado");
    } else {
      proximo.disabled = false;
      proximo.classList.remove("desativado");
    }

  }

  function trocarGrafico(direcao) {

    if (direcao === "proximo") {
      indexGrafico++;
      graficoAtual.destroy()
      graficoAtual =
      graficos[indexGrafico].funcao(
        ctx,
        graficos[indexGrafico].dados);
    } else {
      indexGrafico--;
      graficoAtual.destroy()
      graficoAtual = graficos[indexGrafico].funcao(ctx,graficos[indexGrafico].dados);
    }
    atualizarBotoes();
    atualizarIndicadores();
  }
  botoesGrafico.forEach((botao) => {

    botao.addEventListener("click", () => {

      const direcao = botao.dataset.direcao;
      trocarGrafico(direcao);

    });

  });

});