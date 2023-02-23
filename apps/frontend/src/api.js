import getHostApi from "./host";

async function pegaApi(element, apiNome = ""){
    try {
        let apiUrl = await getHostApi();   
        apiUrl = apiUrl + element.id 
        if(apiNome != "geral"){
          apiUrl = apiUrl + '/' + apiNome;  
        }
        const apiResponse = await fetch(apiUrl);
        const api = await apiResponse.json();
        return api;
    } catch (error) {
        console.error(`Error getting API ${apiNome}: ${error}`);
        element.parentElement.innerHTML = "Não foi possivel renderizar o grafico, recarregue a pagina e tente novamente ou contate o administrador";
        return {}
    }
}

export default pegaApi;