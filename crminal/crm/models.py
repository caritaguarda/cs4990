from django.db import models
from django.contrib.auth.models import User
import datetime


# Create your models here.
class Stage(models.Model):
    name = models.CharField(max_length=200)
    order = models.IntegerField(help_text= "The order this is displayed on the screen")
    value = models.IntegerField(help_text="On a scale of 0 to 100 of the stage of the pipeline")
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    #def Meta:
        #ordering = ??

class Company(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(max_length=200, blank=True, null=True)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def getAddress(self):
        address = ""
        if self.address1:
            address += self.address1
            address += ","
        if self.address2:
            address += self.address2
            address += ", "
        if self.city:
            address += self.city
            address += ", "
        if self.state:
            address += self.state
            address += ","
        if self.zipcode:
            address += self.zipcode
        if address != "":
            return address
        else:
            return None


    class Meta:
        verbose_name_plural = 'companies'


class Contact(models.Model):
    company = models.ForeignKey(Company, blank=True, null=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address1 = models.CharField(max_length=200, blank=True, null=True)
    address2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def getAddress(self):
        address = ""
        if self.address1:
            address += self.address1
            address += ","
        if self.address2:
            address += self.address2
            address += ", "
        if self.city:
            address += self.city
            address += ", "
        if self.state:
            address += self.state
            address += ","
        if self.zipcode:
            address += self.zipcode
        if address != "":
            return address
        else:
            return None

    def __unicode__(self):
        return self.get_full_name()



class Campaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_opportunity_count(self):
        opportunity_list = []
        for opportunity in Opportunity.objects.all().filter(source = self.id):
            opportunity_list.append(opportunity)
        return len(opportunity_list)



class Opportunity(models.Model):
    description = models.CharField(max_length=200, blank=True, null=True)
    stage = models.ForeignKey(Stage)
    company = models.ForeignKey(Company, blank=True, null=True)
    contact = models.ForeignKey(Contact)
    value = models.FloatField(help_text="How much this opportunity is worth to the organization")
    source = models.ForeignKey(Campaign)
    user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'opportunities'

    def __unicode__(self):
        if self.company and self.contact:
            return str(self.contact) + " @ " + str(self.company)
        elif self.company:
            return str(self.company)
        else:
            return str(self.contact)



class Reminder(models.Model):
    opportunity = models.ForeignKey(Opportunity)
    date = models.DateTimeField()
    note = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        str(self.opportunity) + ": " + self.note

    def markComplete(self):
        self.complete = True

class Report(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()

    def __unicode__(self):
        return self.name


class CallLog(models.Model):
    opportunity = models.ForeignKey(Opportunity)
    date = models.DateTimeField(default=datetime.datetime.now)
    note = models.TextField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.opportunity) + " on " + self.date.strftime("%Y-%m-%d") + " on " + self.user.get_full_name()


class OpportunityStage(models.Model):
    opportunity = models.ForeignKey(Opportunity)
    stage = models.ForeignKey(Stage)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.opportunity) + " moved to " + str(self.stage)





