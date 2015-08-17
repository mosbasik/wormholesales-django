from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from main.models import Character, System, Order

import json
import re
import requests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('main/static/main/test_sale_data.json', 'r') as f:
            data = json.load(f)
            self._populateCharacters(data)
            self._populateOrders(data)

    def _populateCharacters(self, data):
        for order in data['order']:
            char, created = Character.objects.get_or_create(
                    name=order['contact_name'])

    def _populateOrders(self, data):
        for order in data['order']:
            order = Order.objects.create(
                    user=User.objects.get(
                            username=order['user']),
                    contact_name=Character.objects.get(
                            name=order['contact_name']),
                    system=System.objects.get(
                            j_code=order['system']),
                    price=order['price'],
                    information=order['information'])
