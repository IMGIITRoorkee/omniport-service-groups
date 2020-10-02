from rest_framework import status
from rest_framework import response
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from formula_one.enums.active_status import ActiveStatus

from groups.models import Membership, Group
from groups.permissions.admin import HasAdminRights, has_admin_rights
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
        
        queryset = queryset.order_by(
            '-person__student__current_year',
            '-person__student__current_semester',
            'person__full_name',
        )
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Check if user has permission to create the new membership and defer to
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
            if not has_admin_rights(person, group):
                raise PermissionDenied
        except Group.DoesNotExist:
            pass
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        send_membership_notification(group.name, 'add', request.data['person'])
        return response.Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        """
        Check if user has permission to delete the new membership and defer to
        the base implementation of the method
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: deleted instance
        """

        person = request.person
        member = kwargs.get('pk')
        try:
            member = Membership.objects.get(pk=member)
            if not has_admin_rights(person, member.group):
                raise PermissionDenied
        except Membership.DoesNotExist:
            pass
        instance = self.get_object()
        self.perform_destroy(instance)
        send_membership_notification(
            member.group.name,
            'remove',
            member.person.id
        )
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        """
        Check if user has permission to edit the new membership and defer to
        the base implementation of the method
        :param request: the request being processed
        :param args: arguments
        :param kwargs: keyword arguments
        :return: response
        """

        person = request.person
        member = kwargs.get('pk')
        try:
            member = Membership.objects.get(pk=member)
            if not has_admin_rights(person, member.group):
                raise PermissionDenied
        except Membership.DoesNotExist:
            pass
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
            member.group.name,
            'edit',
            member.person.id
        )
        return response.Response(serializer.data)
