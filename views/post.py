from rest_framework import viewsets, permissions

from groups.models import Post
from groups.permissions.edit import HasPostingRights
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
