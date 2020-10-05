from django.db import models

# Create your models here.
class Mention(models.Model):

    name = models.CharField(max_length=80)
    tweet = models.CharField(max_length=300)
    tweet_id = models.IntegerField(default=2)
    img = models.URLField(default="No img")
    replied = models.BooleanField(default='False')


    

    class Meta:
        verbose_name = ("Mention")
        verbose_name_plural = ("Mentions")

    def __str__(self):
        return self.name

  
