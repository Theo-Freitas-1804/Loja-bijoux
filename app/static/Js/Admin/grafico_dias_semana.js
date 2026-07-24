const GraficoDiasSemana = (ctx , dados) =>{
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: dados.labels,
      datasets: [{
        label: "Pedidos",
        data: dados.quantidades,
        backgroundColor: "#b8860b",
        borderColor: "#8b6508",
        borderWidth: 1
      }]
    }
  });
}