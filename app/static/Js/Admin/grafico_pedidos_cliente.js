const GraficoPedidosCliente = (ctx, dados) => {

  const labels = dados.dados.map(item => item.cliente);
  const pedidos = dados.dados.map(item => item.pedidos);
  const ticketMedio = dados.dados.map(item => item.ticket_medio);

  return new Chart(ctx, {
    type: "bar",

    data: {
      labels,
      datasets: [
        {
          label: "Pedidos",
          data: pedidos,
          backgroundColor: "#30fc03",
          borderColor: "blue",
          borderWidth: 1,

          yAxisID: "y"
        },
        {
          label: "Ticket Médio",
          data: ticketMedio,
          backgroundColor: "red",
          borderColor: "black",
          borderWidth: 1,

          yAxisID: "y1"
        }
      ]
    },

    options: {
      responsive: true,

      scales: {

        y: {
          type: "linear",
          position: "left",

          title: {
            display: true,
            text: "Pedidos"
          },

          beginAtZero: true
        },

        y1: {
          type: "linear",
          position: "right",

          title: {
            display: true,
            text: "Ticket Médio (R$)"
          },

          beginAtZero: true,

          grid: {
            drawOnChartArea: false
          }
        }

      }
    }

  });

}