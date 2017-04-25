from django.db import models


class Distillery(models.Model):
    """The Distillery where whiskies are created."""
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    url = models.CharField(max_length=255)


class Type(models.Model):
    """The type of whisky."""
    name = models.CharField(max_length=255)


class Bottler(models.Model):
    """The bottler for a whisky."""
    name = models.CharField(max_length=255)


class Brand(models.Model):
    """The brand which produces the whisky."""
    name = models.CharField(max_length=255)


class Cask(models.Model):
    """The type of cask used to create the whisky."""
    name = models.CharField(max_length=255)


class Market(models.Model):
    """The market the whisky is generally sold in."""
    name = models.CharField(max_length=255)


class Whisky(models.Model):
    """The good stuff."""

    # essential data
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand)
    wb_url = models.CharField(max_length=255)
    wb_id = models.IntegerField()

    # metadata
    age = models.CharField(max_length=255, blank=True)
    size = models.IntegerField(default=0)
    strength = models.FloatField(default=0)
    barcode = models.CharField(max_length=255, blank=True)
    vintage = models.CharField(max_length=255, blank=True)
    type = models.ForeignKey(Type)

    bottler = models.ForeignKey(Bottler)
    bottling_series = models.CharField(max_length=255)

    cask = models.ForeignKey(Cask)
    cask_number = models.CharField(max_length=255)

    # capability for multiple distilleries
    distillery = models.ManyToManyField(Distillery)


