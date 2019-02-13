from rest_framework import permissions

from groups.models import Membership


def has_edit_rights(person, group):
    """
    Check if the person has rights to make edits to the group
    :param person: the person whose rights are being checked
    :param group: the group whose member the person must be
    :return: True if the person has edit or admin rights, False otherwise
    """

    try:
        membership = Membership.objects.get(
            person=person,
            group=group
        )

        return membership.has_edit_rights or membership.has_admin_rights
    except Membership.DoesNotExist:
        pass

    return False


class HasEditRights(permissions.BasePermission):
    """
    Allows access only to users who have edit rights
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting person has permission to access a Group instance
        :param request: the request being checked for permissions
        :param view: the view to which the request was made
        :param obj: the instance being accessed
        :return: True if safe method or person has edit rights, False otherwise
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        person = request.person
        return has_edit_rights(person, obj)


class HasPostingRights(permissions.BasePermission):
    """
    Allows access only to users who have edit rights
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting person has permission to access a Post instance
        :param request: the request being checked for permissions
        :param view: the view to which the request was made
        :param obj: the instance being accessed
        :return: True if safe method or person has edit rights, False otherwise
        """

        if request.method in permissions.SAFE_METHODS:
            return True

        person = request.person
        group = obj.group
        return has_edit_rights(person, group)
