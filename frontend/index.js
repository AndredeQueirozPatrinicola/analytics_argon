import plotaGrafico from './src/graficos';
import animaSearchBar from './src/searchbar';

async function coordenaGraficos(){
    const graficos = Array.from(document.getElementsByTagName('canvas'))
    graficos.forEach(tag => {
        plotaGrafico(tag)
    });
}


coordenaGraficos()
animaSearchBar()