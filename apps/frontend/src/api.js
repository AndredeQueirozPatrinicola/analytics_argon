async function getHostApi(){
    const pathName = window.location.pathname
    const apiUrl = `/api${pathName}`
    return apiUrl
}
async function pegaApi(element, parameters){
    try {
        let apiUrl = `/api/${element.id}?ano_inicial=${parameters.ano_inicial}&ano_final=${parameters.ano_final}&departamento=${parameters.departamento}&stacked=${parameters.stacked}`
        let response = await fetch(apiUrl);
        let data = await response.json(apiUrl);
        return data
    } catch (error) {
        console.error(`Error getting API ${element.id}: ${error}`);
        element.parentElement.innerHTML = "Não foi possivel renderizar o grafico, recarregue a pagina e tente novamente ou contate o administrador";
        return {}
    }
}

export default pegaApi;