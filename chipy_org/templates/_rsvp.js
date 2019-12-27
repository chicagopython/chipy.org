$('.rsvp').click(function(){
    $.ajax({
        type: 'GET',
        url: "{% url 'rsvp' %}",
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            meeting: '{{ curr_meeting.id }}'
        },
        success: function(data){
            $('#rsvp-form-fields').html(data['html']);
            if(data['is_anonymous']){
                grecaptcha.render(
                    'rsvp-captcha',
                    {'sitekey': data['sitekey']}
                );
            }
            $('#rsvp-dialog').dialog({width: '500'});
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
