from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from main.models import Character, System, Order

import json
from lxml import etree
import requests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with open('main/static/main/test_sale_data.json', 'r') as f:
            data = json.load(f)
            self._wipe_data()
            self._populate_characters(data)
            self._populate_orders(data)

    def _wipe_data(self):
        Order.objects.all().delete()
        Character.objects.all().delete()

    def _populate_characters(self, data):
        for order in data['order']:
            name = order['contact_name']

            # if name is already in our database, skip it and continue
            if Character.objects.filter(name=name).exists():
                continue

            # if name is not already cached in our database, check the API
            else:
                url_stub = 'https://api.eveonline.com/eve/CharacterID.xml.aspx?names='
                response = requests.get(url_stub + name)
                tree = etree.XML(response.content)
                character_id_xpath = '/eveapi/result/rowset/row/@characterID'
                character_id = int(tree.xpath(character_id_xpath)[0])

                # make sure no garbage data is being introduced
                assert character_id != 0

                # create character
                Character.objects.create(id=character_id, name=name)

    def _populate_orders(self, data):
        for order in data['order']:
            order = Order.objects.create(
                    user=User.objects.get(
                            username=order['user']),
                    contact_name=Character.objects.get(
                            name=order['contact_name']),
                    system=System.objects.get(
                            j_code=order['system']),
                    price=order['price'],
                    information=order['information'],
                    is_sell=True)
