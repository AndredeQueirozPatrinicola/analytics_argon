import plotaGrafico from './src/graficos';

async function coordenaGraficos(){
    const graficos = Array.from(document.getElementsByTagName('canvas'))
    graficos.forEach(tag => {
        plotaGrafico(tag)
    });
}

coordenaGraficos()