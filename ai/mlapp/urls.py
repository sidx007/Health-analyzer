from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('diabetes/', views.diabetes, name='diabetes'),
    path('hypertension/', views.hypertension, name='hypertension'),
    path('api/predict-diabetes/', views.predict_diabetes_api, name='predict_diabetes_api'),
    path('api/predict-hypertension/', views.predict_hypertension_api, name='predict_hypertension_api'),
]
