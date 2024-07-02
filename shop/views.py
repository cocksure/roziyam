from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from shop.cart import Cart
from shop.forms import CartAddProductForm
from shop.models import Product, Category
import requests


def about_view(request):
	return render(request, 'about.html')


class HomePageView(ListView):
	model = Product
	context_object_name = 'product'
	paginate_by = 9

	def get_template_names(self):
		if self.request.path == '/products':
			return ['products.html']
		else:
			return ['home_page.html']

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context['product_list'] = Product.objects.order_by('-created')[:10]
		context['man_products'] = Product.available_products.filter(category__id=1).order_by('-created')[:5]
		context['woman_products'] = Product.available_products.filter(category__id=2).order_by('-created')[:3]
		context['kids_products'] = Product.available_products.filter(category__id=3).order_by('-created')[:5]
		context['accessory_products'] = Product.available_products.filter(category__id=4).order_by('-created')[:5]

		print(context['man_products'])
		return context


def product_detail(request, id):
	product = get_object_or_404(Product, id=id)
	cart_product_form = CartAddProductForm()

	return render(request, 'single-product.html', {'product': product, 'cart_product_form': cart_product_form})


@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
	return redirect('cart_detail')


def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('cart_detail')


def cart_detail(request):
	cart = Cart(request)
	return render(request, 'cart_detail.html', {'cart': cart})


def order_confirm(request):
	if request.method == 'POST':
		cart = Cart(request)

		client_name = request.POST.get('client_name', '')
		client_phone = request.POST.get('client_phone', '')

		order_details = "\n".join(
			[f"{item['product'].name} - {item['quantity']} шт. - {item['total_price']} руб." for item in cart])

		total_price = cart.get_total_price()

		telegram_message = f"Новый заказ от {client_name} ({client_phone}):\n{order_details}\nОбщая стоимость: {total_price} сум."

		send_telegram_message(telegram_message)

		cart.clear()

		return redirect('cart_detail')
	else:
		return redirect('cart_detail')


def send_telegram_message(message):
	bot_token = settings.TELEGRAM_BOT_TOKEN
	chat_id = settings.TELEGRAM_CHAT_ID
	url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
	payload = {
		'chat_id': chat_id,
		'text': message
	}
	requests.post(url, data=payload)
