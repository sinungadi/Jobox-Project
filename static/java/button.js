const input = document.getElementById("fileUpload")
const text = document.getElementById("text")
const btn = document.getElementById("upload")

input.addEventListener("change", () => {
    const path = input.value.split('\\')
    const filename = path[path.length -1]

    text.innerText = filename ? filename : "Choose file"

    if(filename)
        btn.classList.add("chosen")
    else
        btn.classList.remove("chosen")
})