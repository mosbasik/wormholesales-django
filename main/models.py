from django.contrib.auth.models import User
from django.db import models

import re


class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    portrait = models.ImageField(null=True, blank=True)

    @property
    def evewho_link(self):
        url_stub = 'http://evewho.com/pilot/'
        name = self.name.replace(' ', '+')
        return url_stub + name

    def __unicode__(self):
        return self.name


class Effect(models.Model):
    name = models.CharField(max_length=30, unique=True)
    effect_elements = models.ManyToManyField('main.EffectElement',
                                             related_name='effects')

    @property
    def blankname(self):
        if self.name == 'No Effect':
            return ''
        return self.name

    def __unicode__(self):
        return self.name


class EffectElement(models.Model):
    name = models.CharField(max_length=255)
    base = models.IntegerField()
    bad = models.BooleanField()

    def __unicode__(self):
        return "{0}, {1}".format(self.name, self.base)


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    contact_name = models.ForeignKey('main.Character')
    system = models.ForeignKey('main.System')
    price = models.DecimalField(max_digits=16, decimal_places=2)
    information = models.TextField(null=True, blank=True)
    is_sell = models.BooleanField()

    def __unicode__(self):
        return "{1} :: {2} :: {0}".format(self.created,
                                          self.system.j_code,
                                          self.system.effect.blankname)


class Space(models.Model):
    name = models.CharField(max_length=50, unique=True)

    @property
    def code(self):
        '''
        Returns a one (or two, for shattered holes) character code indicating
        the type of space ('H', 'L', 'N', '1', '13', etc)
        '''
        if self.name == 'High-Sec':
            return 'H'
        if self.name == 'Low-Sec':
            return 'L'
        if self.name == 'Null-Sec':
            return 'N'
        # regex = re.compile(r'[^\d]+')
        return self.name[6:]

    @property
    def abbrev(self):
        '''
        Returns a two-character string abbreviation of the type of space
        ('Hs', 'Ls', 'Ns', 'C1', 'C13', etc).
        '''
        if self.name == 'High-Sec':
            return 'Hs'
        if self.name == 'Low-Sec':
            return 'Ls'
        if self.name == 'Null-Sec':
            return 'Ns'
        # regex = re.compile(r'[^\d]+')
        return '{0}{1}'.format('C', self.name[6:])

    @property
    def multiplier(self):
        '''
        Returns an integer one less than the space's class value (that is, a
        Class 5 space will return a 4x multiplier value).  A blanket exception
        exists for all "shattered" wormhole classes (C13, C18, etc).  All of
        these x5 multiplier.
        '''
        abbrev = int(self.abbrev[1:])
        return (abbrev - 1) if abbrev < 6 else 5

    def __unicode__(self):
        return self.name


class System(models.Model):
    id = models.IntegerField(primary_key=True)
    j_code = models.CharField(max_length=7, unique=True)
    security = models.FloatField()
    space = models.ForeignKey('main.Space', related_name='systems')
    effect = models.ForeignKey('main.Effect', related_name='systems')
    statics = models.ManyToManyField('main.Wormhole', related_name='systems')

    @property
    def eveplanet_URL(self):
        url_stub = 'http://eveplanets.com/eve/system/index/?show='
        return url_stub + self.j_code

    def __unicode__(self):
        return "{0} {1} {2}".format(self.j_code, self.space, self.effect)


class Wormhole(models.Model):
    name = models.CharField(max_length=4, unique=True)
    life = models.IntegerField()
    space = models.ForeignKey('main.Space')
    mass = models.BigIntegerField()
    jump = models.IntegerField()

    def __unicode__(self):
        return self.name
