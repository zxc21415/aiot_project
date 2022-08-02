from django.db import models

"""
 現階段規劃資料表由不同權重出發，當作外鍵，不同的權重對應到不同的損失數值們
 而現有的損失數值如下列，把每一次 epoch 結果視為單一item，如同股票之於日期
 ，日期之於當天開盤價、收盤價、成交量等。
 
  股票們     對應  權重們

股市資訊(日期)對應  每次epoch
"""


class Weight(models.Model):
    weights = models.CharField(max_length=10, verbose_name="權重")
    def __str__(self):
        return self.weights

class Loss(models.Model):
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE)
    
    box_train_loss = models.FloatField(verbose_name="box_train_loss")
    box_value_loss = models.FloatField(verbose_name="box_value_loss")
    
    obj_train_loss = models.FloatField(verbose_name="obj_train_loss")
    obj_value_loss = models.FloatField(verbose_name="obj_value_loss")
    
    cls_train_loss = models.FloatField(verbose_name="cls_train_loss")
    cls_value_loss = models.FloatField(verbose_name="cls_value_loss")
    
    precision = models.FloatField(verbose_name="準確度")
    recall = models.FloatField(verbose_name="召回率")
    
    mAP_05 = models.FloatField(verbose_name="mAP_0.5")
    mAP_05_095 = models.FloatField(verbose_name="mAP_0.5:0.95")
    
    x_lr0 = models.FloatField(verbose_name=" x/lr0")
    x_lr1 = models.FloatField(verbose_name=" x/lr1")
    x_lr2 = models.FloatField(verbose_name=" x/lr2")
    def __str__(self):
        return "({},{},{},{},{},{},{},{},{},{},{})".format(self.weight, self.precision,self.recall, #3
                                                     self.box_train_loss, self.box_value_loss,      #2
                                                     self.obj_train_loss,self.obj_value_loss,       #2
                                                     self.cls_train_loss,self.cls_value_loss,       #2
                                                     self.box_value_loss,self.box_value_loss,)      #2
