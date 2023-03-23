import { Chart } from "chart.js/auto";
import pegaApi from './api';
import ChartjsPluginStacked100 from "chartjs-plugin-stacked100";

Chart.register(ChartjsPluginStacked100);

const DEFAULT_PARAMS = {
  ano_inicial: 2017,
  ano_final: 2023,
  departamento: ""
}

async function raiseDataError(ctx){
  ctx.classList.add('active-message')
}

async function plotaGrafico(element, parameters) {
  let chart = Chart.getChart(element.id)
  if (!chart) {
    const config = await pegaApi(element, DEFAULT_PARAMS)
    new Chart(element, config)
  }
  else {
    chart.destroy()
    const config = await pegaApi(element, parameters)
    new Chart(element, config)
  }
}

async function submitPost(element) {
  const message = element.parentElement.parentElement.firstElementChild;
  message.classList.remove('active-message')
  const parent = element.parentElement;
  const chart = Array.from(parent.parentElement.children).filter(element => element.className == 'grafico-container')[0].firstElementChild;
  const parameters = Array.from(parent.children).filter(element => element.tagName == 'SELECT').map(element => element.value);
  const ano_inicial = parameters[0]
  const ano_final = parameters[1]
  const departamento = parameters[2]

  if (ano_inicial > ano_final) {
    raiseDataError(message)
  }
  else {
    plotaGrafico(chart, {ano_inicial:ano_inicial, ano_final:ano_final, departamento:departamento})
  }

}

export async function coordenaGraficos() {
  const graficos = Array.from(document.getElementsByTagName('canvas'))
  graficos.forEach(tag => {
    plotaGrafico(tag)
  });
  const selectButtons = Array.from(document.getElementsByTagName('btn'))
  selectButtons.forEach(tag => {
    tag.addEventListener('click', () => {
      submitPost(tag);
    });
  })
}



