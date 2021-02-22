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

// async function processForm(evt) {
//     evt.preventDefault()
//     // URL search params 
//     const params = {};
//     params.title = $('#title').val()
//     console.log(title)
//     const resp = await axios.get("/api/movies", params);
//     console.log(resp)
//     res = Object.entries(resp.data)
//     console.log(res)
//     showMovie(res)
// }

 function showMovie(res){
    console.log(res)
    $('<ul>').appendTo('body')
    for(const [key, value] of res){
        const listItem = $('<li>')
        $('<a>').attr('href', `/api/movies/search/${value.id}`).text(value.title).appendTo(listItem)
        listItem.appendTo('ul')
    }
}

$("#movie-form").on("submit", processForm);