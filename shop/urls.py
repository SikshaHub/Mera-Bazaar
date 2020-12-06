from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="BlogHome"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('tracker/', views.tracker, name="TrackingStatus"),
    path('search/', views.search, name="Search"),
    path('products/', views.products, name="ProductView"),
    path('product/<int:prid>', views.product, name="ProductView"),
    path('checkout/', views.checkout, name="CheckOut"),
    path('handle-request/', views.handlePaytmRequest, name="HandleRequest"),
]