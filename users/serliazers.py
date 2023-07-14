from rest_framework import serializers

from education.serliazers import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(many=True, read_only=True, source='user')

    class Meta:
        model = User
        fields = '__all__'
