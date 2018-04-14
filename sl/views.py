from rest_framework import serializers
from rest_framework_jwt.compat import Serializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.compat import get_username_field
from django.contrib.auth import get_user_model

from rest_framework_jwt.settings import api_settings

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class InsecureJSONSerializer(Serializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

    def create(self, validated_data):
        super().create(validated_data)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        pk_field = attrs.get(self.username_field)
        try:
            user = User.objects.get(pk=pk_field)
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuario no existe')
        if not user.is_active:
            msg = _('User account is disabled.')
            raise serializers.ValidationError(msg)
        payload = jwt_payload_handler(user)

        return {
            'token': jwt_encode_handler(payload),
            'user': user
        }


class InsecureObtainJSONWebToken(ObtainJSONWebToken):
    serializer_class = InsecureJSONSerializer


obtain_jwt_token = InsecureObtainJSONWebToken.as_view()