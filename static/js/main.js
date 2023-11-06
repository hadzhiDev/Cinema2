let genres = document.getElementById('genres')
let genres_card = document.querySelector('.genres_card')

if (genres_card){
    genres_card.addEventListener('mouseover', e =>{
        genres.classList.remove('hidden')
    })
}

if (genres_card){
    genres_card.addEventListener('mouseout', e => {
        genres.classList.add('hidden')
    })
}

const createCommentVar = document.forms.createComment
if (createCommentVar) {
createCommentVar.addEventListener('submit', e => {
    e.preventDefault();
    const form = e.target
    const movieId = +document.getElementById('movie_id').textContent
    const body = new FormData(form)
    body.append('movie', movieId)
    const btn = document.querySelector('#addCommentBtn')
    // btn.innerHTML = '<img src="https://i.gifer.com/ZKZg.gif" width="15px">'
    fetch(
        '/ajax/create_comment/',
        {
            method: 'POST',
            headers:{
                'Accept': 'application/json'
            },
            body
        }
    )
    .then(res => res.json())
    .then(res => {
        const commentContainer = document.querySelector('#commentContainer')
        commentContainer.innerHTML = `
                <div class="p-2 mt-3 rounded-xl text-slate-800 bg-white" id="comment_block_${res.id}">
                    <div class="flex justify-between">
                        <div class="">${res.name}</div>
                        <div class="text-muted text-end">${res.date}</div>
                    </div>
                    <p class="">${res.text}</p>
                    <div class="text-end">
                        <button class="bg-amber-400 rounded-xl text-black addCommentBtn" onclick="deleteComment(${res.id})">Delete</button>
                    </div>
                </div>
        ` + commentContainer.innerHTML
    })
    .finally(res => btn.innerHTML = 'Add this comment')
})
}

const deleteComment = async (commentId) => {

  const res = await fetch(`/workspace/ajax/comments/${commentId}/delete/`)
  if (res.status == 200) {
    const data = await res.json()
    if (data.isDeleted){
      const commentBlock = document.querySelector(`#comment_block_${commentId}`)
      commentBlock.remove()
    }
  } else  alert('Network error or unauthorized')
  
}





