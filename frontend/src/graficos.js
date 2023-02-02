import { Chart } from "chart.js/auto";
import pegaApi from './api';

async function plotaGrafico(element){
  const grafico = await pegaApi()
  return new Chart(element, grafico)
}

async function coordenaGraficos(){
  const graficos = Array.from(document.getElementsByTagName('canvas'))
  graficos.forEach(tag => {
      plotaGrafico(tag)
  });
}

export default coordenaGraficos

