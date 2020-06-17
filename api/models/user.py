from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _

User = get_user_model()
NULLABLE = dict(null=True, blank=True)


class UserProfile(models.Model):
    GENDERS = (
        ("male", _("Male")),
        ("female", _("Female")),
    )
    user = models.OneToOneField(
        User, related_name="user_profile", on_delete=models.CASCADE,
    )
    gender = models.CharField(
        max_length=255,
        choices=GENDERS,
        default="male",
        verbose_name=_("Gender"),
        help_text=_("Gender"),
    )

    class Meta:
        verbose_name = _(u"Profile")
        verbose_name_plural = _(u"Profiles")
        app_label = "api"

    def __str__(self):
        return self.name
