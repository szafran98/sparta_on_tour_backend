from rest_framework import serializers
from .models import Event, Participant


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'normalized_event_date',
                  'normalized_join_date', 'image_link']


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'
