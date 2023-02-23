async function getHostApi(){
    const pathName = window.location.pathname
    const apiUrl = `/api${pathName}`
    return apiUrl
}

export default getHostApi