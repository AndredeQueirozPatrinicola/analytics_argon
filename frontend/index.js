import { Chart } from "chart.js/auto";

async function pegaApi(apiNome = ""){
    try {
        const apiResponse = await fetch("http://127.0.0.1:8000/api/graduacao");
        const api = await apiResponse.json();
        return api;
    } catch (error) {
        console.error(`Error getting API ${apiNome}: ${error}`);
        return error;
    }
}

async function dataSetsApi(){
    const api = await pegaApi()
    const labels = ['Amarela', 'Branca', 'Indígena', 'Não informada', 'Parda']
    const colors = ['#052e70', '#1a448a', '#425e8f', '#7585a1', '#91a8cf']

    let datasets = []
    for(let i=0;i < labels.length; i++){
        let data = []
        for(let j = 0; j < api.length; j++){
            let label = labels[i]
            data.push(api[j].dados[label])
        }
        datasets.push(
            {
                label : labels[i],
                data : data,
                backgroundColor: colors[i],
                borderWidth: 1
            }
        )
    }    
    return datasets
}

async function plotaGrafico(){
    const labels = ["2017", "2018", "2019","2020","2021","2022", "2023"];
    const datasets = await dataSetsApi()
    const data = {
      labels: labels,
      datasets: datasets
    };
    const config = {
        type: 'bar',
        data: data,
        plugins: {
            title: {
              display: true,
              text: 'Chart.js Bar Chart - Stacked'
            },
          },
          responsive: true,
          scales: {
            x: {
              stacked: true,
            },
            y: {
              stacked: true
            }
        }
    };
    const grafico = document.getElementById('teste')
    return new Chart(grafico, config)
}


plotaGrafico()