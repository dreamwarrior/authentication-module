import jwt
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import list_route
from rest_framework.response import Response
from auth.permissions import HasToken, ACLPermission, ACLDetailsPermission
from auth.settings import SECRET_KEY, SUPERUSER
from auth_jwt.models import Auth
from user_group.models import UserGroup
from acl.models import ACL
from services.models import ServiceList
from services.serializers import ServiceSerializer
from .serializers import GetACLSerializer, ACLSerializer, GetGroupSerializer, GetServiceSerializer

from auth.tasks import save_activity

import logging
log = logging.getLogger(__name__)


class GetACLViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (ACLDetailsPermission,)
    queryset = ACL.objects.all()
    serializer_class = GetACLSerializer

    @list_route(url_path='service/(?P<service_id>[0-9]+)')
    def service(self, request, pk=None, service_id=None):
        # permission_classes = (ACLDetailsByServicePermission,)

        try:

            queryset = ACL.objects.filter(service=service_id)
            serializer = GetGroupSerializer(queryset, many=True)
            return Response(serializer.data)
        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @list_route(url_path='group/(?P<group_id>[0-9]+)')
    def group(self, request, pk=None, group_id=None):
        # permission_classes = (ACLDetailsByGroupPermission,)

        try:

            queryset = ACL.objects.filter(group=group_id)
            serializer = GetServiceSerializer(queryset, many=True)
            return Response(serializer.data)

        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ACLViewSet(viewsets.ModelViewSet):
    permission_classes = (ACLPermission,)
    queryset = ACL.objects.all()
    serializer_class = ACLSerializer


class PermissionsList(APIView):
    permission_classes = (HasToken,)

    def get(self, request, format=None):
        try:
            token = request.META['HTTP_TOKEN']
            payload = jwt.decode(token, SECRET_KEY)

            try:
                if payload['loginID'] not in SUPERUSER:
                    user = Auth.objects.get(loginID=payload['loginID'], appID=payload['appID'], is_active=True)
                    groups = UserGroup.objects.filter(user=user.id).values_list('group', flat=True)
                    services = ACL.objects.filter(group__in=groups).values_list('service', flat=True)
                    services = list(set(services))
                    details = ServiceList.objects.filter(pk__in=services)
                else:
                    details = ServiceList.objects.all()

                serializer = ServiceSerializer(details, many=True)

                async_result = save_activity.delay(payload['loginID'], payload['appID'], 'AUTH_GET_PERMISSION_LIST', payload)
                # return_value = async_result.get()
                # print(return_value)

                return Response(serializer.data)
            except Auth.DoesNotExist:
                return Response(status=status.HTTP_412_PRECONDITION_FAILED)

        except jwt.ExpiredSignatureError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
