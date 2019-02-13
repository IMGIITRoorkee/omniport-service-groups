from rest_framework import viewsets, permissions, mixins
from rest_framework.exceptions import PermissionDenied

from groups.models import Membership, Group
from groups.permissions.edit import has_edit_rights
from groups.serializers.generics.social_link import (
    GroupSocialLinkSerializer,
)
from kernel.models import SocialLink


class SocialLinkViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    View for CRUD operations on SocialLink objects
    """

    serializer_class = GroupSocialLinkSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Return the queryset of SocialLink objects a user can see
        :return: the queryset of SocialLink objects
        """

        person = self.request.person
        memberships = Membership.objects.filter(
            person=person
        ).filter(
            has_edit_rights=True
        )
        groups = Group.objects.filter(
            membership__in=memberships
        )
        social_links = SocialLink.objects.filter(
            socialinformation__group__in=groups
        ).order_by(
            'datetime_created'
        )
        return social_links

    def create(self, request, *args, **kwargs):
        """
        Check if user has permission to create the new social link and defer to
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
