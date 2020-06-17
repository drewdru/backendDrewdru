from django.db import models
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    is_done = models.BooleanField(
        default=False,
        verbose_name=_("Is Task done?"),
        help_text=_("Is Task done?"),
    )
    name = models.CharField(
        max_length=100, verbose_name=_("Task Name"), help_text=_("Task Name")
    )
    description = models.TextField(
        verbose_name=_("Task Description"), help_text=_("Task Description")
    )

    class Meta:
        verbose_name = _(u"Task")
        verbose_name_plural = _(u"Tasks")
        app_label = "api"

    def __str__(self):
        return self.name
