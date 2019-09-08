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