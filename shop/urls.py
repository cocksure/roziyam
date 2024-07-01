from django.urls import path

from shop import views
from shop.views import product_detail, order_confirm

urlpatterns = [
	path('', views.HomePageView.as_view(), name='home'),
	path('products', views.HomePageView.as_view(), name='product_list'),
	path('product/<int:id>/', product_detail, name='product_detail'),

	path('add/<int:product_id>/', views.cart_add, name='cart_add'),
	path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
	path('card/', views.cart_detail, name='cart_detail'),
	path('order/confirm/', order_confirm, name='order_confirm'),

]
