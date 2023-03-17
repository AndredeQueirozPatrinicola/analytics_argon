async function dropdown(element) {
    if (Array.from(element.classList).includes("dropdown-is-toggled")) {
        element.classList.remove("dropdown-is-toggled")
    }
    else {
        element.classList.add("dropdown-is-toggled")
    }
}

async function addDropdownListener() {
    const element = document.getElementById("dropdown")
    if (element) {
        const elementChildren = Array.from(element.children)
        elementChildren[0].addEventListener('click', function () {
            dropdown(elementChildren[1])
        })
    }
}

export default addDropdownListener;

