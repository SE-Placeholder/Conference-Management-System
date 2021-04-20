from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, ListField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from conference.models import Conference
from role.models import Role, RoleTypes


class ConferenceSerializer(ModelSerializer):
    steering_committee = SerializerMethodField()

    class Meta:
        model = Conference
        fields = [
            'id',
            'title',
            'description',
            'deadline',
            'location',
            'date',
            'fee',
            'steering_committee'
        ]

    def get_steering_committee(self, conference):
        return map(lambda role: role.user.username,
                   Role.objects.filter(role=RoleTypes.STEERING_COMMITTEE, conference=conference))

#
# class WriteConferenceSerializer(ModelSerializer):
#     steering_committee = ListField(required=False)
#
#     class Meta:
#         model = Conference
#         fields = [
#             'id',
#             'title',
#             'description',
#             'deadline',
#             'location',
#             'date',
#             'fee',
#             'steering_committee'
#         ]
#
#     def create(self, validated_data):
#         conference = super().create(validated_data)
#         Role.objects.create(
#             role=RoleTypes.STEERING_COMMITTEE,
#             conference=conference,
#             user=self.context['request'].user)
#         return conference
#
#     def update(self, instance, validated_data):
#         conference = super().update(instance, validated_data)
#         for user in validated_data.get('steering_committee', []):
#             print('user:', user)
#         return conference
