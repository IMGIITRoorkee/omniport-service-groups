from rest_framework import viewsets, permissions, generics, mixins

from groups.models import Group
from groups.permissions.edit import HasEditRights
from groups.serializers.group import (
    GroupListSerializer,
    GroupDetailSerializer,
)


class GroupViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    Viewset for RU operations on Group objects
    """

    permission_classes = [
        permissions.IsAuthenticated,
        HasEditRights,
    ]

    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupDetailSerializer

    lookup_field = 'slug'
    pagination_class = None

    def get_serializer_class(self):
        """
        Return the appropriate serializer class for the current action
        :return: the appropriate serializer class for the current action
        """

        action_serializer_map = {
            'list': GroupListSerializer,
        }
        if self.action in action_serializer_map:
            return action_serializer_map[self.action]

        return super().get_serializer_class()
