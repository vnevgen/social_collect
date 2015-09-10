__author__ = 'vitaly'

from rest_framework import serializers

from .models import Person, PersonAccount

class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonAccount
        fields = ('person', 'type', 'screen_name', 'social_id', 'name', 'image', )


class AccountCreateSerializer(serializers.Serializer):

    link = serializers.URLField()