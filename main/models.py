import datetime
from django.db import models

# Create your models here.

class Data(models.Model):
    file = models.FileField()
    file_date = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Forecast(models.Model):
    LGBM = 'lgbm'
    XGB = 'xgb'
    ADA = 'ada'
    CAT = 'cat'
    SVR = 'svr'
    MODEL_MACHINE = [
        (LGBM, 'LightGBM'),
        (XGB, 'XGBoost'),
        (ADA, 'AdaBoost'),
        (CAT, 'CatBoost'),
        (SVR, 'SVR')
    ]
    model = models.CharField(max_length=4, choices=MODEL_MACHINE, default=LGBM)
    comp_code = models.CharField(max_length=6)
    date_st = models.DateField(default=datetime.datetime.now() - datetime.timedelta(days=3*365))
    date_end = models.DateField(default=datetime.datetime.now)

class Classification(models.Model):
    LGBM = 'lgbm'
    XGB = 'xgb'
    SVM = 'svm'
    MODEL_MACHINE = [
        (LGBM, 'LightGBM'),
        (XGB, 'XGBoost'),
        (SVM, 'SVM')
    ]
    model = models.CharField(max_length=4, choices=MODEL_MACHINE, default=LGBM)
    file = models.FileField()
    target = models.CharField(max_length=256)
