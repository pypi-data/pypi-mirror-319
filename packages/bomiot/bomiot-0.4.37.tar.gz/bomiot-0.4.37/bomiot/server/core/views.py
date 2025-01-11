from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .serializers import UserSerializer
from .filter import UserFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
        retrieve:
            Response a data list（get）

        list:
            Response a data list（all）

        create:
            Create a data line（post）

        delete:
            Delete a data line（delete)
    """
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "created_time", "updated_time", ]
    filter_class = UserFilter

    def get_project(self):
        try:
            data_id = self.kwargs.get('pk')
            return data_id
        except:
            return None

    def get_queryset(self):
        data_id = self.get_project()
        if self.request.user:
            if data_id is None:
                return User.objects.filter(openid=self.request.auth.openid, is_delete=False)
            else:
                return User.objects.filter(openid=self.request.auth.openid, id=data_id, is_delete=False)
        else:
            return User.objects.none()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy']:
            return UserSerializer
        else:
            return self.http_method_not_allowed(request=self.request)

    def create(self, request, *args, **kwargs):
        data = self.request.data
        data['openid'] = self.request.auth.openid
        return Response({"detail": "Bin size does not exists or it has been changed"})


    def destroy(self, request, **kwargs):
        qs = self.get_object()
        if qs.openid != self.request.auth.openid:
            raise APIException({"detail": "Cannot delete data which not yours"})
        else:
            qs.is_delete = True
            qs.save()
            serializer = self.get_serializer(qs, many=False)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)