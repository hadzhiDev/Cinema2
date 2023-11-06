const content = document.querySelector('#content')

const addDirForm = document.forms.addDirector

function getData(){
    fetch('http://127.0.0.1:8000/api/directors/')
    .then(response => response.json())
    .then(res => {
        content.innerHTML = '<ul></ul>'
        const directors = res.data 
        directors.forEach((item) => {
            content.children[0].innerHTML += `<li>${item.full_name}</li>`
        })
    })
}

addDirForm.addEventListener('submit', e => {
    e.preventDefault()
    const full_name = e.target.full_name.value
    fetch(
        'http://127.0.0.1:8000/api/directors/add/',
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                full_name
            })
        }
    ).then((res) => {
        return res.json()
    }).then((res) => {
        console.log(res)
        getData()
    })
})