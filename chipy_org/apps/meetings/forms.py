from django.forms import ModelForm
from durationfield.forms import DurationField as FDurationField
from meetings.models import Topic

class TopicForm(ModelForm):
    length = FDurationField()
    
    required = ('title',
                'meeting',
                'description',
    )
    
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
            instance.presentor = request.user
        instance.save()