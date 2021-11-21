from django.urls import path
from . import views


urlpatterns = [
    path('',views.store, name="store"),
    path('cart/',views.cart, name="cart"),
    path('checkout/',views.checkout, name="checkout"),
    path('card_items/',views.cardItems, name='card_items'),
    path('update_item/',views.updateItem, name='update_item'),
    path('checkout_proceed/',views.checkoutDeliveryInfor, name='checkout_proceed'),

    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('register/',views.register,name="register"),


]