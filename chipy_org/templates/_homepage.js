$('#where-link').click(function() {
    $('#where-dialog').dialog({ width: 182, modal: true });
    return false;
});

$('.rsvp').click(function(){
    {% if request.user.is_authenticated %}
    $.ajax({
        type: 'POST',
        url: '{% url rsvp %}',
        data: {response:$(this).data('response'), csrfmiddlewaretoken: '{{ csrf_token }}', meeting: '{{ next_meeting.id }}'},
        success: function(data){
            location.reload();
        },
    });
    {% else %}
    $('#anonymous-rsvp-dialog').dialog({width: '500'});
    $('#anonymous-rsvp-form input[name=response]').val($(this).data('response'))
    return false;
    {% endif %}
});
$('#anonymous-rsvp-form1').submit(function(event){
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: '{% url anonymous_rsvp %}',
        data: $('#anonymous-rsvp-form').serialize(),
        success: function (data, textStatus) {
            alert(data, textStatus);
            $('#anonymous-rsvp-dialog').html(data);
        },
        error: function(xhr, status, e) {
            alert(status, e);
        }
    });
});
//$('#live-stream-link').click(function() {
//    $('#live-stream-dialog').dialog({ width: 800, modal: true });
//    return false;
//});

