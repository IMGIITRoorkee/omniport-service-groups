from rest_framework import viewsets, permissions, mixins

from formula_one.models import ContactInformation
from groups.models import Membership, Group
from groups.serializers.generics.contact_information import (
    GroupContactInformationSerializer,
)


class ContactInformationViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    View for RU operations on ContactInformation objects
    """

    serializer_class = GroupContactInformationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Return the queryset of ContactInformation objects a user can see
        :return: the queryset of ContactInformation objects
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
        contact_information = ContactInformation.objects.filter(
            group__in=groups
        ).order_by(
            'datetime_created'
        )
        return contact_information
