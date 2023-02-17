function send_search_request() {
    search_value = document.getElementById('search').value
    if (search_value != '') {
        fetch('http://127.0.0.1:8000/', {
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
        .then(data => {console.log(data);});
    }
}