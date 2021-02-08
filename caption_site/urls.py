from django.urls import path

from . import views

app_name = "caption"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:image_id>/', views.image_detail, name='image_detail'),
    path('image_upload', views.image_upload, name='image_upload'),
    path('processUploadedImage', views.processUploadedImage, name="processUploadedImage"),
    path('feedback', views.getFeedbackForm, name="feedback"),
    path('processfeedback', views.processfeedback, name='processfeedback'),
    path('startfeedback', views.startfeedback, name='startfeedback'),
    path('downloadreport', views.pushReport2clientJSON, name='downloadreport'),
    path('download_csv', views.pushReport2clientCSV, name='download_csv')
]