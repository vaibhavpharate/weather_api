# api/auth.py
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token 
from rest_framework.response import Response

class CustomAuthToken(ObtainAuthToken):
    def get(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        # print(request.headers)
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token,created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.username,
            'email':user.email
        })

