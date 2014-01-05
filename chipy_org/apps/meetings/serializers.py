from rest_framework import serializers

from .models import Meeting, Topic, Presentor


class PresentorSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField('get_email')

    def get_email(self, obj):
        request = self.context.get('request')

        if request and request.user.is_staff:
            return obj.email
        else:
            return ''

    class Meta:
        model = Presentor
        fields = ('id', 'name', 'release', 'email')


class TopicSerializer(serializers.ModelSerializer):
    presentors = PresentorSerializer()

    class Meta:
        model = Topic
        fields = (
            'id',
            'title',
            'presentors',
            'length',
            'description',
            'embed_video',
            'slides_link',
            'start_time',
            'approved',
            'license'
        )
        depth = 1


class MeetingSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)

    class Meta:
        model = Meeting
        fields = ('id', 'when', 'where', 'live_stream', 'topics')
        depth = 2
