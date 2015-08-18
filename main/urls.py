from django.conf.urls import url, include
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required

from main.views import RegisterView, LoginView, LogoutView
from main.views import (
    # OrderListView,
    SellOrderListView,
    BuyOrderListView,
    filter_view,
    OrderDetails,
    OrderModelFormView,
    UserOrderListView,
    wormhole_details_json,
    validate_contact_name,
    landing_page,
)

urlpatterns = [
    # Home page URLS
    url(r'^$', landing_page, name='home'),

    # Public order page (and filtering) URLS
    url(r'^sell/$', SellOrderListView.as_view(), name='sell_list'),
    url(r'^buy/$', BuyOrderListView.as_view(), name='buy_list'),
    url(r'^(sell|buy)/filter/$', filter_view, name='filter'),

    # User order URLS
    url(r'^user/(?P<set_string>(all|buy|sell))/$',
        login_required(UserOrderListView.as_view()),
        name='user_order_list'),

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

    # Order Details
    url(r'^order-details/(?P<id>[0-9]+)/$',
        OrderDetails.as_view(),
        name='order_details'),

    # Legacy URLS
    url(r'^wormholes/$', SellOrderListView.as_view(), name='wormholes'),
]
