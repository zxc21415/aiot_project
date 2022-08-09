

from cProfile import label
from django.shortcuts import render,redirect
from plotly.offline import plot
import plotly.graph_objs as go

import io
from PIL import Image as im
import torch

from django.views.generic.edit import CreateView
from mysite.models import ImageModel, Loss
from mysite.forms import ImageUploadForm


# Create your views here.
def index(request):
    return render(request,"index.html",locals())

def chart(request):
    url = 'chart'
    return render(request,"chart.html",locals())

def chart2(request):
    url = 'chart'
    label_10=[float(i/20) for i in range(0,20)]
    Weights_20=Loss.objects.filter(weight_id=1).order_by('recall')
    Weights_30=Loss.objects.filter(weight_id=2).order_by('recall')
    Weights_40=Loss.objects.filter(weight_id=3).order_by('recall')
    recall_20 = [d.recall for d in Weights_20]
    precision_20 = [d.precision*10 for d in Weights_20]
    recall_30 = [d.recall for d in Weights_30]
    precision_30 = [d.precision for d in Weights_30]
    recall_40 = [d.recall for d in Weights_40]
    precision_40 = [d.precision for d in Weights_40]
    plot_div = plot([go.Scatter(x=recall_20,y=precision_20,mode='lines'),go.Scatter(x=recall_30,y=precision_30,mode='lines'),go.Scatter(x=recall_40,y=precision_40)],output_type="div" )
    plot_div2 = plot([go.Scatter(x=list(range(1,10)),y=precision_20,mode='lines')],output_type="div" )
    return render(request,"chart2.html",locals())
    

def introduce(request):
    url = 'introduce'
    return render(request,"introduce.html",locals())

def show(request):
    
   
    model = ImageModel
    template_name = 'show.html'
    fields = ["image"]
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        url = 'show'
        img = request.FILES.get('image')
        img_instance = ImageModel(
            image=img
        )
        img_instance.save()

        uploaded_img_qs = ImageModel.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        # Change this to the correct path
        path_hubconfig = "C:/aiot_project/tugweb/yolov5_code"
        path_weightfile = "C:/aiot_project/tugweb/absolute/path/to/best.pt"  # or any custom trained model

        model = torch.hub.load(path_hubconfig, 'custom',
                            path=path_weightfile, source='local')

        results = model(img, size=640)
        results.render()
        for img in results.imgs:
            img_base64 = im.fromarray(img)
            img_base64.save("static/media/yolo_out/image0.jpg", format="JPEG")

        inference_img = "/media/yolo_out/image0.jpg"

        form = ImageUploadForm()
        context = {
            "form": form,
            "inference_img": inference_img,
            "url": url
        }
        return render(request, 'show.html', context)

    else:
        url = 'show'
        form = ImageUploadForm()
    context = {
        "form": form,
        "url": url
    }
    return render(request, 'show.html', context)

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
    template_name = 'show.html'
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
            path_hubconfig = "C:/aiot_project/tugweb/yolov5_code"
            path_weightfile = "C:/aiot_project/tugweb/absolute/path/to/best.pt"  # or any custom trained model

            model = torch.hub.load(path_hubconfig, 'custom',
                               path=path_weightfile, source='local')

            results = model(img, size=640)
            results.render()
            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save("static/media/yolo_out/image0.jpg", format="JPEG")

            inference_img = "/media/yolo_out/image0.jpg"

            form = ImageUploadForm()
            context = {
                "form": form,
                "inference_img": inference_img
            }
            return render(request, 'show.html', context)

        else:
            form = ImageUploadForm()
        context = {
            "form": form
        }
        return render(request, 'show.html', context)