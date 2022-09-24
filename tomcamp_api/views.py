from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from tomcamp_api.authentication import ExpiringTokenAuthentication


class UserObtainTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response_data = {
                'token': token.key,
                'user': {'username': user.username, 'full_name': user.get_full_name(), 'email': user.email},
            }

        if not created:
            auth = ExpiringTokenAuthentication()
            try:
                auth.authenticate_credentials(token.key)
            except AuthenticationFailed:
                new_token = Token.objects.create(user=user)
                response_data["token"] = new_token.key

            return Response(response_data)

        return Response(response_data)
