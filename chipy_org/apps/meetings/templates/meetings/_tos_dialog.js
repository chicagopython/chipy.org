$('#propose_submit').click(function(event){
    event.preventDefault();
    $('#tos-dialog').dialog({width: '50%', modal: true, height: 600});
    $('#agree').click(function(){
        $('#propose-topic').submit();
    });
    $('#cancel').click(function(){
        $('#tos-dialog').dialog('close');
    });
});
