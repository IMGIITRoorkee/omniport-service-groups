from rest_framework import permissions

from groups.models import Membership


def has_admin_rights(person, group):
    """
    Check if the person has rights to make administrative changes to the group
    :param person: the person whose rights are being checked
    :param group: the group whose member the person must be
    :return: True if the person has admin rights, False otherwise
    """

    try:
        membership = Membership.objects.get(
            person=person,
            group=group
        )

        return membership.has_admin_rights
    except Membership.DoesNotExist:
        pass

    return False


class HasAdminRights(permissions.BasePermission):
    """
    Allows access only to users who have edit rights
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting person has permission to access a Membership
        instance
        :param request: the request being checked for permissions
        :param view: the view to which the request was made
        :param obj: the instance being accessed
        :return: True if safe method or person has edit rights, False otherwise
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        person = request.person
        group = obj.group
        return has_admin_rights(person, group)
