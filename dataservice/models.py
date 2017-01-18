from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from dataservice.tasks import generate_json_file_key_map

# Create your models here.
class DataFile(models.Model):
    filename = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    upload_datetime = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="JSONDoc/", default="JSONDoc/None/No-doc.json")
    key_map = models.CharField(max_length=1000, default="")
    def __str__(self):
        return "%s" % self.filename

# method for building key map
@receiver(post_save, sender=DataFile, dispatch_uid="build_key_map")
def build_key_map(sender, instance, **kwargs):
     if not instance.key_map:
         generate_json_file_key_map.delay(instance.id)

class StoredData(models.Model):
    file = models.ForeignKey(DataFile, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=255)
    calculated_value = models.CharField(max_length=100)
    calculcated_datetime = models.DateTimeField(auto_now=True)
