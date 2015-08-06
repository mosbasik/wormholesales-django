from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.generic.list import ListView

from main.forms import OrderModelForm
from main.models import Order


def home(request):
    return render(request, 'main/home.html')


class OrderListView(ListView):

    model = Order

    # def get(self, request):
    #     orders = Order.objects.all()
    #     context = {}
    #     context['orders'] = order
    #     return render(request, 'main/order_list')



class OrderModelFormView(View):

    def get(self, request):
        form = OrderModelForm()
        context = {}
        context['form'] = form
        return render(request, 'main/order_form.html', context)
        # return render(request, 'main/home.html')

    def post(self, request):
        context = {}
        form = OrderModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:order_form')
        else:
            context['form'] = form
            return render(request, 'main/order_form.html', context)
