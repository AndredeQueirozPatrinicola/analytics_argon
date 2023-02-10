import getHostApi from "./host";

async function pegaApi(element, apiNome = ""){
    try {
        let apiUrl = await getHostApi();   
        apiUrl = apiUrl + element.id  
        if(apiNome != "todos"){
          apiUrl = apiUrl + '/' + apiNome;  
        }
        const apiResponse = await fetch(apiUrl);
        const api = await apiResponse.json();
        return api;
    } catch (error) {
        console.error(`Error getting API ${apiNome}: ${error}`);
        return error;
    }
}

export default pegaApi;