from django.contrib.auth import views
from spicy.core.profile.decorators import is_staff
from spicy.core.service import api
from spicy.core.siteskin.decorators import render_to


def login(request):
    return views.login(
        request, template_name='spicy.core.admin/admin/login.html')


def logout(request):
    return views.logout(request, template_name='spicy.core.admin/admin/logout.html')
