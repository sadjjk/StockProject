var search_url = "/stock/"
$('#stock-search').bind('keypress',function(event){
    var word = $('#stock-search').val()
    if(event.keyCode == "13" && word.length >=6  )
    {
        window.location = search_url + word;
    }
});

$('#search').click(function(){
    var word = $('#stock-search').val()
    if (word.length >=6)
    {
        window.location = search_url + word;
    }
});