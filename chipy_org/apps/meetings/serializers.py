from rest_framework import serializers

from .models import Meeting, Topic, Presentor


class PresentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentor
        fields = ('name', 'release')


class TopicSerializer(serializers.ModelSerializer):
    presentor = PresentorSerializer()

    class Meta:
        model = Topic
        fields = (
            'title',
            'presentor',
            'length',
            'description',
            'embed_video',
            'slides_link',
            'start_time',
            'approved'
        )
        depth = 1


class MeetingSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)

    class Meta:
        model = Meeting
        fields = ('when', 'where', 'live_stream', 'topics')
        depth = 2
