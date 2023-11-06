const logout = async () => {

    const res = await fetch('/ajax/logout/')

    if (res.status == 200){
        const data = await res.json()
        if (data.isLogout){
            window.location.reload()
            return true
        }
    }
    alert('Network error')
}