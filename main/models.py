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


class Wormhole(models.Model):
    name = models.CharField(max_length=4, unique=True)
    life = models.IntegerField()
    space = models.ForeignKey('main.Space')
    mass = models.BigIntegerField()
    jump = models.IntegerField()

    def __unicode__(self):
        return self.name


class Effect(models.Model):
    name = models.CharField(max_length=30, unique=True)
    effect_elements = models.ManyToManyField('main.EffectElement',
                                             related_name='effects')

    def __unicode__(self):
        return self.name


class EffectElement(models.Model):
    name = models.CharField(max_length=255)
    base = models.IntegerField()
    bad = models.BooleanField()

    def __unicode__(self):
        return "{0}, {1}".format(self.name, self.base)


class System(models.Model):
    id = models.IntegerField(primary_key=True)
    j_code = models.CharField(max_length=7, unique=True)
    security = models.FloatField()
    space = models.ForeignKey('main.Space', related_name='systems')
    effect = models.ForeignKey('main.Effect', related_name='systems')
    statics = models.ManyToManyField('main.Wormhole', related_name='systems')

    def __unicode__(self):
        return self.j_code


class Space(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __unicode__(self):
        return self.name
