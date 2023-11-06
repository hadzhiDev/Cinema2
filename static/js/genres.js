const content = document.querySelector('#content')

const createGenreForm = document.forms.createGenre

function getData(){
    fetch('http://127.0.0.1:8000/api/genres/')
    .then(response => response.json())
    .then(res => {
        content.innerHTML = '<ul></ul>'
        const genres = res.data
        genres.forEach((item) => {
            content.children[0].innerHTML += `<li>${item.name}</li>`
        })
    })
}

createGenreForm.addEventListener('submit', e => {
    e.preventDefault()
    const name = e.target.name.value
    fetch(
        'http://127.0.0.1:8000/api/genres/add/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name
            })
        }
    ).then((res) => {
        return res.json()
    }).then((res) => {
        console.log(res)
        getData()
    })
})