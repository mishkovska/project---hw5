from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_displayed_in_menu = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    has_phone_type = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='child', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'categories'
    
    def is_root_category(self):
        return self.get_root() == self
    
    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])
    
    def __str__(self):
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        ordering = ('-created',) 
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    
    def __str__(self):
        return self.title


