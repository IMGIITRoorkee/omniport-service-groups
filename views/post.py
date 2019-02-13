from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from groups.models import Post, Group
from groups.permissions.edit import HasPostingRights, has_edit_rights
from groups.serializers.post import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on Post objects
    """

    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasPostingRights,
    ]
    queryset = Post.objects.all().order_by('-datetime_created')
    filter_fields = ['group__slug', ]

    def create(self, request, *args, **kwargs):
        """
        Check if user has permission to create the new post and defer to
        the base implementation of the method
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the newly created instance
        """

        person = request.person
        group = request.data.get('group')
        try:
            group = Group.objects.get(pk=group)
            if not has_edit_rights(person, group):
                raise PermissionDenied
        except Group.DoesNotExist:
            pass

        return super().create(request, *args, **kwargs)
