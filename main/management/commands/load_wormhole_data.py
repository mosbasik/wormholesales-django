from django.core.management.base import BaseCommand, CommandError

from main.models import Effect, EffectElement, Space, System, Wormhole

import json
import re
import requests


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # target = 'https://static.eve-apps.com/js/combine.json'
        # target = 'https://dl.dropboxusercontent.com/s/qciyfl1a94z9k6h/combine.json'
        # result = requests.get(url=target)
        # data = json.loads(result.content)
        with open('main/static/main/combine.json', 'r') as f:
            data = json.load(f)
            self._populateEffects(data)
            self._populateWormholes(data)
            self._populateSystems(data)

    def _populateEffects(self, data):
        effects = data['effects']
        for effect in effects:

            # get or create the Effect object
            new_effect, _ = Effect.objects.get_or_create(name=effect)

            for effect_element in effects[effect]:

                # get or create the EffectElement object
                new_effect_element, _ = EffectElement.objects.get_or_create(
                                            name=effect_element['name'],
                                            base=int(effect_element['base']),
                                            bad=bool(effect_element['bad']),
                                        )

                # associate it with the parent Effect object
                new_effect.effect_elements.add(new_effect_element)

        # get or create an Effect object for the no-effect case (naturally it
        # has no associated EffectElement objects)
        Effect.objects.get_or_create(name='No Effect')

    def _populateWormholes(self, data):
        wormholes = data['wormholes']
        for wormhole in wormholes:

            # get integer from life string
            life_str = wormholes[wormhole]['life']
            life_int = int(re.search(r'^\d+', life_str).group(0))

            # get integer from mass string
            mass_str = wormholes[wormhole]['mass']
            mass_int = -1 if mass_str == 'regenerating' else int(mass_str)

            # get or create Space object from relationship field
            name_str = wormholes[wormhole]['leadsTo']
            new_space, _ = Space.objects.get_or_create(name=name_str)

            # get or create Wormhole object
            new_wormhole, _ = Wormhole.objects.get_or_create(
                                  name=wormhole,
                                  life=life_int,
                                  space=new_space,
                                  mass=mass_int,
                                  jump=int(wormholes[wormhole]['jump']),
                              )

    def _populateSystems(self, data):
        systems = data['systems']
        for system in systems:
            if 'class' in systems[system]:

                print systems[system]['name']

                # get or create system's Space object
                wh_class_str = 'Class ' + systems[system]['class']
                new_space, _ = Space.objects.get_or_create(name=wh_class_str)

                # get system's Effect object
                effect_str = 'No Effect'
                if 'effect' in systems[system]:
                    effect_str = systems[system]['effect']
                new_effect = Effect.objects.get(name=effect_str)

                # get or create System object with everything but static info
                new_system, _ = System.objects.get_or_create(
                                    id=system,
                                    j_code=systems[system]['name'],
                                    security=systems[system]['security'],
                                    space=new_space,
                                    effect=new_effect,
                                )

                # get list of names (str) of the system's static holes (if any)
                static_names = data['systems'][system]['statics']
                static_names = static_names if static_names is not None else []

                # convert it to a list of system's Wormhole objects
                new_statics = []
                for static_name in static_names:
                    new_statics.append(Wormhole.objects.get(name=static_name))

                # associate the system with each of the new static wormholes
                for new_static in new_statics:
                    print '\t', new_static.name
                    new_system.statics.add(new_static)
