from optparse import make_option
import sys
import traceback

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import NoArgsCommand
from django.core.management.color import no_style
from django.core.management.sql import custom_sql_for_model, emit_post_sync_signal
from django.db import connections, router, transaction, models, DEFAULT_DB_ALIAS
from django.utils.datastructures import SortedDict
from django.utils.importlib import import_module

from django.core.management.commands.syncdb import Command as SyncDBCommand
from spicy.utils.printing import print_info

class Command(SyncDBCommand):
    def handle_noargs(self, **options):
        super(Command, self).handle_noargs(**options)

        sites = Site.objects.all()
        if not sites:
            site_url = getattr(settings, 'SITE_URL', 'example.com')
            site_name = getattr(settings, 'SITE_NAME', site_url)
            
            # TODO
            # if settings.SITE_ID set to 2 or 3
            # ? create more sites for testing using for...range(2)?

            site = Site(domain=site_url, name=site_name)
            site.save()
            sites = Site.objects.all()
        
            print_info('Current SITE set to `{}` SITE_ID={}'.format(site_name, site.id))
