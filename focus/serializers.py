from rest_framework import serializers

from .models import PomodoroSession, DurationCategory


class DurationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DurationCategory
        fields = ('id', 'type', 'minutes')


class PomodoroSessionSerializer(serializers.ModelSerializer):
    category = DurationCategorySerializer()
    class Meta:
        model = PomodoroSession
        fields = ('id', 'start_time', 'duration', 'category', 'completed')


class PomodoroCreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = ('id', 'category')


class PomodoroSessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PomodoroSession
        fields = ('id', 'duration')
