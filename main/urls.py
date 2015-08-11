from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from main.views import RegisterView, LoginView, LogoutView
from main.views import (
    OrderListView,
    OrderModelFormView,
    wormhole_details_json,
    validate_contact_name,
)

urlpatterns = [
    # Home page URLS
    url(r'^$', OrderListView.as_view(), name='order_list'),
    url(r'^wormholes/$', OrderListView.as_view(), name='order_list'),

    # Order form URLS
    url(r'^order-form/$',
        login_required(OrderModelFormView.as_view()),
        name='order_form'),
    url(r'^order-form/autofill/(?P<j_code>J[0-9]{6})/$',
        wormhole_details_json,
        name='wormhole_details_json'),
    url(r'^validate-contact-name/$',
        validate_contact_name,
        name='validate_contact_name'),
]
