from rest_framework import serializers

from .models import Meeting, Topic, Presentor


class PresenterSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

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
    presenters = PresenterSerializer(many=True, source='presentors')
    reviewer = serializers.SerializerMethodField()

    def get_reviewer(self, obj):
        request = self.context.get('request')

        if request and request.user.is_staff:
            return obj.email
        else:
            return ''

    class Meta:
        model = Topic
        fields = (
            'id',
            'title',
            'presenters',
            'reviewer',
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
