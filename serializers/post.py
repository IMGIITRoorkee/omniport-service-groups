from rest_framework import serializers

from groups.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post objects
    """

    class Meta:
        """
        Meta class for PostSerializer
        """

        model = Post
        exclude = [
            'datetime_modified',
        ]
