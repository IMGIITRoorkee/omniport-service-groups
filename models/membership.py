import swapper
from django.db import models

from formula_one.mixins.period_mixin import PeriodMixin
from formula_one.models.base import Model


class Membership(PeriodMixin, Model):
    """
    This model holds information about a person's membership in a group
    """

    person = models.ForeignKey(
        to=swapper.get_model_name('kernel', 'Person'),
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        to='Group',
        on_delete=models.CASCADE,
    )

    # See kernel.Maintainer for more information about these fields
    designation = models.CharField(
        max_length=127,
        blank=True,
    )
    post = models.CharField(
        max_length=127,
        blank=True,
    )

    has_edit_rights = models.BooleanField(
        default=False,
    )

    has_admin_rights = models.BooleanField(
        default=False,
    )

    class Meta:
        """
        Meta class for Membership
        """

        unique_together = ('person', 'group')

    def __str__(self):
        """
        Return the string representation of the model
        :return: the string representation of the model
        """

        group = self.group
        person = self.person
        return f'{group} - {person}'
