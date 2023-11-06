const content = document.getElementById('content')


const deleteMovie = () => {
    for(item of content.children){
        item.children[6].addEventListener('click', e => {
            e.preventDefault()
            let movieId = +e.target.parentElement.getAttribute('data')
            fetch(`http://127.0.0.1:8000/api/movies/${movieId}/delete/`, 
                {
                    method: 'DELETE',
                    
                }
            )
            .then(res => res.json())
            .then(res => {
                console.log(res);
            })
            // if (res.status == ) {
            //     if (data.isDeleted){
            //         // const commentBlock = document.querySelector(`#comment_block_${commentId}`)
            //         e.target.parentElement.remove()
            //     }
            // } else  alert('Network error or unauthorized')
        
        })
    }
}

const getGenres = () => {
    const genreSelect = document.getElementById('genreSelect')
    fetch('http://127.0.0.1:8000/api/genres/')
    .then(res => res.json())
    .then(res => {
        const genres = res.data
        genres.forEach(genre => {
            genreSelect.innerHTML += `
            <div class="">
                <input type="checkbox" name="genres" id="${genre.id}" value="${genre.id}">
                <label for="genres_${genre.id}">${genre.name}</label>
            </div>
            `
        })
    })
}

const getDirectors = () => {
    const directorSelect = document.getElementById('directorSelect')
    fetch('http://127.0.0.1:8000/api/directors/')
    .then(res => res.json())
    .then(res => {
        const directors = res.data
        directors.forEach(director => {
            const option = document.createElement('option');
            option.setAttribute('value', director.id)
            option.innerText = director.full_name
            directorSelect.appendChild(option)
        })
    })
}

const getUsers = () => {
    const userSelect = document.getElementById('userSelect')
    fetch('http://127.0.0.1:8000/api/users/')
    .then(res => res.json())
    .then(res => {
        const users = res.data
        users.forEach(user => {
            const option = document.createElement('option');
            option.setAttribute('value', user.id)
            option.innerText = user.username
            userSelect.appendChild(option)
        })
    })
}


const runProject = () => {
    content.innerHTML = '<div class="text-center"><img width="30px" src="https://i.gifer.com/ZKZg.gif"></div>'
    fetch('http://127.0.0.1:8000/api/movies/')
    .then(res => res.json())
    .then(res => {
        const data = res.data
        content.innerHTML = ''
        data.forEach(item => {
            const date = new Date(item.created_at)
            content.innerHTML += `
                <div data="${item.id}" class="col-lg-3 col-md-4 col-sm-6 col-12">
                    <img src="${item.image}" class="card-img-top" alt="${item.name}">
                    <h5 class="card-title">${item.name}</h5>
                    <h5 class="card-title">rating: ${item.rating}</h5>
                    <h5 class="card-title">year: ${item.year}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">created date: ${date.toLocaleDateString()}</h6>
                    <p class="card-text">${item.overview}</p>
                    <button>delete</button>
                </div>
            `
        })
        deleteMovie()
    })
}

const addMovie = (e) => {
    e.preventDefault();
    const body = new FormData(e.target)
    const token = prompt()
   
    fetch(
        'http://127.0.0.1:8000/api/movies/add/',
        {
            // headers:{
            //     'Authorization': `Token ${token}`
            // },
            method: 'POST',
            body, 
        }
    ).then(res => res.json())
    .then(res => runProject())
    .catch(err => console.log(err))
}

document.forms.addMovie.onsubmit = addMovie


// function updateMovie() {
    
// }

getGenres()
getDirectors()
getUsers()

