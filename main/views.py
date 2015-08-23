# django imports
# from django.contrib.humanize.templatetags.humanize import intword, intcomma
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
# from django.template.defaultfilters import date
from django.views.generic import View
from django.views.generic.list import ListView

# django user authentication imports
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout,
)

# project imports
from main.forms import OrderModelForm, UserCreationForm
from main.models import Order, System, Character
# from main.templatetags.customfilters import sigfigs
# from main.templatetags.nbsp import nbsp
from project.settings import EFFECT_CONST

# python imports
from lxml import etree
import json
import requests
import urllib


class RegisterView(View):

    def get(self, request):
        # if  a user is already logged in, redirect to the order page
        if request.user.is_authenticated():
            return redirect('main:sell_list')

        # save a blank user creation form in the context and reload page
        context = {'form': UserCreationForm}
        return render(request, 'project/register.html', context)

    def post(self, request):

        # if  a user is already logged in, redirect to the order page
        if request.user.is_authenticated():
            return redirect('main:sell_list')

        # get and check if the filled user creation form is valid
        filled_user_creation_form = UserCreationForm(request.POST)
        if filled_user_creation_form.is_valid():

            # create a new user object with the form information
            user = filled_user_creation_form.save()

            # authenticate the new user against the database (a formality)
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])

            # log the new user into the site and redirect to front page
            auth_login(request, user)
            return redirect('main:sell_list')

        # if the filled form was invalid
        else:

            # save error message and invalid form to be passed back for editing
            context = {}
            context['error_on_create'] = True
            context['form'] = filled_user_creation_form
            return render(request, 'project/register.html', context)


def landing_page(request):
    context = {}
    context['sell_count'] = Order.objects.filter(is_sell=True).count()
    context['buy_count'] = Order.objects.filter(is_sell=False).count()
    return render(request, 'main/landing_page.html', context)


class LoginView(View):

    def get(self, request):
        context = {}
        context['next'] = request.GET.get('next', '/')
        print context
        return render(request, 'project/login.html', context)

    def post(self, request):

        # if a user is already logged in, redirect to the order page
        if request.user.is_authenticated():
            return redirect('main:sell_list')

        # create blank context dictionary for some reason
        context = {}

        # attempt to authenticate the user
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        # if the user is found in the database
        if user is not None:

            # and the user's account is active
            if user.is_active:
                auth_login(request, user)

                return redirect(request.POST.get('next', None))

                # then go ahead and log the user in and redirect to front page

            # if the user's account is not active
            else:

                # reload login page and display error message
                context['error'] = 'Account deactivated.'
                return render(request, 'project/login.html', context)

        # if this user doesn't appear in the database
        else:

            # reload login page and display error message
            context['error'] = 'Username or password not found'
            return render(request, 'project/login.html', context)


class LogoutView(View):

    def get(self, request):
        auth_logout(request)
        return redirect('main:sell_list')


class OrderDetails(View):

    def get(self, request, id=None):
        context = {}
        context['order'] = Order.objects.get(id=id)
        return render(request, 'main/order_details.html', context)

    def post(self, request, id=None):
        pass


class SellOrderListView(ListView):
    model = Order
    template_name = 'main/sell_list.html'

    def get_queryset(self):
        return Order.objects.all().order_by('-modified')


class BuyOrderListView(ListView):
    pass


