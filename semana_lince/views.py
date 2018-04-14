from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from semana_lince import models, serializers


# Create your views here.
class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = models.Activity.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ActivityDetailedSerializer
        return serializers.ActivitySerializer
