from django.conf.urls import url

from main.views import OrderListView, OrderModelFormView

urlpatterns = [
    url(r'^$', 'main.views.home', name='home'),
    url(r'^wormholes/$', OrderListView.as_view(), name='order_list'),
    url(r'^order-form/$', OrderModelFormView.as_view(), name='order_form'),
]
