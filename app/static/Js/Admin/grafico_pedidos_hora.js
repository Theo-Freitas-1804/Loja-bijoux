const GraficoPedidosHora = (ctx, dados) => {
  return new Chart(ctx, {
    type: "bar",
    data: {
      labels: dados.labels,
      datasets: [{
        label: "Pedidos por hora",
        data: dados.quantidades,
        backgroundColor: "yellow",
        borderColor: "orange",
        borderWidth: 1
      }]
    }
  });
};