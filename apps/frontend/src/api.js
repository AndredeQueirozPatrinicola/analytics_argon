function objectToQueryString(obj) {
  let result = "";
  for (let key in obj) {
    if (obj.hasOwnProperty(key)) {
      result += key + "=" + obj[key] + "&";
    }
  }
  return result.slice(0, -1);
}

async function pegaApi(element, parameters) {

  try {
    let apiUrl = `/api/${element.id}?` + objectToQueryString(parameters)
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