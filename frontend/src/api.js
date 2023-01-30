import getHostApi from "./host";

async function pegaApi(apiNome = ""){
    try {
        const apiUrl = await getHostApi()
        const apiResponse = await fetch(apiUrl);
        const api = await apiResponse.json();
        return api;
    } catch (error) {
        console.error(`Error getting API ${apiNome}: ${error}`);
        return error;
    }
}

export default pegaApi;