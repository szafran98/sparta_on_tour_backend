from rest_framework import serializers
from .models import Event, Participant


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date',
                  'can_be_joined_to', 'image_link']


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
