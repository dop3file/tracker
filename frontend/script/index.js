audio = new Audio();
isPlay = false
let track_id = null

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
    spotify_artist = artist["spotify"]
    words = artist["most_popular_words"]
    
    clear_artist_info()

    console.log(artist)

    var name = document.createElement('H1')
    name.appendChild(document.createTextNode(spotify_artist["name"]))

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
    spotify_tracks.className = "card_ purple"
    for (const track of spotify) {
        spotify_tracks.appendChild(get_spotify_track(track))
    }

    var most_popular_words = document.createElement('div')
    most_popular_words.className = "card_ green"
    title = document.createElement('h1')
    title.appendChild(document.createTextNode("Топ используемых слов:"))
    most_popular_words.appendChild(title)
    for (const word of words) {
        word_ = document.createElement('h3')
        word_.className = "word_artist"
        word_.appendChild(document.createTextNode(word))
        most_popular_words.appendChild(word_)
    } 

    var alternate_names = document.createElement('p')
    alternate_names.className = 'alternate_names'
    if (get_pretty_alternate_names(genius["alternate_names"])) {
        alternate_names.appendChild(document.createTextNode('или же ' + get_pretty_alternate_names(genius["alternate_names"])))
    }

    genres = document.createElement('div')
    genres.id = 'genres'
    for (const el of spotify_artist["genres"]) {
        genre = document.createElement('span')
        genre.className = "genre"
        genre.appendChild(document.createTextNode(el))
        genres.appendChild(genre)
    }

    followers = document.createElement('div')
    followers.id = "followers"
    foll_text = document.createElement('span')
    foll_text.appendChild( document.createTextNode(spotify_artist["followers_count"].toLocaleString() + " followers") )
    followers.appendChild( foll_text )

    popularity = document.createElement('div')
    popularity.id = "popularity"
    popularity_text = "Popularity " + spotify_artist["popularity"].toString() + "/100"
    popularity_txt = document.createElement('span')
    popularity_txt.appendChild(document.createTextNode(popularity_text))
    popularity.appendChild(popularity_txt)

    // parent.appendChild(header_artist)
    parent_col_left.appendChild(avatar)
    parent_col_left.appendChild(name)
    parent_col_left.appendChild(alternate_names)
    parent_col_right.appendChild(spotify_tracks)
    parent_artist.appendChild(most_popular_words)
    
    
    for (const el of get_social_elements(genius)) {
        parent_col_left.appendChild(el)
    }
    parent_col_left.appendChild(genres)
    parent_col_left.appendChild(popularity)
    parent_col_left.appendChild(followers)
    


}

function highlight_track(on) {
    if (track_id != null) {
        if (on) {
            document.getElementById(track_id).style.border = "7px solid pink";
        }
        else {document.getElementById(track_id).style.border = null;}
    }
}

function convert_ms_to_sec(ms) {
    return ms / 1000 / 60
}

function get_spotify_track(track) {
    cover = document.createElement('img')
    cover.src = track["cover_url"]
    cover.id = "track_" + track["id"]
    cover.className = "cover_artist"

    var spotify_track = document.createElement('div')
    spotify_track.className = "spotify_track"

    spotify_track.onclick = function() {
        if (isPlay) {
            audio.pause();
            isPlay = false;
            highlight_track(false);
        }
        else {
            audio = new Audio(track["preview_url"]);
            audio.play();
            isPlay = true;
            track_id = "track_" + track["id"];
            highlight_track(true);
        }
     };

    var track_left = document.createElement('div')
    track_left.className = "track_left"
    var track_details = document.createElement('div')

    title = document.createElement('h3')
    title.appendChild(document.createTextNode(track["title"]))

    release_date = document.createElement('p')
    release_date.appendChild(document.createTextNode(track["release_date"]))

    track_details.appendChild(title)
    track_details.appendChild(release_date)

    track_left.appendChild(cover)

    var track_info = document.createElement('div')
    track_info.className = "track_info"
    lst = ['Танцевальность: ', 'Энергия: ', 'Громкость: ', 'Темп: ', 'Длительность: ']
    idx = 0
    for (const detail in track["details"]) {
        p = document.createElement('span')
        if (idx == 4) {
            detail_ = convert_ms_to_sec(track["details"][detail]).toString().slice(0, 4) + "m"
        }
        else if (idx == 2) {
            detail_ = track["details"][detail] + " db"
        }
        else {
            detail_ = track["details"][detail]
        }
        
        p.appendChild(document.createTextNode(lst[idx] + " " + detail_))
        track_info.appendChild(p)
        idx++
    }

    spotify_track.append(track_left)
    spotify_track.append(track_details)
    spotify_track.append(track_info)

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

    artist_profile = document.getElementById('artist_profile')
    artist_profile.id = "artist_profile_hidden"
}

function hide_loader() {
    var loader = document.getElementById('loader')
    loader.className = 'hide-loader'

    try {
        artist_profile = document.getElementById('artist_profile_hidden')
        artist_profile.id = "artist_profile"
    } catch{;}
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
    cat_off()
    try {
        artist_profile = document.getElementById('artist_profile_hidden')
        artist_profile.id = "artist_profile"
    } catch{;}
    clear_artist_info()
    display_loader()
    search_value = document.getElementById('search').value
    if (search_value == "") {
        location.reload()
    }
    artist = await sendSearchRequest(search_value)
    try {
        artist = JSON.parse(artist)
    } catch {}
    console.log(artist)
    if (artist["error"] != undefined) {
        hide_loader()
        clear_artist_info()
        return display_error(artist["error"])
    }

    localStorage.setItem('artist', JSON.stringify(artist))

    hide_loader()
    display_artist_info(artist)
}

function cat_off() {
    cat = document.getElementById('cat_')
    cat.style.display = "none";
}

function is_local_values() {

    if (localStorage.length > 0) {
        try {
            artist_profile = document.getElementById('artist_profile_hidden')
            artist_profile.id = "artist_profile"
        } catch{;}
        cat_off()
        display_artist_info(JSON.parse(localStorage.getItem('artist')))
    }
}

function hotkey_router(e) {
    if (e.enter) {
        get_artist()
    }
}

