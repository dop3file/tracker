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
    genius = artist["genius"]
    spotify = artist["spotify_tracks"]
    
    clear_artist_info()

    console.log(artist)

    var name = document.createElement('H1')
    name.appendChild(document.createTextNode(genius["name"]))

    var avatar = document.createElement('img')
    avatar.src = genius["avatar_photo"]
    avatar.className = "avatar photo_sec"

    var header_artist = document.createElement('img')
    header_artist.src = genius["header_photo"]
    header_artist.className = "header_artist photo_sec"

    var parent_artist = document.getElementById('artist_profile')

    var parent_col_left = document.createElement('div')
    parent_col_left.id = "col_left"
    parent_artist.appendChild(parent_col_left)

    var parent_col_right = document.createElement('div')
    parent_col_right.id = "col_right"
    parent_artist.appendChild(parent_col_right)

    var spotify_tracks = document.createElement('div')
    spotify_tracks.className = "spotify_tracks"
    for (const track of spotify) {
        spotify_tracks.appendChild(get_spotify_track(track))
    }

    var alternate_names = document.createElement('p')
    alternate_names.className = 'alternate_names'
    alternate_names.appendChild(document.createTextNode('или же ' + get_pretty_alternate_names(genius["alternate_names"])))

    // parent.appendChild(header_artist)
    parent_col_left.appendChild(avatar)
    parent_col_left.appendChild(name)
    parent_col_left.appendChild(alternate_names)
    parent_col_right.appendChild(spotify_tracks)

    for (const el of get_social_elements(genius)) {
        parent_col_left.appendChild(el)
    }

}

function get_spotify_track(track) {
    var spotify_track = document.createElement('div')
    spotify_track.className = "spotify_track"

    title = document.createElement('h3')
    title.appendChild(document.createTextNode(track["title"]))

    cover = document.createElement('img')
    cover.src = track["cover_url"]

    release_date = document.createElement('p')
    release_date.appendChild(document.createTextNode(track["release_date"]))


    spotify_track.appendChild(title)
    spotify_track.appendChild(cover)
    spotify_track.appendChild(release_date)

    return spotify_track
}

function get_social_elements(artist) {
    var elements = []
    if (artist["instagram_name"] != undefined) {
        var link = document.createElement('a')
        link.href = "https://www.instagram.com/" + artist["instagram_name"]
        var image = document.createElement('img')
        image.src = 'static/instagram.png'
        image.className = 'social'
        link.appendChild(image)
        elements.push(link)
    }
    if (artist["twitter_name"] != undefined) {
        var link = document.createElement('a')
        link.href = "https://www.twitter.com/" + artist["twitter_name"]
        var image = document.createElement('img')
        image.src = 'static/twitter.png'
        image.className = 'social'
        link.appendChild(image)
        elements.push(link)
    }
    return elements
}

function get_pretty_alternate_names(alternate_names) {
    var alternate_names_string = ''
    for(i=0; i < alternate_names.length; i++) {
        alternate_names_string += alternate_names[i] + ', '
    }
    return alternate_names_string.slice(0, -2)
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

