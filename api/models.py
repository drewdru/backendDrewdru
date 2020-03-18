from django.db import models
from django.utils.translation import ugettext_lazy as _


class Post(models.Model):
    title = models.CharField(
        max_length=100, verbose_name=_("Post Title"), help_text=_("Post Title")
    )
    content = models.CharField(
        max_length=100,
        verbose_name=_("Post Content"),
        help_text=_("Post Content"),
    )

    class Meta:
        verbose_name = _(u"Post")
        verbose_name_plural = _(u"Posts")
        app_label = "api"

    def __str__(self):
        return self.title


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
