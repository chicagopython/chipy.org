$('#propose_submit').click(function(event){
    event.preventDefault();
    $('#tos-dialog').dialog({width: '500px'});
    $('#agree').click(function(){
        $('#propose-topic').submit();
    });
    $('#cancel').click(function(){
        $('#tos-dialog').dialog('close');
    });
});
