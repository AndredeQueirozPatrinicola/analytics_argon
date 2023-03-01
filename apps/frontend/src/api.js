async function getHostApi(){
    const pathName = window.location.pathname
    const apiUrl = `/api${pathName}`
    return apiUrl
}
async function pegaApi(element, apiNome = ""){
    try {
        let apiUrl = await getHostApi();   
        console.log(apiUrl)
        apiUrl = apiUrl + element.id 
        if(apiNome != "geral"){
          apiUrl = apiUrl + '/' + apiNome;  
        }
        console.log(apiUrl)
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