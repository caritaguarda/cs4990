from django.db import models

# Create your models here.


class Item(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey('Category')
    sku = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def increment(self):
        self.quantity += 1
        return

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'