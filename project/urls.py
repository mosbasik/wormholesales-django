"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# serving static files
from django.conf import settings
from django.conf.urls.static import static
from main.views import RegisterView, LoginView, LogoutView
import django.contrib.auth.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls', namespace='main')),

    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),

    url(r'^password/reset/$',
        django.contrib.auth.views.password_reset,
        {"template_name": "project/password_reset/password_reset_form.html"},
        name="password_reset"
        ),
    url(r'^password/reset/done/$',
        django.contrib.auth.views.password_reset_done,
        {"template_name": "project/password_reset/password_reset_form_done.html"},
        name="password_reset_done"),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        django.contrib.auth.views.password_reset_confirm,
        {"template_name": "project/password_reset/password_reset_confirm.html"},
        name="password_reset_confirm"),
    url(r'^password/reset/confirm/done/$',
        django.contrib.auth.views.password_reset_complete,
        {"template_name": "project/password_reset/password_reset_complete.html"},
        name="password_reset_complete"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
