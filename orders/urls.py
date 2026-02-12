from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pagar/<int:pk>', views.PaymentDetailView.as_view(), name="payment"),
    path('placeorder/', views.PlaceOrderView.as_view(), name="placeorder"),
    path('list/', views.ListOrderView.as_view(), name="list"),
    path('detail/', views.OrderDetailView.as_view(), name="detail"),
]
