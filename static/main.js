function bookSearch(){
    var search = document.getElementById('search')
    var title = document.getElementById('title')

    document.getElementById('results').innerHTML = ""
    //console.log(search)
    console.log(title.value)
    var bookid
    //event.preventDefault();

    $.ajax({
        url: "https://www.googleapis.com/books/v1/volumes?q=intitle:" + title.value + "&key=AIzaSyAaVB1rnJ5Yi5o4MBb4gMAzv6pHi6scTfA",
        datatype: "json",
        success: function(data){
            console.log(data);  
             for(i=0; i<data.items.length; i++){
                 if(data.items[i].volumeInfo.title != undefined){
                 results.innerHTML +="<h2>" + data.items[i].volumeInfo.title + "</h2>"                
                 results.innerHTML += "<img src=\"" + data.items[i].volumeInfo.imageLinks.thumbnail + "\"width=\"100px\">"
                // for(j=0;j<data.items[i].volumeInfo.authors.length;j++){
                     results.innerHTML +="<h3>" + data.items[i].volumeInfo.authors + "</h3>"                
                 //}                 
                 results.innerHTML +="<h2>" + data.items[i].volumeInfo.publisher + "</h2>"  
                 results.innerHTML +="<h2>" + data.items[i].volumeInfo.pagecount + "</h2>"
                 results.innerHTML +="<h2>" + data.items[i].volumeInfo.averageRating + "</h2>"                
                 bookid = data.items[i].id   
                             
                 results.innerHTML +="<form action=\"{{ url_for('addbook') }}\" method=\"post\"> \
                 <button type=\"submit\" >Click Me</button></form>"

                }
             }
        },
        type: 'GET'
    });
}


function addbookuser(){
    var temp = document.getElementById('idforbook')
    console.log("hello")
    
}
document.getElementById('button').addEventListener('click',bookSearch,false)
// document.getElementById('idforbook').addEventListener('click',addbookuser,false)

// author publisher,ratings, pages