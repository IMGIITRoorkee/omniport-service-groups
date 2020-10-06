import re

from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo

from tinymce.models import HTMLField

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

    text = HTMLField()

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        group = self.group
        html_inner_text = re.sub('<.*?>', '', self.text)
        text = html_inner_text[:80]        
        return f'{group}: {text}'
        
