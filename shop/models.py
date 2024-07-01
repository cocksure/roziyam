from django.db import models
from django.urls import reverse


class AvailableManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(available=True)


class Category(models.Model):
	name = models.CharField(max_length=150, unique=True, verbose_name='Категория')
	description = models.TextField(verbose_name='Описание', blank=True)

	class Meta:
		ordering = ['name']
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name


class Product(models.Model):
	code = models.CharField(max_length=100, unique=True, verbose_name='Код', null=True, blank=True)
	name = models.CharField(max_length=200, unique=True, verbose_name='Название')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
	description = models.TextField(verbose_name='Описание')
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
	stock = models.IntegerField(verbose_name='Запасы')
	available = models.BooleanField(default=True, verbose_name='Доступен')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
	updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')

	# manager
	objects = models.Manager()
	available_products = AvailableManager()

	class Meta:
		ordering = ['name']
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('product_detail', args=[str(self.id)])


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='product_images/%Y/%m/%d', verbose_name='Дополнительное изображение')

	def __str__(self):
		return f"{self.product.name} Image"
