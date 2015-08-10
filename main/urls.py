from django.conf.urls import url
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from main.views import RegisterView, LoginView, LogoutView
from main.views import OrderListView, OrderModelFormView, wormhole_details_json

urlpatterns = [
    url(r'^$', OrderListView.as_view(), name='order_list'),
    url(r'^wormholes/$', OrderListView.as_view(), name='order_list'),

    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    url(r'^order-form/$', login_required(OrderModelFormView.as_view()), name='order_form'),
    url(r'^order-form/autofill/(?P<j_code>J[0-9]{6})/$', wormhole_details_json, name='wormhole_details_json'),
]
