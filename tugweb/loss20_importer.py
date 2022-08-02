"""
先在 權重資料表 建立 權重20子項目 再進行轉移
"""


import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tugweb.settings')
django.setup()
import pandas as pd
from mysite.models import Weight, Loss





df=pd.read_csv("results20.csv")#更換檔名
'''
#舊欄位名稱(新的把空格去掉了)
Index(['Unnamed: 0', 'train/box_loss', 'val/box_loss', ' train/obj_loss',
       'val/obj_loss', ' train/cls_loss', 'val/cls_loss', 'metrics/precision',
       'metrics/recall', 'metrics/mAP_0.5', 'metrics/mAP_0.5:0.95',
       'Unnamed: 11', ' x/lr0', ' x/lr1', ' x/lr2'],
      dtype='object')
'''
print(df["train/box_loss"][0])
print(df.columns)
for i in range(0,len(df)):
    _box_train_loss=df["train/box_loss"][i]
    _box_value_loss=df["val/box_loss"][i]
    
    _obj_train_loss=df["train/obj_loss"][i]
    _obj_value_loss=df["val/obj_loss"][i]
    
    _cls_train_loss=df["train/cls_loss"][i]
    _cls_value_loss=df["val/cls_loss"][i]
    
    _precision=df["metrics/precision"][i]
    _recall=df["metrics/recall"][i]
    
    _mAP_05=df["metrics/mAP_0.5"][i]
    _mAP_05_095=df["metrics/mAP_0.5:0.95"][i]
    
    _x_lr0=df["x/lr0"][i]
    _x_lr1=df["x/lr1"][i]
    _x_lr2=df["x/lr2"][i]
    c = Weight.objects.get(id=1)
    #print(c)
    loss_instance=Loss(weight=c,
         box_train_loss=_box_train_loss, 
         box_value_loss=_box_value_loss,
         obj_train_loss=_obj_train_loss,
         obj_value_loss=_obj_value_loss,
         cls_train_loss=_cls_train_loss,
         cls_value_loss=_cls_value_loss,
         precision=_precision,
         recall= _recall,
         mAP_05=_mAP_05,
         mAP_05_095=_mAP_05_095,
         x_lr0=_x_lr0,
         x_lr1=_x_lr1,
         x_lr2=_x_lr2)
    loss_instance.save()
