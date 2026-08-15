from rest_framework import status
from rest_framework import response
from rest_framework import viewsets, permissions

from formula_one.enums.active_status import ActiveStatus

from groups.models import Membership
from groups.permissions.admin import HasAdminRights
from groups.serializers.membership import MembershipSerializer
from groups.utils.membership_notifications import send_membership_notification


class MembershipViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operations on Membership objects
    """

    permission_classes = [
        permissions.IsAuthenticated,
        HasAdminRights,
    ]

    serializer_class = MembershipSerializer

    filter_fields = ['group__slug', ]

    def get_queryset(self):
        """
        Return the queryset of memberships that a person is allowed to see
        :return: the queryset of memberships that a person is allowed to see
        """

        is_active = self.request.query_params.get('is_active', None)
        if is_active == 'true':
            queryset = Membership.objects_filter(ActiveStatus.IS_ACTIVE)
        elif is_active == 'false':
            queryset = Membership.objects_filter(ActiveStatus.IS_INACTIVE)
        else:
            queryset = Membership.objects.all()

        queryset = queryset.select_related(
            'group',
        ).order_by(
            'person__student__enrolment_number',
        )
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create the new membership and notify the person it was created for
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: the newly created instance
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        membership = serializer.instance
        send_membership_notification(
            membership.group.name,
            'add',
            membership.person_id
        )
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete the membership and notify the person it belonged to
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: deleted instance
        """

        instance = self.get_object()
        group_name = instance.group.name
        person_id = instance.person_id
        self.perform_destroy(instance)
        send_membership_notification(group_name, 'remove', person_id)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """
        Update the membership and notify the person it belongs to
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: response
        """

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        send_membership_notification(
            instance.group.name,
            'edit',
            instance.person_id
        )
        return response.Response(serializer.data)
