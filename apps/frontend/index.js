import { coordenaGraficos } from './src/graficos';
import animaSearchBar from './src/searchbar';
import datatables from './src/datatables';
import addDropdownListener from './src/dropdown';

async function main(){
    addDropdownListener();
    coordenaGraficos();
    animaSearchBar();
    datatables();
}

main()