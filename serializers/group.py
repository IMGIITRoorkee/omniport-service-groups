from rest_framework import serializers

from groups.models import Group
from kernel.serializers.generics.contact_information import (
    ContactInformationSerializer,
)
from kernel.serializers.generics.location_information import (
    LocationInformationSerializer,
)
from kernel.serializers.generics.social_information import (
    SocialInformationSerializer,
)


class GroupListSerializer(serializers.ModelSerializer):
    """
    Serializer for Group objects that includes the bare minimum fields
    """

    class Meta:
        """
        Meta class for GroupListSerializer
        """

        model = Group
        fields = [
            'id',
            'name',
            'slug',
            'short_description',
            'logo',
        ]


class GroupDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Group objects that includes more fields
    """

    contact_information = ContactInformationSerializer(
        many=True,
    )
    location_information = LocationInformationSerializer(
        many=True,
    )
    social_information = SocialInformationSerializer(
        many=True,
    )

    class Meta:
        """
        Meta class for GroupDetailSerializer
        """

        model = Group
        read_only_fields = [
            'contact_information',
            'location_information',
            'social_information',
        ]
        exclude = [
            'datetime_created',
            'datetime_modified',
            'members',
        ]
