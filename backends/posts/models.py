from django.db import models
from users.models import UserAccount
from datetime import datetime
from django.template.defaultfilters import slugify

#category model
class Category(models.TextChoices):
    PRIMARY='primary school',
    MIDDLE='middle school',
    SECONDARY='secondary school',
    TERTIARY='tertiary education'


#theme model
class Theme(models.TextChoices):
    MATH='math'
    PHYS='phys'

#modality model
class Modality(models.TextChoices):
    ONLINE='online'
    OFFLINE='offline'


#posts model
class Annonces(models.Model):
    title=models.CharField(max_length=300)
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    date=models.DateTimeField(default=datetime.now, blank=True)
    photo = models.ImageField(upload_to='images/%y/%m/%d/')
    category =models.CharField(choices=Category.choices,max_length=30)
    theme=models.CharField(choices=Theme.choices,max_length=30)
    modalite=models.CharField(choices=Modality.choices,max_length=30)
    description=models.TextField()
    lieu=models.CharField(max_length=50)
    tarif=models.BigIntegerField()

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-date']


#favorite model
class Favorite(models.Model):
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post=models.ManyToManyField(Annonces)


#history model
class History(models.Model):
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post=models.ManyToManyField(Annonces)
    

#comments model
class Comments(models.Model):
    user=models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    post=models.ForeignKey(Annonces, on_delete=models.CASCADE)
    body=models.TextField()
    date=models.DateTimeField(default=datetime.now, blank=True)
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return self.body

