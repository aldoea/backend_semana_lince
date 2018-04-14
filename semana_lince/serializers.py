from rest_framework import serializers
from semana_lince import models


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Responsable
        fields = '__all__'


class ActivityCategory(serializers.ModelSerializer):
    class Meta:
        model = models.ActivityCategory
        fields = '__all__'


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Speaker
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = '__all__'


class EventDetailedSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True, read_only=True)

    class Meta:
        model = models.Event
        exclude = ('activity',)
        depth = 1


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'


class ActivityDetailedSerializer(ActivitySerializer):
    event_set = EventDetailedSerializer(many=True, read_only=True)

    class Meta:
        model = models.Activity
        fields = '__all__'
        depth = 1


class AssistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assistance
        fields = '__all__'
