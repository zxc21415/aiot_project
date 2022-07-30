from django.shortcuts import render
import plotly.graph_objs as go

# Create your views here.
def index(request):

    return render(request,"index.html",locals())

def chart(request):
    
   

    return render(request,"chart.html",locals())