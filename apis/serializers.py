from rest_framework import serializers, viewsets
from .models import VDbApi
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly



class VBADataSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = VDbApi
        fields = "__all__"

class VBAViewSets(viewsets.ModelViewSet):
    queryset = VDbApi.objects.all()[0:10]
    serializer_class = VBADataSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]