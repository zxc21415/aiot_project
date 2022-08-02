from django.shortcuts import render
import plotly.graph_objs as go

# Create your views here.
def index(request):
    return render(request,"index.html",locals())

def chart(request):
    url = 'chart'
    return render(request,"chart.html",locals())

def introduce(request):
    url = 'introduce'
    return render(request,"introduce.html",locals())