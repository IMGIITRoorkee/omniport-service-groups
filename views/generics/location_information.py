from rest_framework import viewsets, permissions, mixins

from formula_one.models import LocationInformation
from groups.models import Membership, Group
from groups.serializers.generics.location_information import (
    GroupLocationInformationSerializer
)


class LocationInformationViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    """
    View for CRU operations on LocationInformation objects
    """

    serializer_class = GroupLocationInformationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        """
        Return the queryset of LocationInformation objects a user can see
        :return: the queryset of LocationInformation objects
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
        location_information = LocationInformation.objects.filter(
            group__in=groups
        ).order_by(
            'datetime_created'
        )
        return location_information
