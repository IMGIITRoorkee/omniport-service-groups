from rest_framework import permissions

from groups.models import Group, Membership


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

    def has_permission(self, request, view):
        """
        Check if the requesting person has permission to act on the collection
        of Membership instances
        :param request: the request being checked for permissions
        :param view: the view to which the request was made
        :return: True if safe method, a detail route or the person has admin
        rights over the group named in the request, False otherwise
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        if getattr(view, 'detail', False):
            return True

        try:
            group = Group.objects.get(pk=request.data.get('group'))
        except (Group.DoesNotExist, TypeError, ValueError):
            return False

        return has_admin_rights(request.person, group)

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
