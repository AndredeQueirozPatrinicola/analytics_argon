import { Chart } from "chart.js/auto";
import pegaApi from './api';

async function plotaGrafico(element){
  console.log('ola')
  const grafico = await pegaApi()
  console.log('fim')
  return new Chart(element, grafico)
}

export default plotaGrafico