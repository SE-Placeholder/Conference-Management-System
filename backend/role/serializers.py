from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

# from role.models import Role

# class RoleSerializer(ModelSerializer):
#     role = SerializerMethodField()
#     conference = ConferenceSerializer()
#     paper = PaperSerializer()
#
#     class Meta:
#         model = Role
#         fields = ['role', 'user', 'conference', 'paper']
#
#     def get_role(self, instance):
#         return instance.get_role_display()
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         items = []
#         for key, value in data.items():
#             if value is None:
#                 items.append(key)
#         for item in items:
#             data.pop(item)
#         return data
#
#


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
