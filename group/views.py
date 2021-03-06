from rest_framework import viewsets,status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from auth.permissions import GroupPermission,GroupFilterPermission
from .models import GroupList
from .serializers import GroupSerializer

from auth.settings import SECRET_KEY, SUPERUSER
import jwt
from auth.tasks import save_activity

import logging
log = logging.getLogger(__name__)


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (GroupPermission,)
    queryset = GroupList.objects.all()
    serializer_class = GroupSerializer
    @list_route(url_path='')
    def get(self, request):
        # permission_classes = (SearchGroupPermission,)

        group_id = ''
        app_id = ''
        # account_status= ''
        try:
            group_id=request.query_params.get('group_id')
        except ValueError:
            group_id=''
        try:
            app_id=request.query_params.get('app_id')
        except ValueError:
            app_id=''

        if group_id != '' and app_id != '':
            queryset = GroupList.objects.filter(groupID__icontains=request.query_params.get('group_id', None),appID=request.query_params.get('app_id', None))
        elif group_id == '' and app_id != '':
            queryset = GroupList.objects.filter(appID=request.query_params.get('app_id', None))
        elif group_id != '' and app_id == '':
            queryset = GroupList.objects.filter(groupID__icontains=request.query_params.get('group_id', None))
        else:
            queryset = GroupList.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (GroupFilterPermission,)
    queryset = GroupList.objects.all()
    serializer_class = GroupSerializer

    @list_route(url_path='(?P<app_id>[0-9]+)')
    def service(self, request, pk=None, app_id=None):
        try:
            queryset = GroupList.objects.filter(appID=app_id)
            serializer = GroupSerializer(queryset, many=True)

            return Response(serializer.data)

        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
