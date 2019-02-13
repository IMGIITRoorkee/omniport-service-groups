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
