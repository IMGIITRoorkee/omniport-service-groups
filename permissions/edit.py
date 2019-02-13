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
