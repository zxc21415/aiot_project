

from cProfile import label
from django.shortcuts import render,redirect
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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
    
    Weights_20=Loss.objects.filter(weight_id=1).order_by('recall')
    Weights_30=Loss.objects.filter(weight_id=2).order_by('recall')
    Weights_40=Loss.objects.filter(weight_id=3).order_by('recall')
    
    precision_20 = [d.precision for d in Weights_20]
    precision_30 = [d.precision for d in Weights_30]
    precision_40 = [d.precision for d in Weights_40]

    recall_20 = [d.recall for d in Weights_20]
    recall_30 = [d.recall for d in Weights_30]
    recall_40 = [d.recall for d in Weights_40]

    mAP05_20 = [d.mAP_05 for d in Weights_20]
    mAP05_30 = [d.mAP_05 for d in Weights_30]
    mAP05_40 = [d.mAP_05 for d in Weights_40]

    mAP95_20 = [d.mAP_05_095 for d in Weights_20]
    mAP95_30 = [d.mAP_05_095 for d in Weights_30]
    mAP95_40 = [d.mAP_05_095 for d in Weights_40]

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=list(range(1,len(Weights_20))),y=precision_20, name="權重20",mode='lines'),    )
    fig.add_trace(go.Scatter(x=list(range(1,len(Weights_30))),y=precision_30, name="權重30",mode='lines'),    )
    fig.add_trace(go.Scatter(x=list(range(1,len(Weights_40))),y=precision_40, name="權重40",mode='lines'),    )
    fig.update_layout(title_text='metrics/precision')

    fig2 = make_subplots()
    fig2.add_trace(go.Scatter(x=list(range(1,len(Weights_20))),y=recall_20, name="權重20",mode='lines'),    )
    fig2.add_trace(go.Scatter(x=list(range(1,len(Weights_30))),y=recall_30, name="權重30",mode='lines'),    )
    fig2.add_trace(go.Scatter(x=list(range(1,len(Weights_40))),y=recall_40, name="權重40",mode='lines'),    )
    fig2.update_layout(title_text='metrics/recall')

    fig3 = make_subplots()
    fig3.add_trace(go.Scatter(x=list(range(1,len(Weights_20))),y=mAP05_20, name="權重20",mode='lines'),    )
    fig3.add_trace(go.Scatter(x=list(range(1,len(Weights_30))),y=mAP05_30, name="權重30",mode='lines'),    )
    fig3.add_trace(go.Scatter(x=list(range(1,len(Weights_40))),y=mAP05_40, name="權重40",mode='lines'),    )
    fig3.update_layout(title_text='metrics/mAP_0.5')

    fig4 = make_subplots()
    fig4.add_trace(go.Scatter(x=list(range(1,len(Weights_20))),y=mAP95_20, name="權重20",mode='lines'),    )
    fig4.add_trace(go.Scatter(x=list(range(1,len(Weights_30))),y=mAP95_30, name="權重30",mode='lines'),    )
    fig4.add_trace(go.Scatter(x=list(range(1,len(Weights_40))),y=mAP95_40, name="權重40",mode='lines'),    )
    fig4.update_layout(title_text='metrics/mAP_0.5:0.95')

    plot_div = plot(fig,output_type="div")
    plot_div2 = plot(fig2,output_type="div")
    plot_div3 = plot(fig3,output_type="div")
    plot_div4 = plot(fig4,output_type="div")
    return render(request,"chart.html",locals())    

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

