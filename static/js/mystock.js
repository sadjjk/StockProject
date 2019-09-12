$('#add-stock').bind('keypress',function(event){
        var word = $('#add-stock').val()
        if (event.keyCode == "13" &&  word.length >=6){
            if (confirm("确认添加" + word + "到自选股？")) {
                $.post("/index",{add_code:word},function(response) {
                    document.write(response);
                })
            }
        }
});


$('.delete-stock').click(function () {
    var delete_code = $(this).prev().attr('href').split("/")[2]
    var delete_name = $(this).prev().children(':first').text()
    if (confirm("将在自选股中删除" + delete_name + "？")) {
               $.post("/index",{delete_code:delete_code},function(response) {
                    document.write(response);
                })
            }
})

