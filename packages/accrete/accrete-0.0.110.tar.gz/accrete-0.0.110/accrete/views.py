import os
from functools import wraps
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import login_required
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from accrete.models import Tenant, Member
from . import config


class TenantRequiredMixin(LoginRequiredMixin):

    tenant_missing_url = None
    member_access_groups = []
    member_not_authorized_url = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.tenant:
            return self.handle_no_tenant()
        if not request.user.is_staff:
            if self.member_access_groups and not self.member_has_access():
                return self.handle_member_not_authorized()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_tenant(self):
        return redirect(self.get_tenant_not_set_url())

    def get_tenant_not_set_url(self):
        tenant_not_set_url = (
                self.tenant_missing_url
                or settings.ACCRETE_TENANT_NOT_SET_URL
        )
        if not tenant_not_set_url:
            cls_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{cls_name} is missing the tenant_not_set_url attribute. "
                f"Define {cls_name}.tenant_not_set_url, "
                f"settings.ACCRETE_TENANT_NOT_SET_URL, or override "
                f"{cls_name}.get_tenant_not_set_url()."
            )
        return tenant_not_set_url

    def member_has_access(self):
        return self.request.member.access_groups.filter(
            code__in=self.member_access_groups
        ).exists()

    def handle_member_not_authorized(self):
        return redirect(self.get_member_not_authorized_url())

    def get_member_not_authorized_url(self):
        url = (self.member_not_authorized_url
               or settings.TENANT_MEMBER_NOT_AUTHORIZED_URL)
        if not url:
            cls_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{cls_name} is missing the member_not_authorized_url "
                f"attribute. Define {cls_name}.member_not_authorized_url, "
                f"settings.TENANT_MEMBER_NOT_AUTHORIZED_URL, or override "
                f"{cls_name}.get_member_not_authorized_url()."
            )
        return url


def tenant_required(
        redirect_field_name: str = None,
        login_url: str = None
):
    def decorator(f):
        @wraps(f)
        @login_required(
            redirect_field_name=redirect_field_name,
            login_url=login_url
        )
        def _wrapped_view(request, *args, **kwargs):
            tenant = request.tenant
            if not tenant:
                return redirect(config.ACCRETE_TENANT_NOT_SET_URL)
            if kwargs.get('tenant'):
                kwargs.pop('tenant')
            return f(request, *args, **kwargs)
        return _wrapped_view
    return decorator


@tenant_required()
def get_tenant_file(request, tenant_id, filepath):
    tenant = get_object_or_404(Tenant, pk=tenant_id)
    if not request.user.is_staff:
        member = Member.objects.filter(user=request.user, tenant=tenant)
        if not member.exists():
            return HttpResponseNotFound()
    filepath = f'{settings.MEDIA_ROOT}/{tenant_id}/{filepath}'
    if not os.path.exists(filepath):
        return HttpResponseNotFound()
    with open(filepath, 'rb') as f:
        return HttpResponse(f)
