from webbrowser import get
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()



class Category(models.Model):
    
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=False,
        null=False,
    )

    value = models.CharField(
        verbose_name=_('value'),
        max_length=255,
        blank=False,
        null=False,
    )

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    
    def __str__(self):
        return self.title

class Product(models.Model):
    """
    title
    price
    current_price
    reduction
    is_stock
    is_avtivated
    recomended
    description
    characteristics (foreignKey)
    categories (manyToMany)
    main_image
    images (foreignKey)
    """
    

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        blank=False,
        null=False,
    )
    
    # prix normale du produit
    price = models.FloatField(
        verbose_name=_('price'),
        default=0,
        blank=False,
        null=False,
    )
    
    # reduction du produits en pourcentage
    reduction = models.FloatField(
        verbose_name=_('reduction'),
        default=0,
        blank=False,
        null=False,
    )
    
    description = models.TextField(
        verbose_name=_('describe'),
        blank=True,
        null=True,
    )
    
    is_avtivated = models.BooleanField(
        verbose_name=_('is active'),
        default=False,
    )

    recomended = models.BooleanField(
        verbose_name=_('recomended'),
        default=False,        
    )
    
    is_stock = models.BooleanField(
        verbose_name=_('is stock'),
        default=True,        
    )
    
    main_image = models.ImageField(
        verbose_name=_('main image'),
        # upload_to=main_image_path,
        upload_to='image/product/main/%Y/%m/%d/%H/%M/%S/',
    )
    
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
    )
    
    update_at = models.DateTimeField(
        verbose_name=_('update at'),
        auto_now=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ['-id', ]
    
    def __str__(self):
        return self.title
    
    # prix courant du produit
    @property
    def current_price(self):
        return int(self.price-((self.price*self.reduction)/100))

    # dit si le produit est en reduction ou pas
    @property
    def disccount(self):
        if self.reduction > 0:
            return True
        return False

class Characteristics(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='characteristics',
    )
    
    title = models.CharField(
        verbose_name=_('title'),
        max_length=150,
    )
    
    value = models.TextField(
        verbose_name=_('value'),
    )

    class Meta:
        verbose_name = _('Characteristic')
        verbose_name_plural = _('Characteristics')

class Image(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        verbose_name=_('product'),
        related_name='images',
        null=False,
    )
    
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    
    image = models.ImageField(
        verbose_name=_("image link"), 
        # upload_to=image_path
        upload_to='image/product/%Y/%m/%d/%H/%M/%S/',
    )
    
    def __str__(self):
        return f'{self.product}: {self.image}'
    
    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')
 

class Order(models.Model):

    user = models.ForeignKey(
        UserModel,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )
    
    product = models.ForeignKey(
        Product,
        verbose_name=_('product'),
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_('quantity'),
        default=1,
        blank=True,
    )

    ordered = models.BooleanField(
        verbose_name=_('ordered'),
        default=False,
    )

    is_active = models.BooleanField(
        verbose_name=_('is active'),
        default=True,
    )

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')
    
    def __str__(self):
        return f'{self.product.title}'

    @property
    def order_price(self):
        return (self.product.current_price*self.quantity)

    @property
    def product_price(self):
        return self.product.current_price
    
    @property
    def title(self):
        return self.product.title
    
    @property
    def image(self):
        return self.product.main_image



class Commande(models.Model):

    user = models.ForeignKey(
        UserModel,
        verbose_name=_('user'),
        on_delete=models.CASCADE,
    )

    oeders = models.ForeignKey(
        Order,
        verbose_name=_('oeders'),
        on_delete=models.CASCADE,
    )

    is_deliver = models.BooleanField(
        verbose_name=_('is deliver'),
        default=False,
    )

    localisation_x = models.FloatField(
        verbose_name=_('localisation X'),
        default=0
    )

    localisation_y = models.FloatField(
        verbose_name=_('localisation Y'),
        default=0
    )

    



# class Cart(models.Model):

#     user = models.OneToOneField(
#         UserModel,
#         on_delete=models.CASCADE,
#     )
    
#     orders = models.ManyToManyField(
#         Order,
#         # limit_choices_to={'user': user},
#         related_name='orders'
#     )

#     class Meta:
#         verbose_name = _('cart')
#         verbose_name_plural = _('carts')
    
#     def __str__(self):
#         return f'cart: {self.user}'