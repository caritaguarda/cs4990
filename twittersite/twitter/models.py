from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User)
    bio = models.TextField('Short Bio',blank=True, null=True)
    picture = models.ImageField(upload_to="pics/%Y/%m/%d", blank=True, null=True)
    following = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __unicode__(self):
        return self.user.get_full_name() or self.user.username

class Post(models.Model):
    profile = models.ForeignKey(Profile)
    body = models.CharField(max_length=140)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-pub_date",)

    def __unicode__(self):
        return self.body

