from django.db import models
from django.contrib.auth.models import User
from djangotoolbox import fields

# Create your models here.
# TODO(rafi): This is a bad implementation..if you are using datastore..


class UserImage(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    image = models.FileField(upload_to='uploads/user_images')
    question = models.CharField(max_length=300, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)


class Options(models.Model):
    poll_id = models.ForeignKey(UserImage)
    option_name = models.CharField(max_length=100)
    # coordinates comprise of x1,y1,width,height
    coordinates = models.CharField(max_length=50)
    users = fields.ListField(null=True, blank=True)
    votes = models.IntegerField()


class VotingHistory(models.Model):
    poll = models.ForeignKey(UserImage)
    option_id = models.ForeignKey(Options)
    user = models.ForeignKey(User, null=True, blank=True)
    ip_address = models.CharField(max_length=15, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        #FIXME: this prolly has no effect on app-engine.
        unique_together = (('option_id', 'user', 'ip_address'),)
