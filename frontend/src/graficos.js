import { Chart } from "chart.js/auto";
import pegaApi from './api';

async function plotaGrafico(element){
  const grafico = await pegaApi()
  return new Chart(element, grafico)
}

export default plotaGrafico