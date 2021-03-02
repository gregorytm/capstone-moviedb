async function processForm(evt) {
    evt.preventDefault()
    // URL search params 
    search = $('#title').val()
    console.log(search)
    const resp = await axios.get("/api/movies", {params: {
        title:search
        }
    });
    console.log(resp)
    res = Object.entries(resp.data)
    console.log(res)
    showMovie(res)
}

 function showMovie(res){
    console.log(res)
    clearAll()
    $('<ul>').appendTo('body')
    for(const [key, value] of res){
        const listItem = $('<li>')
        $('<a>').attr('href', `/api/movies/${value.id}`).text(value.title).attr('id', 'details').appendTo(listItem)
        listItem.appendTo('ul')
    }
}

function clearAll(){
    $('ul').remove()
}

$("#movie-form").on("submit", processForm);
