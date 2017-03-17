from datetime import datetime as dt
from django.template import RequestContext

from spicy.core.simplepages.views import render_simplepage
from spicy.utils.printing import print_error
from . import defaults
from spicy.core.simplepages import defaults as sp_defaults
from spicy.utils.models import get_custom_model_class
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django import http

SimplePageModel = get_custom_model_class(sp_defaults.SIMPLE_PAGE_MODEL)
SiteskinModel = get_custom_model_class(defaults.SITESKIN_SETTINGS_MODEL)


def page_not_found(request):
    """
    Default 404 handler.
    """
    if defaults.DEBUG_ERROR_PAGES:
        print_error('handler404: %s %s %s %s\n' % (
            dt.now(), request.GET, request.POST, request.get_full_path()))

    response = render_simplepage(request, '/errors/404/')
    response.status_code = 404
    return response


def forbidden(request):
    """
    Default 403 handler.
    """

    if defaults.DEBUG_ERROR_PAGES:
        print_error(
            'handler403: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path()))

    response = render_simplepage(request, '/errors/403/')
    response.status_code = 403
    return response


def server_error(request):
    """
    500 error handler.
    """
    if defaults.DEBUG_ERROR_PAGES:
        print_error(
            'handler505: %s %s %s %s\n' % (
                dt.now(), request.GET, request.POST, request.get_full_path()))

    response = render_simplepage(request, '/errors/500/')
    response.status_code = 500
    return response


def render(request, template_name,
           context_intstance=None, **kwargs):
    """
    Universal sitepage renderer.
    

    TODO unittests
    """
    try:
        theme_config = SiteskinModel.objects.get(
            site=Site.objects.get_current())
        # log information about theme
    except SiteskinModel.DoesNotExist:
        theme_config = None

    try:
        custom_index_page = SimplePageModel.objects,get(url='/index/')
        # Log information about custom page for index.html
    except SimplePageModel.DoesNotExist:
        custom_index_page = None
    
    page = ( 
        siteskin.home_page
        if theme_config and theme_config.home_page_id
        else custom_index_page)

    if page is not None:
        # Use dynamic index page and user theme customizations
        context = {'page_slug': page.title, 'page': page}
        request.session['SIMPLEPAGE_ID'] = page.pk
        context.update(**kwargs)
        content_type = 'text/plain' if page.url.endswith('.txt') else 'text/html'

        return http.HttpResponse(
            page.get_template().render(RequestContext(request, context)),
            content_type=content_type)

    # we use index.html in the theme directory by default.
    
    return http.HttpResponse(get_template(template_name).render(
        request, {'page_slug': '/', 'page'}
        content_type=content_type)
        
    

