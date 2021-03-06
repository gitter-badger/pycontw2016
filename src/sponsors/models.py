from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import override
from django.utils.text import slugify


def logo_upload_to(instance, filename):
    return 'sponsors/{name}/{filename}'.format(
        name=slugify(instance.name, allow_unicode=True),
        filename=filename,
    )


class Sponsor(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
    )
    website_url = models.URLField(
        verbose_name=_('website URL'),
        max_length=255,
        blank=True,
    )
    intro = models.TextField(
        verbose_name=_('Introduction'),
    )
    logo = models.ImageField(
        verbose_name=_('logo'),
        upload_to=logo_upload_to,
    )

    class Level:
        PLATINUM = 0
        GOLD = 1
        SILVER = 2
        BRONZE = 3
        SPECIAL = 4

    LEVEL_CHOICES = (
        (Level.PLATINUM, _('platinum')),
        (Level.GOLD, _('gold')),
        (Level.SILVER, _('silver')),
        (Level.BRONZE, _('bronze')),
        (Level.SPECIAL, _('special')),
    )

    @property
    def level_en_name(self):
        with override('en-us'):
            return self.get_level_display()

    level = models.PositiveSmallIntegerField(
        verbose_name=_('level'),
        choices=LEVEL_CHOICES,
    )

    class Meta:
        verbose_name = _('sponsor')
        verbose_name_plural = _('sponsors')
        ordering = ('level', 'name',)

    def __str__(self):
        return self.name
