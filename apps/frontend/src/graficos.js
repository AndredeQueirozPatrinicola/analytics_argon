import { Chart } from "chart.js/auto";
import pegaApi from './api';
import ChartjsPluginStacked100 from "chartjs-plugin-stacked100";

Chart.register(ChartjsPluginStacked100);

const DEFAULT_PARAMS = {
  ano_inicial: 2017,
  ano_final: 2022,
  departamento: ""
}

async function formataParametros(parameters) {
  console.log(parameters)
  if (parameters.length === 4) {
    return {
      "ano_inicial": parameters[0],
      "ano_final": parameters[1],
      "departamento": parameters[2],
      "stacked": parameters[3]
    }
  }
  else if (parameters.length === 3) {
    return {
      "ano": parameters[0],
      "departamento": parameters[1],
      "stacked" : parameters[2]
    }
  }
  else if(parameters.length === 2){
    return {
      "departamento": parameters[0]
    }
  }
}

async function raiseDataError(ctx) {
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
  const labels = Array.from(parent.children).filter(element => element.tagName == 'SELECT').map(element => element.value);
  const checkBox = Array.from(parent.children).filter(element => element.tagName == 'INPUT').map(element => element.checked)
  if (checkBox) {
    labels.push(checkBox[0])
  }
  const parametros = await formataParametros(labels);
  if (parametros.ano_inicial > parametros.ano_final) {
    raiseDataError(message)
  }
  else {
    plotaGrafico(chart, parametros)
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



