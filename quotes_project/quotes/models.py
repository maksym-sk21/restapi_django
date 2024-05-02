from django.db import models


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.TextField()
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'authors'
        app_label = 'quotes'



class Quote(models.Model):
    id = models.AutoField(primary_key=True)
    quote = models.TextField()
    author_fullname = models.CharField(max_length=100)
    tags = models.TextField()
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'quotes'
        app_label = 'quotes'

