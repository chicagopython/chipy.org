$('.rsvp').click(function(){
    $('#rsvp-dialog').dialog({width: '500'});
    return false;
});
$('#anonymous-rsvp-form1').submit(function(event){
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: "{% url 'rsvp' %}",
        data: $('#rsvp-form').serialize(),
        success: function (data, textStatus) {
            alert(data, textStatus);
            $('#rsvp-dialog').html(data);
        },
        error: function(xhr, status, e) {
            alert(status, e);
        }
    });
});
