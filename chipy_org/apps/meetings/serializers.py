from rest_framework import serializers

from .models import Meeting, Presenter, Topic


class PresenterSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        request = self.context.get("request")

        if request and request.user.is_staff:
            return obj.email
        else:
            return ""

    class Meta:
        model = Presenter
        fields = ("id", "name", "release", "email")


class TopicSerializer(serializers.ModelSerializer):
    presenters = PresenterSerializer(many=True)

    class Meta:
        model = Topic
        fields = (
            "id",
            "title",
            "presenters",
            "length",
            "description",
            "embed_video",
            "slides_link",
            "start_time",
            "approved",
            "license",
            "reviewers",
        )
        depth = 1


class MeetingSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)

    class Meta:
        model = Meeting
        fields = ("id", "when", "where", "live_stream", "topics")
        depth = 2
