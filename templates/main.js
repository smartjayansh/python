function bookSearch(){
    var search = document.getElementById('search').nodeValue
    var tit = document.getElementById('title')

    document.getElementById('results').innerHTML = ""
    //console.log(search)
    console.log(tit.value)


    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=intitle:" + tit.value + "&key=AIzaSyAaVB1rnJ5Yi5o4MBb4gMAzv6pHi6scTfA",
        datatype: "json",
        success: function(data){
            console.log(data);  
             for(i=0; i<data.items.length; i++){
                 if(data.items[i].volumeInfo.title != undefined){
                 results.innerHTML +="<h2>" + data.items[i].volumeInfo.title + "</h2>"                
                 results.innerHTML += "<img src=\"" + data.items[i].volumeInfo.imageLinks.thumbnail + "\"width=\"100px\">"

                 }
             }
        },
        type: 'GET'
    });
}
document.getElementById('button').addEventListener('click',bookSearch,false)