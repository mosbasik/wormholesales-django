from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.generic import View
from django.views.generic.list import ListView

from main.forms import OrderModelForm
from main.models import Order, System

import json


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.all().order_by('-modified')


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
            form.save()
            return redirect('main:order_form')
        else:
            context['form'] = form
            return render(request, 'main/order_form.html', context)


def wormhole_details_json(request, j_code=None):
    if request.method == 'GET':
        system = System.objects.get(j_code=j_code)
        data = json.dumps({
            'wormhole_class': {
                'value': system.space.id,
                'name': system.space.name,
            },
            'wormhole_effect': {
                'value': system.effect.id,
                'name': system.effect.name,
            },
        })
        return HttpResponse(data, content_type='application/json')
    return HttpResponse(status=405)
