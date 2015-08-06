from django.db import models


class Order(models.Model):
    WORMHOLE_CLASSES = (
        (1, 'C1'),
        (2, 'C2'),
        (3, 'C3'),
        (4, 'C4'),
        (5, 'C5'),
        (6, 'C6'),
    )
    WORMHOLE_EFFECTS = (
        ('no_effect', 'No Effect'),
        ('black_hole', 'Black Hole'),
        ('cataclysmic_variable', 'Cataclysmic Variable'),
        ('magnetar', 'Magnetar'),
        ('pulsar', 'Pulsar'),
        ('red_giant', 'Red Giant'),
        ('wolf_rayet', 'Wolf Rayet'),
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    contact_name = models.CharField(max_length=255)
    j_code = models.CharField(max_length=7)
    price = models.FloatField()
    wormhole_class = models.IntegerField(choices=WORMHOLE_CLASSES)
    wormhole_effect = models.CharField(choices=WORMHOLE_EFFECTS, max_length=30, default='no_effect')
    information = models.TextField(null=True, blank=True)
