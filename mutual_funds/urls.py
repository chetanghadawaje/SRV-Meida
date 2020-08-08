from django.urls import path
from mutual_funds import views

app_name = "mutual_funds_app"


urlpatterns = [
    path('', views.investmentView.as_view(), name='investment'),
    path('withdraw/<id>', views.withdrawView, name='withdraw')
]
