from .models import Category, Product


def latest_products(request):
	latest_products = Product.available_products.all().order_by('-created')[:10]
	categories = Category.objects.all()

	context = {
		"latest_products": latest_products,
		"categories": categories
	}
	return context
