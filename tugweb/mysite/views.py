

from django.shortcuts import render
#import plotly.graph_objs as go

import io
from PIL import Image as im
import torch

from django.views.generic.edit import CreateView
from mysite.models import ImageModel
from mysite.forms import ImageUploadForm


# Create your views here.
def index(request):
    return render(request,"index.html",locals())

def chart(request):
    url = 'chart'
    return render(request,"chart.html",locals())

def introduce(request):
    url = 'introduce'
    return render(request,"introduce.html",locals())

def show(request):
    url = 'show'
    return render(request,"show.html",locals())

def ship_sign(request):
    url = 'ship_sign'
    tug_list=list() #6
    bow_list=list() #5
    thruster_list=list() #6
    vessel_list=list() #3
    for i in range(1,7):
        temp = "tug0"+str(i)
        temp2 = "thruster0"+str(i)
        tug_list.append(temp)
        thruster_list.append(temp2)
    for i in range(1,6):
        temp = "bow0"+str(i)
        bow_list.append(temp)
    for i in range(1,4):
        temp = "vessel0"+str(i)
        vessel_list.append(temp)
        
    return render(request,"ship_sign.html",locals())





class UploadImage(CreateView):
    model = ImageModel
    template_name = 'image/imagemodel_form.html'
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES.get('image')
            img_instance = ImageModel(
                image=img
            )
            img_instance.save()

            uploaded_img_qs = ImageModel.objects.filter().last()
            img_bytes = uploaded_img_qs.image.read()
            img = im.open(io.BytesIO(img_bytes))

            # Change this to the correct path
            path_hubconfig = "absolute/path/to/yolov5_code"
            path_weightfile = "absolute/path/to/yolov5s.pt"  # or any custom trained model

            model = torch.hub.load(path_hubconfig, 'custom',
                               path=path_weightfile, source='local')

            results = model(img, size=640)
            results.render()
            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save("media/yolo_out/image0.jpg", format="JPEG")

            inference_img = "/media/yolo_out/image0.jpg"

            form = ImageUploadForm()
            context = {
                "form": form,
                "inference_img": inference_img
            }
            return render(request, 'image/imagemodel_form.html', context)

        else:
            form = ImageUploadForm()
        context = {
            "form": form
        }
        return render(request, 'image/imagemodel_form.html', context)