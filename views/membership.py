from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied

from formula_one.enums.active_status import ActiveStatus
from groups.models import Membership, Group
from groups.permissions.admin import HasAdminRights, has_admin_rights
from groups.serializers.membership import MembershipSerializer


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
        queryset = queryset.order_by('-start_date', 'person__full_name')

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

        return super().create(request, *args, **kwargs)
