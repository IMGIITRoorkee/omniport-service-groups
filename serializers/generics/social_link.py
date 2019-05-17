from formula_one.serializers.generics.social_information import (
    SocialLinkSerializer,
)
from groups.serializers.group_mixin import GroupSerializerMixin


class GroupSocialLinkSerializer(
    GroupSerializerMixin,
    SocialLinkSerializer
):
    """
    Extend the SocialLinkSerializer for a particular group
    """

    def update(self, instance, validated_data):
        """
        Drop the slug from the submitted data and defer to the base
        implementation of the function
        :param instance: the instance being updated
        :param validated_data: the new validated data
        :return: the updated instance
        """

        if 'slug' in validated_data:
            del validated_data['slug']

        return super().update(instance, validated_data)

    def create(self, validated_data):
        """
        Create a the new social link instance and insert it into the social
        information instance of the group
        :param validated_data: the new validated data
        :return: the newly created instance
        """

        group = validated_data.pop('slug')
        social_information, created = group.social_information.get_or_create()

        instance = super().create(validated_data)
        social_information.links.add(instance)

        return instance
