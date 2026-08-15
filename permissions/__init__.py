from rest_framework import permissions

from groups.models import Group


def has_rights_over_named_group(request, view, rights_function):
    """
    Check the rights of the requesting person over the group named in the body
    of the request
    :param request: the request being checked for permissions
    :param view: the view to which the request was made
    :param rights_function: the function that checks the rights of a person
    over a group
    :return: True if the request is allowed to proceed, False otherwise
    """

    if request.method in permissions.SAFE_METHODS:
        return True

    group = request.data.get('group')
    if group is None:
        return bool(getattr(view, 'detail', False))

    try:
        group = Group.objects.get(pk=group)
    except (Group.DoesNotExist, TypeError, ValueError):
        return False

    return rights_function(request.person, group)
