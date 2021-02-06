from django.http.response import HttpResponseRedirect
from caption_site.forms import ImageForm
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.urls import reverse

from .models import CaptionsManager, Image, Caption, CaptionModel, Feedback, PresetOpinionOption, Feedback2PresetOpinion


def index(request):
    return render(request, "caption_site/index.html")

################################## Image ##################################
def image_detail(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404("Image does not exist!!!")
    
    captions = image.caption_set.all()
    caption_arr = []
    for caption in captions:
        caption_model = CaptionModel.objects.get(pk=caption.caption_model_id)
        feedbacks = caption.feedback_set.all()
        feedback_arr = []
        for feedback in feedbacks:
            choices = feedback.feedback2presetopinion_set.all()
            choice_arr = []
            for choice in choices:
                choice_arr.append(PresetOpinionOption.objects.get(pk=choice.opinion_id))
            feedback_arr.append((feedback, choice_arr))
        caption_arr.append({
            "model_name"    : caption_model.model_name, 
            "caption_text"  : caption.caption_text,
            "feedback_arr"  : feedback_arr
        })
    # return HttpResponse("details of image {}: {}".format(image_id, data))
    
    return render(request, "caption_site/image_detail.html", {
        "image_id"          : image_id,
        "img_url"           : image.image.url,
        "human_annotation"  : image.human_annotation,
        "caption_arr"       : caption_arr 
    })



def image_upload(request):
    # return HttpResponse(request.POST[])
    caption_models = CaptionModel.objects.all()
    return render(request, "caption_site/image_upload.html", {
        "caption_models": caption_models
    })

def processUploadedImage(request):
    form = ImageForm(request.POST, request.FILES)
    if(form.is_valid()):
        form.save()
        img = form.instance
        # image.image = form.instance
        # image.human_annotation = request.POST["human_annotation"]
        # image.save()
        caption_arr = []
        caption_models = CaptionModel.objects.all()
        for model in caption_models:
            key = "caption_model_"+str(model.id)
            # captions[model] = request.POST[key]
            caption_arr.append((key, request.POST[key].strip()))
            caption_text = request.POST[key].strip()
            if(len(caption_text) != 0):
                caption = Caption(image_id= img.id, caption_model_id= model.id, caption_text= request.POST[key].strip())
                caption.save()

        return render(request, "caption_site/image_upload.html", {
            'form'          : form,
            'img_obj'       : img,
            'caption_arr'   : caption_arr
        })


################################ Feedback ################################

USER_FEEDBACK_MAX = 20

def getFeedbackForm(request):
    if not request.session.session_key:
        return render(request, "caption_site/index.html")
    
    if(request.session["feedback_caption"] == -1):
        caption = Caption.objects.random()
        request.session["feedback_caption"] = caption.id
        warn_null_feedback = False
    else:
        caption = Caption.objects.get(pk = request.session["feedback_caption"])
        warn_null_feedback = True
    
    image = Image.objects.get(pk=caption.image_id)
    caption_model = CaptionModel.objects.get(pk=caption.caption_model_id)
    # return HttpResponse("showing caption {}:  ".format(caption.id) + str(caption))

    preset_opinions = PresetOpinionOption.objects.all()

    return render(request, 'caption_site/caption_feedback.html', {
        'caption'           : caption,
        'image'             : image,
        'caption_model'     : caption_model,
        'preset_opinions'   : preset_opinions,
        'USER_FEEDBACK_MAX' : USER_FEEDBACK_MAX,
        'warn_null_feedback': warn_null_feedback
    })  

def checkValidFeedback(request):
    rating = request.POST.get('slide_mridul')
    if(rating != "0"):
        return True

    comments = request.POST['comments']
    if(len(comments) != 0):
        return True

    preset_opinions = PresetOpinionOption.objects.all()
    for opinion in preset_opinions:
        key = "opinion_"+str(opinion.id)
        if key in request.POST:
            return True

    return False

def processfeedback(request):
    check = checkValidFeedback(request)
    if (check == False):
        return HttpResponseRedirect(reverse("caption:feedback"))

    caption_id = int(request.POST['caption_id'])
    caption = Caption.objects.get(pk=caption_id)
    comments = request.POST['comments']
    rating = request.POST.get('slide_mridul')
    feedback = Feedback(rating = rating, user_id=request.session.session_key, caption_id=caption.id, comments=comments)
    feedback.save()

    checkBoxinfo = []
    preset_opinions = PresetOpinionOption.objects.all()

    for opinion in preset_opinions:
        key = "opinion_"+str(opinion.id)
        check = False
        if key in request.POST:
            check = True
            f2p = Feedback2PresetOpinion(feedback_id = feedback.id, opinion_id=opinion.id)
            f2p.save()

        checkBoxinfo.append((opinion.opinion, check))

    request.session["feedback_count"] += 1
    # return HttpResponse(caption_id)
    request.session["feedback_caption"] = -1 # feedback stored successfully
    if(request.session["feedback_count"] < USER_FEEDBACK_MAX):
        return HttpResponseRedirect(reverse("caption:feedback"))
    else:
        return HttpResponse("THANK YOU!!!!")

def startfeedback(request):
    if not request.session.session_key:
        request.session.save()
    request.session["feedback_count"] = 0
    request.session["feedback_caption"] = -1
    # return HttpResponse(request.session.session_key)
    return HttpResponseRedirect(reverse("caption:feedback"))
    # return HttpResponse(request.POST.get('slide_arnab'))




############################# Captioning Model ############################



################################# Caption #################################



################################# Feedback ################################



############################### PresetOpinions #############################

import json
def pushReport2client(request):
    report = []
    images = Image.objects.all()
    for image in images:
        img_json = {
            "human_annotation"  : image.human_annotation,
            "image_path"        : image.image.url 
        }

        caption_arr = []
        captions = image.caption_set.all()
        for caption in captions:
            caption_model = CaptionModel.objects.get(pk= caption.caption_model_id)
            caption_obj = {
                "caption"   : caption.caption_text,
                "model"     : caption_model.model_name
            }
            

            feedback_arr = []
            feedbacks = caption.feedback_set.all()
            for feedback in feedbacks:
                feedback_obj = {
                    "rating": feedback.rating,
                    "user_id": feedback.user_id,
                    "comments": feedback.comments
                }

                opinion_arr=[]
                opinions = feedback.feedback2presetopinion_set.all()
                for opinion in opinions:
                    opinion_text = PresetOpinionOption.objects.get(pk= opinion.opinion_id).opinion
                    opinion_arr.append(opinion_text)

                feedback_obj['opinion_arr'] = opinion_arr
                feedback_arr.append(feedback_obj)


            caption_obj['feedback_arr'] = feedback_arr
            caption_arr.append(caption_obj)

        img_json['caption_arr'] = caption_arr
        report.append(img_json)

    json_report = json.dumps(report, indent=4)
    # return HttpResponse(json_report)
    return render(request, "caption_site/showjson.html", { "json_str": json_report})