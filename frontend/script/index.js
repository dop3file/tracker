function sendSearchRequest(search_value) {
    if (search_value != '') {
        return fetch('http://127.0.0.1:8000/', {
            mode: 'cors',
            method: "POST",
            body: JSON.stringify({
                "artist_name": search_value
            }),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
        }).then(resp => resp.json())
        .then(data => data);
    }
}

function display_artist_info(artist) {
    clear_artist_info()

    var name = document.createElement('H1')
    name.appendChild(document.createTextNode(artist["name"]))

    var avatar = document.createElement('img')
    avatar.src = artist["avatar_photo"]
    avatar.className = "avatar"

    var header_artist = document.createElement('img')
    header_artist.src = artist["header_photo"]
    header_artist.className = "header_artist"

    var parent = document.getElementById('artist_profile')

    parent.appendChild(avatar)
    parent.appendChild(name)
    // TODO верстка
    //parent.appendChild(header_artist)
}

function display_loader() {
    var loader = document.getElementById('loader')
    loader.className = 'loader'
}

function hide_loader() {
    var loader = document.getElementById('loader')
    loader.className = 'hide-loader'
}

function clear_artist_info() {
    document.getElementById('artist_profile').innerHTML = ""
}

function display_error(error_msg) {
    hide_loader()

    var error = document.createElement('div')
    error.className = "alert alert-danger"
    error.appendChild(document.createTextNode(error_msg))

    var parent = document.getElementById('artist_profile')

    parent.appendChild(error)
}

async function getArtist() {
    clear_artist_info()
    display_loader()
    search_value = document.getElementById('search').value
    artist = await sendSearchRequest(search_value)
    try {
        artist = JSON.parse(artist)
    } catch {}
    

    if (artist["error"] != undefined) {
        clear_artist_info()
        return display_error(artist["error"])
    }

    localStorage.setItem('artist', JSON.stringify(artist))

    hide_loader()
    display_artist_info(artist)

}

function is_local_values() {
    if (localStorage.length > 0) {
        display_artist_info(JSON.parse(localStorage.getItem('artist')))
    }
}


function hotkey_router(e) {
    if (e.enter) {
        get_artist()
    }
}

