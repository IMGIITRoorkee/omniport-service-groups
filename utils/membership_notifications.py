from notifications.actions import push_notification

from groups.utils.get_category import get_category


def send_membership_notification(group_name, membership_type, person_id):
    """
    Send appropriate notifications to member of the group as per
    membership_type parameter
    :param group_name: name of the group
    :param membership_type: add/edit/remove
    :param person_id: id of the person added/edited/removed in the group
    :return: notification
    """

    if membership_type == 'add':
        template = f'You have been added in the {group_name}'
    elif membership_type == 'edit':
        template = f'Your details have been changed in {group_name}'
    elif membership_type == 'remove':
        template = f'You have been removed from {group_name}'
    else:
        return
    push_notification(
        template=template,
        category=get_category(),
        web_onclick_url='',
        android_onclick_activity='',
        ios_onclick_action='',
        is_personalised=True,
        person=person_id,
        has_custom_users_target=False,
        persons=None,
    )
