from django.core.exceptions import MiddlewareNotUsed, ImproperlyConfigured
from django.contrib.flatpages.views import flatpage
from django.db.models.loading import AppCache
from django.http import Http404
from django.views.generic import simple

from middleware import get_current_section, lookup_section_from_request
import app_settings 

Section = app_settings.get_extending_model()

def section(request, section_path=None):
    """
    A view of a section.
    """
    try:
        section = get_current_section()
    except MiddlewareNotUsed:
        section = lookup_section_from_request(request)
    if section:
        return simple.direct_to_template(request, 
            template = "scaffold/section.html",
            extra_context = {'section': section}
        )        
    else:
        app_cache = AppCache()
        try:
            app_cache.get_app('flatpages')
            try:
                return flatpage(request, request.path_info)
            except Http404:
                pass
        except ImproperlyConfigured:
            pass
        raise Http404, "Section does not exist."