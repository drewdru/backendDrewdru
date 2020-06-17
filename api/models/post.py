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
