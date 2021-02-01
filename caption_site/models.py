from django.db import models
from django.db.models.aggregates import Count
import random

# Create your models here.

class ImagesManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]

class Image(models.Model):
    # name = models.CharField(max_length=500)
    # path = models.CharField(max_length=1500)
    
    objects = ImagesManager()

    human_annotation = models.TextField()
    image = models.ImageField(upload_to='images/caption_site')

    def __str__(self):
        return self.human_annotation

class CaptionModel(models.Model):
    model_name = models.CharField(max_length=200)
    description = models.TextField(default="N/A")
    url = models.URLField(default="https://arnab-api.github.io/")

    def __str__(self):
        return str((self.model_name, self.description, self.url))


class CaptionsManager(models.Manager):
    def random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = random.randint(0, count - 1)
        return self.all()[random_index]

class Caption(models.Model):
    objects = CaptionsManager()

    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    caption_model = models.ForeignKey(CaptionModel, on_delete=models.CASCADE)
    caption_text = models.TextField()
    
    def __str__(self):
        return str((self.image_id, self.caption_model_id, self.caption_text))


class Feedback(models.Model):
    caption = models.ForeignKey(Caption, on_delete=models.CASCADE)
    rating = models.IntegerField()
    user_id = models.CharField(max_length=100)
    comments = models.TextField(default="N/A")

    def __str__(self):
        return str((self.caption_id, self.rating, self.user_id, self.comments))


class PresetOpinionOption(models.Model):
    opinion = models.CharField(max_length=200)

    def __str__(self):
        return self.opinion


class Feedback2PresetOpinion(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    opinion = models.ForeignKey(PresetOpinionOption, on_delete=models.CASCADE)

    def __str__(self):
        return str((self.feedback_id, self.opinion_id))

