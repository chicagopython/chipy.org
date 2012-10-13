from django.forms import ModelForm
from meetings.models import Topic, Presentor

class TopicForm(ModelForm):
    required = ('title',
                'meeting',
                'description',
    )

    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['meeting'].required = True
        self.fields['description'].required = True

    
    class Meta:
        model = Topic
        fields = ('title',
                   'meeting',
                   'length',
                   'description',
                   'slides_link',
               )

    def save(self, commit=True, request=None):
        instance = super(TopicForm, self).save(commit)
        if request and not instance.presentor:
            instance.presentor = Presentor.objects.get_or_create(
                user = request.user,
                name = request.user.get_full_name(),
                email = request.user.email,
                release = True,
            )

        if commit:
            instance.save()
        return instance