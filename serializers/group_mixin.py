from rest_framework import serializers

from groups.models import Group


class GroupSerializerMixin(serializers.Serializer):
    """
    Identify a group based on the slug
    """

    slug = serializers.CharField(
        write_only=True,
    )

    def validate_slug(self, value):
        """
        Validate the slug provided and clean it by setting a Group instance
        :param value: the value provided to the serializer
        :return: the Group instance pertaining to this slug
        :raise: serializers.ValidationError, if the slug does not match a group
        """

        try:
            return Group.objects.get(slug=value)
        except Group.DoesNotExist:
            raise serializers.ValidationError('The slug is incorrect.')
