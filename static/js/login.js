const loginForm = document.querySelector('#login_form')

if (loginForm){
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault()
        const form = e.target
        const body = new FormData(form)
        const res = await fetch('/ajax/login/', {
            method: 'POST',
            body,
        })

        if (res.status == 200 || res.status === 400){
            const data = await res.json()
            if (data.isAuthenticated){
                window.location.reload()
            } else {
                const messageBlock = document.querySelector('#login_form_message')
                messageBlock.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i>' + data.message
            }
        } 
        // else if (res.status > 400){
        //     const data = await res.json()
        //     const errorBlock = document.querySelector('#login_form_error')
        //     errorBlock.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i>' + data.error
        // }
        else alert('Network error')
    })
}

function loginToggle() {
    document.querySelector('#loginModalWin').classList.toggle('active')
    document.querySelector('#frame2').classList.toggle('active')
    document.querySelector('#login_card').classList.toggle('active')
}

const selects = document.querySelectorAll('.select');
if (selects) {
  selects[0].addEventListener('click', () => {
    selects.forEach(select => {
      const button = select.querySelector('button');
      const full_height = [];
      [...select.querySelectorAll('div > a')].map(link => {
        const styles = window.getComputedStyle(link);
        const box = link.getBoundingClientRect();
        const margin = parseFloat(styles.marginTop) + parseFloat(styles.marginBottom) || 0;
        const height = box.height + margin;
        full_height.push(height);
        link.addEventListener('click', () => {
          const link_text = link.textContent;
          const button_text = button.textContent;
          button.textContent = link_text;
          button.style.animationName="popOut";
          button.addEventListener("animationend", () => {
            button.style.animationName="none"
          });
          const span = document.createElement('span');
          span.textContent = button_text;
          link.innerHTML = "";
          link.appendChild(span)
          link.blur()
        })
      });
      const totalHeight = full_height.reduce((accumulator, currentValue) => accumulator + currentValue, 0);
      select.dataset.totalHeight = totalHeight;
      select.style.setProperty('--max-height', totalHeight);  
    });
  });
}
  
  