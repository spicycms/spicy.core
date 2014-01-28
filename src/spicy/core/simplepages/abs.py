from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template import loader, Template
from spicy.utils import cached_property


class AbstractBasePage(models.Model):
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(
        _('content'), blank=True,
        default=(
            '{% extends current_base %}\n'
            '{% block content %}\n<!-- Page content here-->\n'
            '{% endblock %}'))
    template_name = models.CharField(
        _('template name'), max_length=255, blank=True, default='',
        help_text=_(
            "Example: 'spicy.core.simplepages/simplepages/default.html'. "
            "If this isn't provided, content can be edited by hand."))
    sites = models.ManyToManyField('sites.Site')

    #@cached_property
    def get_template(self):
        if self.template_name:
            return loader.get_template(self.template_name)
        return Template(self.content)

    class Meta:
        abstract = True
        db_table = 'sp_simplepage'
        verbose_name = _('simple page')
        verbose_name_plural = _('simple pages')
        ordering = ('url',)
        permissions = [('change_robots_txt', 'Robots.txt')]

    def __unicode__(self):
        return u"{0} -- {1}".format(self.url, self.title)

    def get_absolute_url(self):
        return u'/{0}'.format(self.url)


class AbstractSimplePage(AbstractBasePage):
    enable_comments = models.BooleanField(_('enable comments'), default=False)
    registration_required = models.BooleanField(
        _('registration required'),
        help_text=_(
            "If this is checked, only logged-in users will be able to view "
            "the page."),
        default=False)

    class Meta(AbstractBasePage.Meta):
        abstract = True
