from django.db import models

from kernel.models.root import Model
from kernel.utils.upload_to import UploadTo


class Post(Model):
    """
    This model holds information about a post made by a group
    """

    group = models.ForeignKey(
        to='Group',
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to=UploadTo('groups', 'post_images'),
        max_length=255,
        blank=True,
        null=True,
    )

    text = models.TextField()

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        group = self.group
        text = self.text[:80]
        return f'{group}: {text}'
