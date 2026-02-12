from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('pagar/<int:pk>', views.PaymentDetailView.as_view(), name="payment"),
    path('placeorder/', views.PlaceOrderView.as_view(), name="placeorder"),
    path('list/', views.OrderListView.as_view(), name="list"),
    path('detail/<int:pk>', views.OrderDetailView.as_view(), name="detail"),
]
