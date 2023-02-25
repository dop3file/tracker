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
    document.getElementById('main').innerHTML = ""
    var name = document.createElement('H1')
    name.appendChild(document.createTextNode(artist["name"]))
    var avatar = document.createElement('img')
    avatar.src = artist["avatar_photo"]
    avatar.className = "avatar"

    var parent = document.getElementById('main')

    parent.appendChild(avatar)
    parent.appendChild(name)
    
}


async function getArtist() {
    search_value = document.getElementById('search').value
    artist = await sendSearchRequest(search_value)
    artist = JSON.parse(artist)
    
    localStorage.setItem('artist', JSON.stringify(artist))

    display_artist_info(artist)

}

function is_local_values() {
    if (localStorage.length > 0) {
        display_artist_info(JSON.parse(localStorage.getItem('artist')))
    }
}

