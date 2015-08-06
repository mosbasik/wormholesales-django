from django.conf.urls import url

from main.views import OrderListView, OrderModelFormView, wormhole_details_json

urlpatterns = [
    url(r'^wormholes/$', OrderListView.as_view(), name='order_list'),
    url(r'^order-form/$', OrderModelFormView.as_view(), name='order_form'),
    url(r'^order-form/autofill/(?P<j_code>J[0-9]{6})/$', wormhole_details_json, name='wormhole_details_json'),
]
