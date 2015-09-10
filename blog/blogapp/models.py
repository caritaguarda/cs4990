from django.db import models

# Create your models here.
class Post(models.Model):
    body = models.TextField()
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="pics/%Y/%m/%d", blank=True, null=True)
    pub_date = models.DateTimeField()
    keywords = models.CharField(max_length=200, blank=True, null=True)

    comment = models.ManyToManyField('Comment')
    category = models.ManyToManyField('Category')

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    person = models.CharField(max_length=200)
    comment_text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s - %s" % (self.person, self.comment_text[:50])

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.category_name

