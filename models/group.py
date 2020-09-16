import datetime

import swapper
from django.contrib.contenttypes import fields as contenttypes_fields
from django.db import models

from formula_one.models.base import Model
from formula_one.utils.upload_to import UploadTo
from formula_one.validators.aspect_ratio import AspectRatioValidator
from formula_one.validators.year_relation import YearRelationValidator

from tinymce.models import HTMLField


class Group(Model):
    """
    This model stores information about a group on campus
    """

    acronym = models.CharField(
        max_length=15,
        unique=True,
    )
    name = models.CharField(
        max_length=127,
    )
    slug = models.SlugField(
        max_length=127,
        unique=True,
    )

    year_of_inception = models.IntegerField(
        blank=True,
        null=True,
        validators=[
            YearRelationValidator('<='),
        ]
    )

    short_description = models.CharField(
        max_length=127,
        blank=True,
    )
    about = HTMLField()
    mission = HTMLField()

    logo = models.ImageField(
        upload_to=UploadTo('groups', 'logos'),
        max_length=255,
        validators=[
            AspectRatioValidator(1),
        ],
        blank=True,
        null=True,
    )
    cover_image = models.ImageField(
        upload_to=UploadTo('groups', 'cover_images'),
        max_length=255,
        blank=True,
        null=True,
    )

    contact_information = contenttypes_fields.GenericRelation(
        to='formula_one.ContactInformation',
        related_query_name='group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    social_information = contenttypes_fields.GenericRelation(
        to='formula_one.SocialInformation',
        related_query_name='group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )
    location_information = contenttypes_fields.GenericRelation(
        to='formula_one.LocationInformation',
        related_query_name='group',
        content_type_field='entity_content_type',
        object_id_field='entity_object_id',
    )

    members = models.ManyToManyField(
        to=swapper.get_model_name('kernel', 'Person'),
        through='Membership',
        blank=True,
    )

    @property
    def age_in_years(self):
        """
        Return the age of the group in years
        :return: the age of the group in years
        """

        years = datetime.date.today().year - self.year_of_inception
        return years

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        acronym = self.acronym
        name = self.name
        return f'{acronym}: {name}'
