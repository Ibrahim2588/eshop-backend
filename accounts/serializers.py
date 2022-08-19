from dj_rest_auth.registration.serializers import RegisterSerializer as BaseRegistrerSerializer
from dj_rest_auth.serializers import LoginSerializer as BaseLoginSerialiser
from dj_rest_auth.serializers import UserDetailsSerializer as BaseUserDetailsSerializer

from rest_framework import serializers

from django.contrib.auth import get_user_model
UserModel = get_user_model()

class RegisterSerializer(BaseRegistrerSerializer):

    username = serializers.CharField(max_length=200, required=False)

    def save(self, request):
        return super().save(request)


class LoginSerializer(BaseLoginSerialiser):
    username = None


class UserDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = [
            'email',
            'first_name',
            'last_name',
            'image',
        ]