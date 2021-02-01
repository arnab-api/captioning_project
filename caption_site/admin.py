from django.contrib import admin

from .models import Image, Caption, CaptionModel, Feedback, PresetOpinionOption, Feedback2PresetOpinion
# Register your models here.

admin.site.register(Image)
admin.site.register(Caption)
admin.site.register(CaptionModel)
admin.site.register(Feedback)
admin.site.register(PresetOpinionOption)
admin.site.register(Feedback2PresetOpinion)


