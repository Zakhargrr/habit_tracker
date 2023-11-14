from rest_framework import serializers

from main.models import Habit
from main.validators import ConHabitAndRewardValidator, DurationValidator, ConnectedHabitValidator, \
    PleasantHabitValidator, PeriodValidator


class CreateHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['place', 'hours', 'minutes', 'action', 'is_pleasant_habit', 'connected_habit', 'period', 'reward',
                  'duration']
        validators = [
            ConHabitAndRewardValidator(connected_habit='connected_habit', reward='reward'),
            DurationValidator(duration='duration'),
            ConnectedHabitValidator(connected_habit='connected_habit'),
            PleasantHabitValidator(is_pleasant_habit='is_pleasant_habit', connected_habit='connected_habit',
                                   reward='reward'),
            PeriodValidator(period='period')
        ]


class ViewHabitSerializer(serializers.ModelSerializer):
    connected_habit = serializers.SerializerMethodField()

    def get_connected_habit(self, instance):
        if instance.connected_habit:
            return str(instance.connected_habit)
        else:
            return None

    class Meta:
        model = Habit
        fields = ['id', 'user', 'place', 'time', 'action', 'is_pleasant_habit', 'connected_habit', 'period', 'reward',
                  'duration']
