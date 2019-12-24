$('.rsvp').click(function(){

    {% comment %}
    {% if request.user.is_authenticated %}
    $.ajax({
        type: 'POST',
        url: "{% url 'rsvp' %}",
        data: {
            response:$(this).data('response'),
            csrfmiddlewaretoken: '{{ csrf_token }}',
            meeting: '{{ curr_meeting.id }}'
        },
        success: function(data){
            location.reload();
        },
    });
    {% else %}
    {% endif %}
    {% endcomment %}

    $.ajax({
        type: 'GET',
        url: "{% url 'anonymous_rsvp' %}",
        data: {
            response:$(this).data('response'),
            csrfmiddlewaretoken: '{{ csrf_token }}',
            meeting: '{{ curr_meeting.id }}'
        },
        success: function(data){
            $('#form-contents').html(data['html']);
            $('#anonymous-rsvp-dialog').dialog({width: '500'});
            $('#anonymous-rsvp-form input[name=response]').val($(this).data('response'))
        },
        error: function(xhr, status, e){
            alert(status);
        }
    });
    
    return false;
    
});
$('#anonymous-rsvp-form1').submit(function(event){
    event.preventDefault();
    $.ajax({
        type: 'POST',
        url: "{% url 'anonymous_rsvp' %}",
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
