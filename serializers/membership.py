import swapper
from rest_framework import serializers

from groups.models import Membership
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
        corresponding AvatarSerializer serialized instances
        :param instance: the instance being represented
        :return: the dictionary representation of the instance
        """

        representation = super().to_representation(instance)

        # Convert team_member PKs to expanded dictionaries
        person = representation.get('person')
        person = AvatarSerializer(Person.objects.get(pk=person)).data
        representation['person'] = person

        return representation
