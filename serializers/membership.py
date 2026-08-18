import swapper
from rest_framework import serializers

from groups.models import Membership
from groups.permissions.admin import has_admin_rights
from kernel.relations.person import PersonRelatedField
from omniport.utils import switcher

AvatarSerializer = switcher.load_serializer('kernel', 'Person', 'Avatar')

Person = swapper.load_model('kernel', 'Person')


class MembershipSerializer(serializers.ModelSerializer):
    """
    Serializer for Membership objects
    """

    person = PersonRelatedField(
        queryset=Person.objects.all(),
    )

    class Meta:
        """
        Meta class for MembershipSerializer
        """

        model = Membership
        exclude = [
            'datetime_created',
            'datetime_modified',
        ]

    def to_representation(self, instance):
        """
        Convert the team member IDs from the PersonRelatedField to their
        corresponding AvatarSerializer serialized instances, and hide the
        rights flags from everyone but the administrators of the group
        :param instance: the instance being represented
        :return: the dictionary representation of the instance
        """

        representation = super().to_representation(instance)

        # Convert team_member PKs to expanded dictionaries
        person = representation.get('person')
        person = AvatarSerializer(Person.objects.get(pk=person)).data
        representation['person'] = person

        request = self.context.get('request')
        viewer = getattr(request, 'person', None)
        rights = self.context.setdefault('admin_rights', {})
        if instance.group_id not in rights:
            rights[instance.group_id] = has_admin_rights(viewer, instance.group)
        if not rights[instance.group_id]:
            representation.pop('has_edit_rights', None)
            representation.pop('has_admin_rights', None)

        return representation
