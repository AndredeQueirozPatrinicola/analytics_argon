import { Chart } from "chart.js/auto";
import pegaApi from './api';
import ChartjsPluginStacked100 from "chartjs-plugin-stacked100";

Chart.register(ChartjsPluginStacked100);

async function plotaGraficoDefault(element){
  const grafico = await pegaApi(element, "geral")
  return new Chart(element, grafico)
}

async function plotaGrafico(element, option){
  let chart = Chart.getChart(element.id)
  if(!chart){
    new Chart(element, config)
  }
  else{
    chart.destroy()
    const config = await pegaApi(element, option)
    new Chart(element, config)
  }
}

async function addChartListener(element){
  const selectElement = document.querySelector(`.${element.id}`);
  selectElement.addEventListener('change', function() {
    const selectedValue = selectElement.value;
    plotaGrafico(element, selectedValue.toLowerCase())    
  }); 
}

async function coordenaGraficos(){
  const graficos = Array.from(document.getElementsByTagName('canvas'))
  graficos.forEach(tag => {
      plotaGraficoDefault(tag)
      addChartListener(tag)
  });
}

export default coordenaGraficos