def filter_view(request):

    if request.method == 'GET':
        # print '\n'

        # make a blank context dict
        context = {}

        # get the data from the request and load it into a filters dict
        f = request.GET.get('filters', None)
        filters = json.loads(f)

        # combine "normal" wormhole class group and "shattered" wormhole class
        # group into one "class" group so that selections from both groups are
        # OR'ed together (instead of AND'ed, which is the default behavior for
        # buttons in different groups.)
        filters['class'] = filters['normal_class'] + filters['shattered_class']

        # import pprint; pprint.pprint(filters)

        # get the queryset of all existing wormhole systems
        system_qs = System.objects.all()

        # apply the wormhole-level filters (the simplest filters, that are only
        # concerned with the basic attributes of the wormhole being sold)
        wormhole_qs = system_qs
        if filters['class']:
            wormhole_qs = wormhole_qs.filter(space__name__in=filters['class'])
        if filters['effect']:
            wormhole_qs = wormhole_qs.filter(effect__name__in=filters['effect'])

        # Assume we have saved all the systems with two statics in this qs:
        static_double_qs = wormhole_qs

        # precaution: only continue if a list of static filters was received
        if filters['statics']:
            statics = filters['statics']

            # create master_filters dict containing all of the possible values
            # for all the possible groups that statics can be filtered on,
            # coupled with the strings used to perform the Django ORM queries
            # that actually apply those filters to a System queryset.
            master_filters = {
                'class': (
                    'statics__space__name__in',
                    [
                        'Class 1',
                        'Class 2',
                        'Class 3',
                        'Class 4',
                        'Class 5',
                        'Class 6',
                        'High-Sec',
                        'Low-Sec',
                        'Null-Sec',
                    ],
                ),
                'life': (
                    'statics__life__in',
                    [
                        '16',
                        '24',
                    ],
                ),
                'mass': (
                    'statics__mass__in',
                    [
                        '500000000',
                        '1000000000',
                        '2000000000',
                        '3000000000',
                        '5000000000',
                    ],
                ),
                'jump': (
                    'statics__jump__in',
                    [
                        '20000000',
                        '300000000',
                        '1350000000',
                    ],
                ),
            }

            # iterate over each filter group in the master_filters dict and
            # unpack the name of the group, the query it needs, and the master
            # list of filters for that group.
            for master_key, (query, master_filter) in master_filters.items():

                # get the list of filters for static 1, if any
                filter_1 = master_filter
                if statics['static-1']:
                    static = statics['static-1']
                    if static[master_key]:
                        filter_1 = static[master_key]
                # print filter_1

                # get the list of filters for static 2, if any
                filter_2 = master_filter
                if statics['static-2']:
                    static = statics['static-2']
                    if static[master_key]:
                        filter_2 = statics['static-2'][master_key]
                # print filter_2

                # get the list of filters not in filter 1 OR filter 2
                filter_negative = set(master_filter).difference(
                    filter_1 + filter_2)
                # print filter_negative

                # filter on membership in filter 1 AND filter_2
                static_double_qs = static_double_qs.filter(
                    **{query: filter_1, query: filter_2})

                # exclude on membership in the negative filter
                static_double_qs = static_double_qs.exclude(
                    **{query: filter_negative})

                # print '\n'

            # now you have the matching two static holes
            static_double_qs = static_double_qs.distinct()

        # for s in static_double_qs:
        #     listing = ''
        #     listing += str(s)
        #     listing += str([x.space.name for x in s.statics.all()])
        #     listing += str([x.life for x in s.statics.all()])
        #     listing += str([x.mass for x in s.statics.all()])
        #     listing += str([x.jump for x in s.statics.all()])
        #     print listing

        # filter for systems that exist in sell orders
        existing_systems = static_double_qs
        open_orders = Order.objects.filter(is_sell=True)
        systems_with_orders = existing_systems.filter(orders__in=open_orders)
        matching_orders = open_orders.filter(system__in=systems_with_orders)

        # populate the context dict with relevant information
        context['object_list'] = matching_orders
        context['existing_count'] = existing_systems.count()
        context['order_count'] = matching_orders.count()

        return render_to_response('main/table_base.html', context)

    else:
        # bad request by client
        return HttpResponse(status=400)


class OrderModelFormView(View):

    def get(self, request):
        form = OrderModelForm()
        context = {}
        context['form'] = form
        return render(request, 'main/order_form.html', context)

    def post(self, request):
        context = {}
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.is_sell = True
            order.save()
            return redirect('main:sell_list')
        else:
            context['form'] = form
            return render(request, 'main/order_form.html', context)


class UserOrderListView(ListView):
    model = Order
    template_name = "main/user_order_list.html"

    def get_queryset(self):
        # CASE: user/buy/
        if self.kwargs['set_string'] == 'buy':
            return Order.objects.filter(
                    user=self.request.user,
                    is_sell=False).order_by('-modified')
        # CASE: user/sell/
        elif self.kwargs['set_string'] == 'sell':
            return Order.objects.filter(
                    user=self.request.user,
                    is_sell=True).order_by('-modified')
        # CASE: user/all/
        else:
            return Order.objects.filter(
                    user=self.request.user).order_by('-modified')

    def get_context_data(self, **kwargs):
        context = super(UserOrderListView, self).get_context_data(**kwargs)
        context['set_string'] = self.kwargs['set_string']
        return context


def wormhole_details_json(request, j_code=None):
    if request.method == 'GET':

        # get the system in question
        system = System.objects.get(j_code=j_code)

        # make a list of its statics
        statics = [{'name': s.name,
                    'mass': s.mass,
                    'jump': s.jump,
                    'space': s.space.name,
                    'abbrev': s.space.abbrev,
                    'life': s.life} for s in system.statics.all()]

        # make a list of its effect elements
        elements = []
        for e in system.effect.effect_elements.all():
            element = {}

            base = e.base               # the base effect str
            mult = system.space.multiplier  # class-based str multiplier
            incr = base / EFFECT_CONST  # str difference between two classes
            amnt = incr * mult          # str additional to base due to class
            perc = base + amnt          # total percent value of effect

            element['name'] = e.name
            element['bad'] = e.bad
            element['percent'] = perc

            elements.append(element)

        # use everything we just made to make a json file to be returned
        data = json.dumps({
            'system': system.j_code,
            'statics': statics,
            'class': system.space.name,
            'effect': {
                'name': system.effect.name,
                'elements': elements,
            },
        })
        return HttpResponse(data, content_type='application/json')
    return HttpResponse(status=405)


def validate_contact_name(request):
    if request.method == 'GET':
        name = request.GET['name']

        # if name is already in our database, it's valid; return success
        if Character.objects.filter(name=name).exists():
            return HttpResponse(status=200)

        # if name is not already cached in our database, check the API
        else:
            url_stub = 'https://api.eveonline.com/eve/CharacterID.xml.aspx?names='
            response = requests.get(url_stub + name)
            tree = etree.XML(response.content)
            character_id_xpath = '/eveapi/result/rowset/row/@characterID'
            character_id = int(tree.xpath(character_id_xpath)[0])

            # if the API returns an id of 0, name is invalid;  return failure
            if character_id == 0:
                return HttpResponse(status=404)

            # otherwise the name is valid; save it and return success
            Character.objects.create(id=character_id, name=name)
            return HttpResponse(status=200)

    else:
        # client made bad request, return failure
        return HttpResponse(status=400)
